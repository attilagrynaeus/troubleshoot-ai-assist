"""
paste directly from your clipboard or text files
"""

import sys
from app.agent import ask

def main():
    trace = sys.stdin.read().strip()
    if not trace:
        print("⚠️ Paste your stack trace via stdin.")
        sys.exit(1)

    fix = ask(trace)
    print(f"🛠️ Fix suggestion:\n{fix}")

if __name__ == "__main__":
    main()
