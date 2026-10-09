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

`loki-grafana/compose.yml` has no `restart:` policy while `journal-alloy/compose.yml` uses `unless-stopped`. This is the likely reason Grafana stayed down in the lesson 1 incident, and the lesson 3 deck (slide 13) uses it as the example, so if you add a restart policy to the server stack, update that slide too.

```bash
docker compose up -d
docker compose ps
docker compose logs -f alloy   # or loki, grafana
```

## Slides

`logging/slides/assets/imgs/` holds one SVG source and its PNG export (3200x1800) per slide, named `slideN-<descrizione>`. The SVG is the source of truth, so edit it and re-export the PNG. Slide 6 also has step-by-step PNGs (`-passo1` to `-passo3`) for a progressive reveal; these have no SVG of their own.

New slides follow the existing look: 1600x900 viewBox, white background, DejaVu Sans (DejaVu Sans Mono for commands), and the palette already used in the other SVGs.

`logging/slides/Troubleshooting.pdf` is the assembled deck and is built from the PNGs, so it must be rebuilt whenever a slide is added or changed. Page order is slide 0 to 9, with slide 6 expanded as passo1, passo2, passo3 and then the full image:

```bash
cd logging/slides
I=assets/imgs
magick $I/slide0-*.png $I/slide1-*.png $I/slide2-*.png $I/slide3-*.png $I/slide4-*.png $I/slide5-*.png \
  $I/slide6-viaggio-pacco-passo{1,2,3}.png $I/slide6-viaggio-pacco.png \
  $I/slide7-*.png $I/slide8-*.png $I/slide9-*.png \
  -units PixelsPerInch -density 240 -compress zip Troubleshooting.pdf
```

`logging/slides/assets/imgs/docker/` holds the lesson 3 deck on Docker and Docker Compose, with the same SVG plus PNG convention and its own numbering (slide 0 to 15). It lives in a subfolder so the `slideN-*` globs above keep matching only the Troubleshooting deck. Slides 3 and 4 are redrawn from two third-party diagrams (Microsoft Learn and Nordic APIs, credited in the subtitles) rather than copied, because the repository is public. The assembled deck is `logging/slides/Docker.pdf`:

```bash
cd logging/slides
I=assets/imgs/docker
magick $(for n in $(seq 0 15); do ls $I/slide$n-*.png; done) \
  -units PixelsPerInch -density 240 -compress zip Docker.pdf
```

To export an SVG to PNG, pass absolute paths: the snap build of Inkscape on this machine resolves relative paths from the home directory. Flatten the result to RGB so it matches the other slides.

```bash
inkscape "$PWD/$I/slideN-nome.svg" --export-type=png --export-width=3200 --export-background=white --export-filename="$PWD/$I/slideN-nome.png"
magick $I/slideN-nome.png -background white -alpha remove -alpha off $I/slideN-nome.png
```

## Cheatsheets

Two Markdown handouts for students live in `logging/`:

- `cheatsheet-comandi.md` covers the shell tools for reading logs (`cat`, `cut`, `wc`, `sort`, `uniq`, `tail`, `grep`, `sed`). Its examples run from `logging/` against the committed logs and some use values from the seed 1337 dataset (a queue ID, two IPs, a timestamp), so they need updating if the logs are regenerated with another seed. After editing it, run every command again to check it still works.
- `cheatsheet-troubleshooting.md` covers network and service troubleshooting layer by layer (`ping`, `nc`, `curl` from the client; `ss`, `journalctl`, `docker compose logs`, `tcpdump` on the server). It is the text companion of slides 8 and 9 and uses the same shopping-centre metaphor as the deck, so keep the two aligned.

## Other PDFs

These are exported documents with no source in this repository:

- `RecapLezione1.pdf`: written recap of lesson 1, including the live troubleshooting of the Grafana and Alloy stacks.
- `logging/Logging-Monitoring-Troubleshooting_part1.pdf`: slides of the first lesson (image-only, no extractable text).
- `02_shell_GNULinux_Luca Ferroni.pdf`: introduction to the GNU/Linux shell (Bash builtins versus external programs, `help`, `man`, `PATH`), printed from the teacher's GitLab course material for another class. It is background reading for the shell tools used here.
