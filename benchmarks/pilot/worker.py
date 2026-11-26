"""Execute a candidate in the grading container, never on the live host."""
import contextlib
import io
import json
import sys

def main():
    with contextlib.redirect_stdout(io.StringIO()):
        from candidate import solve
        inputs = json.load(sys.stdin)
        results = []
        for value in inputs:
            try:
                results.append({"value": solve(value)})
            except Exception as exc:
                results.append({"error": type(exc).__name__})
    print(json.dumps(results, allow_nan=False))

if __name__ == "__main__":
    main()
