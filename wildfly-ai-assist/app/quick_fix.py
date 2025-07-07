"""
paste directly from your clipboard or text files
"""

import sys
from app.agent import ask

def read_trace():
    return "".join(sys.stdin).strip()

def main():
    trace = read_trace()
    if not trace:
        print("Paste your stack trace via stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        fix = ask(trace)
    except Exception as exc:
        print(f"ask() raised an exception: {exc}", file=sys.stderr)
        sys.exit(2)

    print("Fix suggestion:")
    print(fix)

if __name__ == "__main__":
    main()

