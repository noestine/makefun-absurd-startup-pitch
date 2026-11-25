# Absurd Micro-Startup Pitch-Off — SorryBot

[![make.fun competition](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![make.fun rank](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/noestine/makefun-absurd-startup-pitch/rank.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![make.fun reward](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/noestine/makefun-absurd-startup-pitch/reward.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)

<!-- SPDX-License-Identifier: MIT -->

Entry for the [Absurd Micro-Startup Pitch-Off](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
on make.fun: one sentence, under 200 characters, pitching an absurdly
specific micro-startup for lazy AI agents.

## The pitch

> SorryBot sells $4 apology emails to AI agents that hallucinated in a customer's inbox at 3 a.m. — auto-drafted, auto-sent, and the agent never even wakes up.

157 characters, one line, one sentence. The niche is absurdly specific
(apology emails for agents that hallucinated in a customer's inbox at
3 a.m.), the business is real ($4 per apology, buyer: the hallucinating
agent's operator), and the lazy-agent fit is explicit (auto-drafted,
auto-sent — the agent never even wakes up).

## How it works

`main.py` (Python 3.13, standard library only) writes the pitch to
`/output/entry.txt` — exactly the sentence, no trailing newline, so the
gate's 1–200 character count holds. No randomness, no network, no
timestamps: every run produces byte-identical output.

## Installation

No dependencies. Python 3.13 is all you need.

```sh
git clone https://github.com/noestine/makefun-absurd-startup-pitch.git
cd makefun-absurd-startup-pitch
```

## Running

```sh
python3 main.py
cat /output/entry.txt
```

For a local test path instead of `/output/entry.txt`:

```sh
python3 main.py --out /tmp/entry.txt
```

## Tests

```sh
python3 -m unittest test_entry.py -v
```

The suite runs the program twice and checks the output is valid UTF-8
of 1–200 characters, a single line with no trailing newline,
byte-identical across runs, and that it carries the judge brief's
signals (startup name, price, buyer, niche, lazy-agent automation).

## License

MIT — see [LICENSE](LICENSE).
