# Logging, Monitoring e Troubleshooting

ITS Jesi 2026/2027, 6 lezioni da 5 ore. Il corso parte dal sistema completo (raccolta centralizzata dei log con Grafana, Loki e Alloy) e scende fino ai log del sistema operativo e alla riga di comando; nelle ultime lezioni risale e lo costruiamo noi.

## Lez. 1 - Troubleshooting di un caso reale

L'obiettivo di questa lezione è avere il quadro d'insieme di un'architettura di logging centralizzato,
facendo troubleshooting su un caso reale: i 2 servizi di aggregazione e visualizzazione dei log (Loki e Grafana) non erano attivi.

- Troubleshooting di Grafana sul server befair3: `ping`, `ssh`, `netstat -pltn4`, poi `docker compose ps` e `docker compose logs grafana` in `/opt/loki-grafana`, e infine `docker compose up -d`.
- Troubleshooting di Alloy, il client che invia i log a Loki: raggiungibilità IP (livello 3), porta 3100 con `nc` (livello 4), `docker compose logs -f alloy` in `/opt/journal-alloy`.
- Sul VPS del corso `its.fabersoft.net`: ricerca di un utente in `/home` e in `/etc/passwd` con `cat`, `grep`, `cut` e `awk`.

Abbiamo visto anche che i log di un container si leggono con `docker logs` e, per i servizi di un compose, con `docker compose logs`.

Gli stessi concetti sono stati ripresi nella lezione 3 con la metafora del "centro commerciale": [Troubleshooting.pdf](./logging/slides/Troubleshooting.pdf)

RECAP: [RecapLezione1.pdf](./RecapLezione1.pdf)

## Lez. 2 - Logging e analisi dei log

In questa lezione abbiamo visto le entità del sistema operativo che producono log (kernel, demoni, applicazioni)
e verso chi li inviano: nei sistemi meno recenti a syslog (che li scrive in `/var/log/`), in quelli moderni a systemd-journald, che si legge con `journalctl`. Le due cose non si escludono.
Inoltre altri programmi (di solito demoni) possono scrivere direttamente file di log, di solito in `/var/log/`,
ma anche in directory proprie. I container, infine, loggano attraverso dockerd e i loro log si vedono con `docker logs` o `docker compose logs`.

Abbiamo visto anche gli strumenti più utili da riga di comando per analizzare i log:
`cat`, `cut`, `wc`, `sort`, `uniq`, `tail`, `grep`, e i più avanzati (che non vedremo in dettaglio) `sed` e `awk`.

Fuori programma, sul VPS del corso abbiamo fatto troubleshooting di un processo al 400% di CPU: era un cryptominer (XMRig) camuffato da `fail2ban`.

Abbiamo clonato il repository del corso (`git clone https://github.com/feroda/its-jesi-lessons`), con i log per gli esercizi e due cheatsheet: [comandi per i log](./logging/cheatsheet-comandi.md) e [troubleshooting](./logging/cheatsheet-troubleshooting.md).

Rif: [Logging-Monitoring-Troubleshooting_part1.pdf](./logging/slides/Logging-Monitoring-Troubleshooting_part1.pdf)

Esercizio: [01_ex_greppa_i_logs.txt](./logging/01_ex_greppa_i_logs.txt)

RECAP: [RecapLezione2.pdf](./RecapLezione2.pdf)

## Lez. 3 - Esercizi sui log e Docker

In questa lezione abbiamo corretto gli esercizi della lezione precedente ([01_ex_greppa_i_logs.txt](./logging/01_ex_greppa_i_logs.txt)),
poi abbiamo ripreso le slide Troubleshooting sulla prima lezione (livelli 3, 4 e 7, strumenti lato client e lato server), per passare a Docker:
container e macchine virtuali, registry, immagini e container, il demone `dockerd`, `docker run hello-world`, `docker ps` e `docker ps -a`, le porte.

Rif: [Lezione3-docker.pdf](./logging/slides/Lezione3-docker.pdf), fino alla slide 9

RECAP: [RecapLezione3.pdf](./RecapLezione3.pdf)

## Lez. 4 - Docker Compose e log centralizzati (prevista)

- Docker Compose, il minimo: il file `compose.yml` (`image`, `ports`, `volumes`, `restart`) e i comandi `up -d`, `ps`, `logs`, `down`. Differenza tra `docker run` e `docker compose up`.
- Costruiamo l'architettura della lezione 1: Loki e Grafana sul VPS del corso ([vps-corso](./logging/vps-corso/)), Alloy sul proprio PC ([pc-studente](./logging/pc-studente/)) che invia i log a Loki.
- Grafana e LogQL: gli esercizi della lezione 2 rifatti sul server centrale.
- Troubleshooting di un client che non invia i log.

Rif: [Lezione4-compose.pdf](./logging/slides/Lezione4-compose.pdf)

## Lez. 5 - Monitoraggio (prevista)

- Basi del monitoraggio: metriche e log, agent e agentless, pull e push, database a serie temporali e retention, SNMP.
- Aggiungiamo Prometheus al `compose.yml` del server e facciamo inviare ad Alloy anche le metriche del PC (push).
- Observability: log e metriche dello stesso host insieme in Grafana.
- Simulazione del compito.

Rif: [Lezione5-monitoraggio.pdf](./logging/slides/Lezione5-monitoraggio.pdf)

## Lez. 6 - Ripasso e compito (prevista)

- Ripasso e compito in classe su: architettura d'insieme; troubleshooting lato client ai livelli 3, 4 e 7; i comandi per leggere i log (`cat`, `cut`, `wc`, `sort`, `uniq`, `tail`, `grep`) sui file del repository; `docker run hello-world`; differenza tra Docker e Docker Compose; come impostereste un sistema di raccolta dei log e di monitoraggio.

Rif: [Lezione6-ripasso.pdf](./logging/slides/Lezione6-ripasso.pdf)
