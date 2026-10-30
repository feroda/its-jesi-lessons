# Soluzioni della simulazione

Da correggere insieme in classe subito dopo, o da dare agli studenti: la simulazione non vale per il voto.

20 punti in 60 minuti. Come riferimento, 12 punti corrispondono alla sufficienza del compito vero.

I risultati dell'esercizio 3 valgono per i log committati nel repository (seed 1337).

| Es. | Risposta | Punti |
|---|---|---|
| 1a | Loki 3100, Prometheus 9090 | 1 + 1 |
| 1b | il PC: ha un IP privato, il VPS non lo raggiunge (push) | 1 |
| 2a | ping 3, curl 7, nc 4 | 1 + 1 + 1 |
| 2b | sì: ha risposto a livello 7 con un codice HTTP; il 302 è solo il rimando alla pagina di login | 1 |
| 3a | `cat -n`: stampa il file con i numeri di riga; `tail -n 5`: mostra le ultime 5 righe | 1 + 1 |
| 3b | `grep Accepted sshd_highprec.log \| cut -d' ' -f7 \| sort \| uniq -c \| sort -rn \| head -1` (vale anche `awk '{print $7}'`); `anna`, 6 volte | 1 + 1 |
| 3c | `grep ' 404 ' apache_access.log \| cut -d' ' -f1 \| sort \| uniq -c \| sort -rn \| head -1` (vale anche `grep '\<404\>'`); 185.220.101.54, 45 volte (è lo scanner di directory) | 1 + 1 |
| 4a | `Hello from Docker!`: la stampa il container stesso (vale anche la riga "This message shows that your installation appears to be working correctly"). Non vale la prima riga: la scrive il client `docker` dopo che il demone ha risposto "immagine non trovata", quindi dice solo che il demone risponde, non che il container è partito | 1 |
| 4b | ha finito il suo lavoro ed è fermo | 1 |
| 5a | `grafana/grafana`; `"3000:3000"` (1 punto l'immagine, 1 punto le porte) | 1 + 1 |
| 5b | V | 1 |
| 6 | agentless; retention | 1 + 1 |

## Cosa guardare durante la simulazione

- Chi non riesce a collegarsi con `ssh`: va sistemato prima del compito (client SSH, password, rete della scuola).
- Chi nel 3c si ferma a `sort | uniq -c` senza il secondo `sort -rn`: è l'errore più probabile anche nel compito.
- Chi nel 2b risponde "no" perché vede 302 invece di 200: vale la pena ripetere che qualsiasi codice HTTP vuol dire che il servizio risponde.
