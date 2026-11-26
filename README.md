<p align="center"><img src="assets/mark.svg" width="104" alt="Engineering Reliability mark"></p>
<h1 align="center">Engineering Reliability</h1>
<p align="center"><em>Small changes. Strong evidence. Safer releases.</em></p>
<p align="center"><a href="README.es.md">Español</a> · <a href="INSTALL.md">Install</a> · <a href="benchmarks/README.md">Benchmarks</a></p>
<p align="center"><img alt="Agent Skills" src="https://img.shields.io/badge/Agent%20Skills-compatible-334155?style=flat-square"> <img alt="Status" src="https://img.shields.io/badge/status-preview-64748b?style=flat-square"></p>

AI agents can write code quickly. Reliability is knowing what that code changes, what could break, and what has actually been verified.

Engineering Reliability is a risk-aware set of [Agent Skills](https://agentskills.io/) for software development. It works with existing repositories, languages and tools instead of imposing a new stack.

## Install

```sh
pnpm dlx skills add bcuyul/Engineering-Reliability
```

For all projects, add `-g`. Choose the agents interactively. See [installation and compatibility](INSTALL.md) for native plugins and persistent instructions.

## The method

**Understand → Reuse → Simplify → Verify → Release**

Read the affected code. Prefer existing capabilities. Make the smallest complete change. Test according to risk. Never call a release stable without evidence.

| Risk | Approach |
| --- | --- |
| R0 · Research | Evidence, no changes |
| R1 · Small fix | Focused diff and verification |
| R2 · Feature | Contracts, alternatives, regression tests, review |
| R3 · Critical | Authorization, isolation, recovery, independent review |

Security, data integrity, accessibility and recovery are not optional shortcuts. Stateful changes must verify [lifecycle transitions and invariants](skills/engineering-reliability/references/state-transitions.md), not only isolated operations.

## Skills

| Skill | Purpose |
| --- | --- |
| [engineering-reliability](skills/engineering-reliability/SKILL.md) | Core engineering workflow |
| [engineering-review](skills/engineering-review/SKILL.md) | Review a diff and affected callers |
| [engineering-audit](skills/engineering-audit/SKILL.md) | Find and rank repository risks |
| [engineering-dependencies](skills/engineering-dependencies/SKILL.md) | Evaluate libraries, licenses and stable versions |
| [engineering-release](skills/engineering-release/SKILL.md) | Verify release readiness |

Skills are selected by the host or explicitly invoked. For persistent guidance, merge [AGENTS.md](AGENTS.md) into your project's instructions. Prompts guide behavior; CI enforces checks.

## Before / after

**Task:** Add a library to parse CSV imports.

- Without a workflow: install a package and implement the happy path.
- With Engineering Reliability: inspect the existing parser and standard library, check malformed rows and resource limits, reuse the simplest suitable implementation, and record the tests run.

Illustrative example, not a measured benchmark.

## Evidence, not promises

The [benchmark protocol](benchmarks/README.md) measures correctness, regressions, unnecessary dependencies, cost and time. Results are not published until measured.

No runtime scripts, telemetry or network calls are required by the skills themselves. Host and installer behavior is separate.

Inspired by [Ponytail](https://github.com/DietrichGebert/ponytail) and [Superpowers](https://github.com/obra/superpowers). See [contributing](CONTRIBUTING.md) and [security](SECURITY.md).
