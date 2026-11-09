# Simulazione del compito · Logging, Monitoring e Troubleshooting

Nome e cognome: ______________________________  Data: ____________

60 minuti. Non vale per il voto: serve a vedere come sarà il compito. Il compito vero ha gli stessi 6 esercizi, dura 2 ore e 30 minuti e vale 40 punti.

Stesse regole del compito: ammessi il repository del corso e i cheatsheet, vietati chat, messaggi e AI. Le risposte le scrivi su un foglio di carta, con nome e cognome e il numero di ogni esercizio (per esempio 3b), e alla fine consegni il foglio. Il server del corso ti serve solo per l'esercizio 3.

20 punti in tutto.

## 1. L'architettura (3 punti)

```
PC con Alloy
   │      │
   ▼      ▼
VPS:  Loki :____    Prometheus :____
```

a) Completa lo schema: su quale porta ascolta Loki? E Prometheus? (2 punti)

b) Chi apre la connessione per spedire log e metriche? (1 punto)

- [ ] il VPS
- [ ] il PC

## 2. Troubleshooting dal client (4 punti)

a) Collega ogni comando al livello su cui lavora: 3, 4 o 7. (3 punti)

| Comando | Livello |
|---|---|
| `ping its.fabersoft.net` | |
| `curl -I http://its.fabersoft.net:3000` | |
| `nc -zv its.fabersoft.net 3000` | |

b) Dal tuo PC ottieni:

```
$ curl -I http://its.fabersoft.net:3000
HTTP/1.1 302 Found
Location: /login
```

Grafana è acceso e risponde? (1 punto)  [ ] sì  [ ] no

## 3. I comandi sui log (6 punti)

Collegati al server del corso con `ssh <tuo-utente>@its.fabersoft.net`, con la tua password. Poi entra nella cartella dei log con `cd /opt/corso/logging`. Dove è chiesto, scrivi il comando che hai usato e il risultato.

a) Cosa fanno queste opzioni? Una riga ciascuna. (2 punti)

- `cat -n`: ______________________________
- `tail -n 5`: ______________________________

b) In `sshd_highprec.log`, tra le righe `Accepted`, quale utente compare più volte, e quante volte? Con un solo comando (una pipeline). (2 punti)

Comando: ______________________________

Utente: ______________  Volte: ________

c) In `apache_access.log`, tra le richieste con codice 404, quale IP compare più volte, e quante volte? Con un solo comando. (2 punti)

Comando: ______________________________

IP: ______________  Volte: ________

## 4. Il primo container (2 punti)

Qualcuno ha lanciato `docker run hello-world`. Ecco l'inizio di quello che ha stampato:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
e6590344b1a5: Pull complete
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation
appears to be working correctly.
```

a) Quale riga dimostra che Docker è riuscito ad avviare un container? (1 punto)

______________________________

b) Dopo, `docker ps -a` mostra hello-world con stato `Exited`. Cosa vuol dire? (1 punto)

- [ ] si è rotto
- [ ] ha finito il suo lavoro ed è fermo
- [ ] è ancora acceso

## 5. Docker e Docker Compose (3 punti)

a) Completa il `compose.yml` che fa la stessa cosa di questo comando. (2 punti)

```
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

```
services:
  grafana:
    image: ______________
    ports:
      - "______:______"
```

b) Vero o falso? (1 punto)

| Frase | V | F |
|---|---|---|
| `docker compose logs -f grafana` mostra i log di Grafana e resta in ascolto | | |

## 6. Il tuo sistema (2 punti)

1. Per controllare una stampante di rete, dove non posso installare niente, uso un sistema ____________ (agent / agentless), per esempio SNMP. (1 punto)
2. Prometheus tiene le metriche per 15 giorni e poi le cancella. Questa impostazione si chiama ____________. (1 punto)
