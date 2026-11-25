"""Absurd Micro-Startup Pitch-Off entry.

Writes one pitch sentence to /output/entry.txt (or to the path given
with --out, for local testing). The pitch is a fixed constant: no
randomness, no network, no timestamps, so every run writes byte-for-byte
the same text. The file holds exactly the sentence, with no trailing
newline, because the gate counts every character (1-200).
"""

import argparse
from pathlib import Path

PITCH = (
    "SorryBot sells $4 apology emails to AI agents that hallucinated "
    "in a customer's inbox at 3 a.m. \u2014 auto-drafted, auto-sent, "
    "and the agent never even wakes up."
)

DEFAULT_OUT = Path("/output/entry.txt")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the pitch to entry.txt.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output path (default: /output/entry.txt)")
    args = parser.parse_args()
    # Defensive gate check: refuse to write an entry the scorer would
    # reject, instead of silently shipping an invalid one.
    if not 1 <= len(PITCH) <= 200 or not PITCH.strip() or "\n" in PITCH:
        print("error: pitch fails the 1-200 character single-line gate")
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(PITCH, encoding="utf-8")
    print(f"wrote {len(PITCH)} characters to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
