"""Tests for the Absurd Micro-Startup Pitch-Off entry.

The program (main.py) writes one pitch sentence to /output/entry.txt.
The gate requires UTF-8 text of 1-200 characters, not only whitespace.
These tests run the program twice and check the output is valid,
deterministic, and answers the judge brief (specific niche, buyer,
price, lazy-agent fit) in a single line.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent
MAIN = REPO / "main.py"


def run_main(out_path):
    """Run main.py writing to out_path; return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(MAIN), "--out", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )


class TestEntry(unittest.TestCase):
    def test_runs_successfully(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.is_file(), "main.py must create the output file")

    def test_deterministic_across_two_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.txt"
            second = Path(tmp) / "second.txt"
            self.assertEqual(run_main(first).returncode, 0)
            self.assertEqual(run_main(second).returncode, 0)
            self.assertEqual(first.read_bytes(), second.read_bytes(),
                             "two runs must produce byte-identical output")

    def test_gate_valid_utf8_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            raw = out.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), "no UTF-8 BOM")
            text = raw.decode("utf-8")  # raises if not valid UTF-8
            self.assertGreaterEqual(len(text), 1, "entry must not be empty")
            self.assertLessEqual(len(text), 200,
                                 f"entry is {len(text)} chars, gate caps at 200")
            self.assertTrue(text.strip(), "entry must not be only whitespace")
            # Report the exact counts for the build log.
            print(f"\nchars={len(text)} bytes={len(raw)}")

    def test_single_line_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            text = out.read_text(encoding="utf-8")
            self.assertNotIn("\n", text, "entry must be a single line")
            self.assertNotIn("\r", text, "entry must not contain CR")
            self.assertEqual(text, text.rstrip(),
                             "entry must not end with trailing whitespace")
            self.assertTrue(text.endswith("."),
                            "entry is one sentence ending with a period")

    def test_one_sentence(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            text = out.read_text(encoding="utf-8")
            # The only ". " sequence is inside "3 a.m."; the sentence ends
            # with its single terminal period.
            self.assertEqual(text.count(". "), 1,
                             "entry must be one sentence (one '. ' inside '3 a.m.')")

    def test_judge_brief_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            text = out.read_text(encoding="utf-8")
            self.assertIn("SorryBot", text, "pitch must name the startup")
            self.assertIn("$4", text, "pitch must name the price (business sense)")
            self.assertIn("agent", text.lower(),
                          "pitch must name the buyer: AI agents")
            self.assertIn("apology", text.lower(),
                          "pitch must name the absurdly specific niche")
            self.assertIn("auto-", text,
                          "pitch must show the lazy-agent fit (auto-drafted/sent)")

    def test_rerun_overwrites_not_appends(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            first = out.read_bytes()
            self.assertEqual(run_main(out).returncode, 0)
            self.assertEqual(out.read_bytes(), first,
                             "a re-run must overwrite, never append")


if __name__ == "__main__":
    unittest.main()
