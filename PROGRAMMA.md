# Logging, Troubleshooting, Monitoring

## Lez. 1 - Troubleshooting

L'obiettivo di questa lezione è di avere il quadro di insieme di un'architettura di logging centralizzato
effettuando attività di troubleshooting perché 2 servizi di aggregazione e visualizzazione dei log non sono attivi (loki e grafana).

In questa lezione abbiamo visto tutti i concetti che poi sono stati riproposti con una metafora del "centro commerciale" 
nelle slides: [./logging/slides/Troubleshooting.pdf]

RECAP: [./RecapLezione1.pdf]

Abbiamo visto anche che per visionare i logs di docker è necessario fare docker logs.


## Lez. 2 - Logging ed analisi

In questa lezione abbiamo visto le entità del sistema operativo che effettuano logging
e verso chi le effettuano: prima syslogd, ora journalctl. Ma non sono esclusivi.
Inoltre altri programmi (di solito demoni) possono scrivere direttamente file di logs, di solito in /var/log/,
ma anche in directory incluse nel loro ramo di directory, e poi aggiungiamo che i container possono loggare anche
attraverso dockerd e in effetti i logs si vedono con docker logs o docker compose logs

In questa lezione abbiamo anche visto gli strumenti più utili da riga di comando per analizzare i logs,
come `cut`, `cat`, `wc`, `sort`, `uniq`, `tail`, `grep` e i più avanzati (che non vedremo in dettaglio) `sed`, `awk`

Rif: [https://github.com/feroda/its-jesi-lessons/blob/main/logging/slides/Logging-Monitoring-Troubleshooting_part1.pdf](Logging monitoring etc.)

RECAP: [./RecapLezione2.pdf]

## Lez. 3 - Esercizi logging e docker

In questa lezione abbiamo risolto gli esercizi della lezione precedente

[https://github.com/feroda/its-jesi-lessons/blob/main/logging/01_ex_greppa_i_logs.txt]

poi abbiamo visionato le slides Troubleshooting che riguardavano la prima lezione, per passare a Docker

Rif: https://github.com/feroda/its-jesi-lessons/blob/main/logging/slides/Docker.pdf

RECAP: [./RecapLezione3.pdf]

