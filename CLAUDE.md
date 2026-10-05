# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Teaching material for a course on logging, monitoring and troubleshooting at ITS Jesi (2026). It is not a software project: there is no build, lint or test suite. The content is slides, lesson recaps, sample log files for shell exercises, and small Docker Compose stacks used in live demos.

All course material (slides, comments, docstrings, exercise text) is written in Italian. Write new material in Italian.

The repository is pushed to GitHub and read by students, so anything committed is visible to them.

## Exercise logs (`logging/`)

`logging/genera_log.py` (standard library only) generates the four exercise logs plus the answer key:

```bash
cd logging
python3 genera_log.py                # seed 1337, reproduces the committed logs byte for byte
python3 genera_log.py --seed random  # a different dataset each run
python3 genera_log.py --seed 42 --out ./logs
```

`--out` defaults to the current directory, so run it from `logging/` (or pass `--out logging`) to refresh the committed files.

Things that are not obvious from a single file:

- **The committed `.log` files are generator output, not hand-written.** Change the generator and regenerate rather than editing the logs. All five outputs come from one seeded `random.Random` consumed in a fixed order (SSH, then Apache, then mail), so adding or removing a single random call in an earlier section changes everything after it.
- **`soluzioni.txt` is the answer key and is gitignored on purpose.** It is computed from the generated events, so it stays correct for any seed, but it must not be committed. If the logs are regenerated with a different seed, the local `soluzioni.txt` changes with them.
- **The quirks in the logs are the lesson.** Each one is planted deliberately:
  - `sshd_classic.log` uses the classic syslog timestamp and includes days 1 to 9, which produce a double space (`Sep  8`) that breaks `cut -d' '` but not `awk`. `mail.log` only uses days 10 to 31, so it has no such problem.
  - `sshd_highprec.log` holds the same SSH events with an rsyslog high-precision timestamp, so date and time collapse into one field and field numbers shift (the invalid user moves from field 8 to field 6).
  - SSH scenarios: password spraying from `185.22.1.9` on day 8, and a brute force from `45.9.14.207` against `deploy` that ends in one successful login.
  - Apache scenarios: a directory scanner (`185.220.101.54`, burst of 404s) and SQL injection attempts from `45.9.14.207`, the same IP as the SSH brute force.
  - Mail scenarios: two queue IDs appear twice because of retries (deferred then sent, deferred then bounced), so counting `status=sent` counts delivered recipients, not unique messages.

  When changing the generator, keep these properties or update the notes that `main()` writes into `soluzioni.txt`.
- `parsing-classic-corretto.txt` holds the reference shell solutions for the double-space problem (`awk`, or `tr -s ' '` before `cut`).

## Demo stacks

Two independent Compose stacks mirror the real setup used for live troubleshooting in class (see `RecapLezione1.pdf`). They run on different machines:

- `logging/loki-grafana/` is the server side: Loki on port 3100 (single node, filesystem storage, no auth) and Grafana on port 3000. Deployed on the server under `/opt/loki-grafana`.
- `logging/journal-alloy/` is the client side: Grafana Alloy reads the host's systemd journal (bind-mounted read-only) and pushes it to Loki. Deployed on each client under `/opt/journal-alloy`.

The Loki push URL and the `host` label are hardcoded in `journal-alloy/alloy/config.alloy` and must be changed per client. Grafana has no provisioning here: the Loki datasource is added by hand in the UI.

```bash
docker compose up -d
docker compose ps
docker compose logs -f alloy   # or loki, grafana
```

## Slides

`logging/slides/assets/imgs/` holds one SVG source and its PNG export per slide, named `slideN-<descrizione>`. The SVG is the source of truth, so edit it and re-export the PNG. Slide 6 also has step-by-step PNGs (`-passo1` to `-passo3`) for a progressive reveal. The PDFs are exported presentations and are not generated from this repository.
