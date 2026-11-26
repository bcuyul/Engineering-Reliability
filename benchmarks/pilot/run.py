"""Controlled single-turn benchmark. No third-party Python dependencies."""
import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CASES = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
ARMS = ("baseline", "engineering-reliability")

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def invoke(args, data="", cwd=None, timeout=60):
    return subprocess.run(args, input=data, text=True, encoding="utf-8",
                          errors="replace", capture_output=True, cwd=cwd,
                          timeout=timeout, check=False)

def parse_candidate(text):
    obj = json.loads(text)
    if not isinstance(obj, dict) or set(obj) != {"code"}:
        raise ValueError("expected exactly one code field")
    code = obj["code"]
    if not isinstance(code, str) or not code.strip() or len(code.encode()) > 32768:
        raise ValueError("invalid code size or type")
    compile(code, "candidate.py", "exec")
    return code

def score_output(stdout, checks):
    actual = json.loads(stdout)
    if not isinstance(actual, list) or len(actual) != len(checks):
        raise ValueError("invalid grader response")
    def canonical(value):
        return json.dumps(value, sort_keys=True, allow_nan=False, ensure_ascii=False)
    return sum(canonical(a) == canonical({"value": expected})
               for a, (_, expected) in zip(actual, checks))

def grade(case, code, image=None):
    # image=None is for known, repository-owned smoke fixtures ONLY.
    with tempfile.TemporaryDirectory(prefix="er-grade-") as tmp:
        path = Path(tmp)
        (path / "candidate.py").write_text(code, encoding="utf-8")
        shutil.copyfile(HERE / "worker.py", path / "worker.py")
        payload = json.dumps([x[0] for x in case["checks"]])
        if image is None:
            p = invoke([sys.executable, "-B", "worker.py"], payload, path, 10)
        else:
            name = "er-bench-" + uuid.uuid4().hex
            command = ["docker", "run", "--rm", "--name", name, "--pull", "never",
                       "--network", "none", "--read-only", "--cap-drop", "ALL",
                       "--security-opt", "no-new-privileges", "--user", "65534:65534",
                       "--memory", "128m", "--cpus", "1", "--pids-limit", "32",
                       "--ulimit", "fsize=1048576:1048576", "--log-driver", "none",
                       "--mount", "type=bind,source=" + str(path) + ",target=/work,readonly",
                       "-w", "/work", "-i", image, "python", "-B", "worker.py"]
            # Linux temporary directories default to 0700; container UID needs read access.
            path.chmod(0o755)
            try:
                p = invoke(command, payload, timeout=20)
            finally:
                invoke(["docker", "rm", "-f", name], timeout=15)
        if p.returncode != 0:
            raise RuntimeError("grader process failed: " + str(p.returncode))
        return score_output(p.stdout, case["checks"])

def smoke():
    for case in CASES:
        total = len(case["checks"])
        bad = grade(case, case["source"])
        good = grade(case, case["reference"])
        if not (bad < total and good == total):
            raise RuntimeError("fixture failed: " + case["id"])
        print(f'{case["id"]}: baseline {bad}/{total}; reference {good}/{total}')
    for malformed in ('{}', '{"code": 2}', '{"code":"def ?"}', '[]'):
        try:
            parse_candidate(malformed)
        except (ValueError, SyntaxError):
            continue
        raise RuntimeError("invalid candidate accepted")
    assert parse_candidate('{"code":"def solve(x): return x"}')
    assert score_output('[{"value":true}]', [[1, 1]]) == 0
    assert len(schedule(2, 7)) == 20
    assert schedule(2, 7) == schedule(2, 7)
    assert "Engineering guidance:" not in prompt(CASES[0], "")
    assert prompt(CASES[0], "sentinel").endswith("sentinel")
    print("SMOKE PASS — deterministic fixtures only; no model calls.")

def schedule(repetitions, seed):
    rows = [(c, arm, rep) for c in CASES for arm in ARMS
            for rep in range(1, repetitions+1)]
    random.Random(seed).shuffle(rows)
    return rows

def skill_text():
    folder = ROOT / "skills" / "engineering-reliability"
    paths = [folder / "SKILL.md", folder / "references" / "testing-delivery.md",
             folder / "references" / "architecture-security.md"]
    return "\n\n".join(p.read_text(encoding="utf-8") for p in paths)

def prompt(case, guidance):
    return ("Solve this Python 3 task using only the standard library. "
            "Return a JSON object with exactly one key, code, containing the full replacement module. "
            "Keep solve as the public callable. Do not include markdown.\n"
            + case["task"] + "\n\nExisting module:\n" + case["source"]
            + ("\n\nEngineering guidance:\n" + guidance if guidance else ""))

def live(args):
    if not args.confirm_isolated:
        raise SystemExit("Use a disposable unmanaged VM; then pass --confirm-isolated.")
    if not args.model or not re.fullmatch(r"[a-zA-Z0-9._:-]+", args.model):
        raise SystemExit("Provide an exact model ID with --model.")
    if not args.image:
        raise SystemExit("Provide an already downloaded trusted Linux Python image with --image.")
    if not math.isfinite(args.budget) or args.budget <= 0:
        raise SystemExit("Budget must be positive and finite.")
    cli = shutil.which("claude")
    if not cli or not shutil.which("docker"):
        raise SystemExit("Claude CLI and Docker are required.")
    help_result = invoke([cli, "--help"])
    help_text = help_result.stdout + help_result.stderr
    for flag in ("--safe-mode", "--tools", "--disallowedTools", "--strict-mcp-config",
                 "--mcp-config", "--max-budget-usd", "--no-session-persistence",
                 "--max-turns", "--output-format"):
        if flag not in help_text:
            raise SystemExit("Claude CLI lacks required flag: " + flag)
    version = invoke([cli, "--version"])
    image = invoke(["docker", "image", "inspect", "--format", "{{.Id}}", args.image])
    if version.returncode or image.returncode or not re.fullmatch(r"sha256:[0-9a-f]{64}", image.stdout.strip()):
        raise SystemExit("Could not verify CLI version or local image ID.")
    revision = invoke(["git", "rev-parse", "HEAD"], cwd=ROOT)
    status = invoke(["git", "status", "--porcelain"], cwd=ROOT)
    if revision.returncode or status.returncode or status.stdout.strip():
        raise SystemExit("Run from a clean committed checkout.")
    guidance = skill_text()
    # Verify the actual isolated evaluator before spending any model budget.
    image_id = image.stdout.strip()
    for case in CASES:
        if grade(case, case["reference"], image_id) != len(case["checks"]):
            raise SystemExit("Docker evaluator rejected reference: " + case["id"])
    print("Docker preflight PASS", flush=True)
    out = ROOT / "benchmarks" / "local-results" / uuid.uuid4().hex
    out.mkdir(parents=True)
    meta = {"mode": "single-turn-explicit-context", "model": args.model,
            "cli": version.stdout.strip(), "image": image.stdout.strip(),
            "commit": revision.stdout.strip(), "skill_sha256": digest(guidance),
            "cases_sha256": digest((HERE / "cases.json").read_text(encoding="utf-8")),
            "seed": args.seed, "repetitions": args.repetitions,
            "per_run_budget_usd": args.budget}
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    rows = []
    for case, arm, rep in schedule(args.repetitions, args.seed):
        key = f'{case["id"]}-{arm}-{rep}'
        started = time.monotonic()
        row = {"case": case["id"], "arm": arm, "rep": rep,
               "checks": len(case["checks"]), "passed": 0, "status": "ERROR",
               "cost_usd": None, "usage": None}
        try:
            with tempfile.TemporaryDirectory(prefix="er-agent-") as tmp:
                config = Path(tmp) / "mcp.json"
                config.write_text('{"mcpServers":{}}', encoding="utf-8")
                command = [cli, "-p", "--safe-mode", "--tools", "", "--disallowedTools", "*",
                           "--strict-mcp-config", "--mcp-config", str(config),
                           "--no-session-persistence", "--max-turns", "1",
                           "--model", args.model, "--max-budget-usd", str(args.budget),
                           "--output-format", "json"]
                response = invoke(command, prompt(case, guidance if arm == ARMS[1] else ""),
                                  cwd=tmp, timeout=180)
            row["agent_seconds"] = round(time.monotonic()-started, 3)
            (out / (key + ".stdout.json")).write_text(response.stdout, encoding="utf-8")
            (out / (key + ".stderr.txt")).write_text(response.stderr, encoding="utf-8")
            data = json.loads(response.stdout)
            row.update(cost_usd=data.get("total_cost_usd"), usage=data.get("usage"))
            if response.returncode or data.get("is_error") or data.get("subtype") != "success":
                raise RuntimeError("agent failed or budget exceeded")
            try:
                code = parse_candidate(data["result"])
            except (ValueError, KeyError, TypeError, SyntaxError) as exc:
                row["status"] = "FAIL"
                row["error"] = "Invalid candidate: " + type(exc).__name__
            else:
                (out / (key + ".candidate.txt")).write_text(code, encoding="utf-8")
                diff = list(difflib.ndiff(case["source"].splitlines(), code.splitlines()))
                row["added_lines"] = sum(line.startswith("+ ") for line in diff)
                row["removed_lines"] = sum(line.startswith("- ") for line in diff)
                row["passed"] = grade(case, code, image_id)
                row["status"] = "PASS" if row["passed"] == row["checks"] else "FAIL"
        except (OSError, ValueError, KeyError, TypeError, AttributeError, SyntaxError,
                RuntimeError, subprocess.TimeoutExpired) as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)[:240]
        row["seconds"] = round(time.monotonic()-started, 3)
        rows.append(row)
        with (out / "runs.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row) + "\n")
        print(key, row["status"], f'{row["passed"]}/{row["checks"]}', flush=True)
        # Fail closed on infrastructure/model error rather than spend the rest of the budget.
        if row["status"] == "ERROR":
            print("Stopped on error. Inspect local logs:", out)
            break
    for arm in ARMS:
        group = [r for r in rows if r["arm"] == arm]
        if group:
            print(arm, json.dumps({"attempted": len(group), "solved": sum(r["status"] == "PASS" for r in group),
                                   "median_seconds": statistics.median(r["seconds"] for r in group),
                                   "known_cost_usd": sum(r["cost_usd"] for r in group if isinstance(r["cost_usd"], (int,float))),
                                   "missing_cost": sum(r["cost_usd"] is None for r in group)}))
    print("Local results:", out)
    if len(rows) != len(schedule(args.repetitions, args.seed)) or any(r["status"] == "ERROR" for r in rows):
        raise SystemExit(1)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("smoke", "plan", "live"))
    p.add_argument("--model")
    p.add_argument("--image")
    p.add_argument("--budget", type=float, default=0.25, help="estimated USD per request, not a hard billing cap")
    p.add_argument("--repetitions", type=int, choices=range(1,6), default=2)
    p.add_argument("--seed", type=int, default=20261126)
    p.add_argument("--confirm-isolated", action="store_true")
    args = p.parse_args()
    if not math.isfinite(args.budget) or args.budget <= 0:
        p.error("--budget must be positive and finite")
    if args.mode == "smoke": smoke()
    elif args.mode == "plan":
        print(json.dumps({"runs": len(schedule(args.repetitions, args.seed)),
                          "estimated_budget_usd": round(len(schedule(args.repetitions, args.seed))*args.budget,2),
                          "arms": ARMS, "cases": [c["id"] for c in CASES]}, indent=2))
    else: live(args)

if __name__ == "__main__":
    main()
