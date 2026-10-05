# Cheatsheet: esaminare i log da riga di comando

Gli strumenti visti a fine Lezione 1: `cat`, `cut`, `wc`, `sort`, `uniq`, `tail`, `grep`, `sed`.

Tutti gli esempi si eseguono dalla cartella `logging/` sui file:

| File | Formato |
|---|---|
| `sshd_classic.log` | syslog classico (`Sep  8 03:11:00 srv sshd[...]: ...`) |
| `sshd_highprec.log` | stessi eventi, timestamp ad alta precisione (`2026-09-08T03:11:00.000000+02:00 ...`) |
| `apache_access.log` | Apache combined |
| `mail.log` | Postfix, syslog classico |

## L'idea di fondo: la pipe

Ogni comando fa una cosa sola. Con `|` l'output di uno diventa l'input del successivo:

```bash
grep '\<404\>' apache_access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn
#  filtra le righe          estrae un campo   ordina   conta    classifica
```

Lo schema **filtra, estrai, ordina, conta, classifica** risolve la maggior parte delle domande sui log.

```
grep -w '404' apache_access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn
grep ' 404 ' apache_access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn
```

## cat: leggere un file

```bash
cat mail.log                 # stampa tutto il file
cat -n mail.log              # con i numeri di riga
cat sshd_*.log               # concatena più file
```

Per file lunghi è più comodo `less mail.log` (si esce con `q`, si cerca con `/testo`).

## wc: contare

```bash
wc -l mail.log               # numero di righe
wc -l *.log                  # righe di ogni file, più il totale
grep 'Accepted' sshd_classic.log | wc -l    # quante righe escono da una pipe
```

`-w` conta le parole, `-c` i byte.

## tail (e head): la fine e l'inizio

```bash
tail mail.log                # ultime 10 righe
tail -n 5 mail.log           # ultime 5
tail -n +80 sshd_classic.log # dalla riga 80 fino alla fine
tail -f /var/log/syslog      # segue il file mentre cresce (Ctrl+C per uscire)
head -n 3 apache_access.log  # prime 3 righe
```

`tail -f` è lo strumento da usare su un server vivo: si lancia, si riproduce il problema, si guarda cosa compare.

## grep: filtrare le righe

```bash
grep 'Failed password' sshd_classic.log     # righe che contengono il testo
grep -i 'invalid user' sshd_classic.log     # ignora maiuscole/minuscole
grep -v 'Accepted' sshd_classic.log         # righe che NON lo contengono
grep -c 'Failed password' sshd_classic.log  # conta le righe (come | wc -l)
grep -n 'Accepted' sshd_classic.log         # con il numero di riga
grep -l '45.9.14.207' *.log                 # solo i nomi dei file che lo contengono
grep -A1 'qmgr' mail.log                    # anche 1 riga dopo (-B prima, -C intorno)
```

Con `-E` si usano le espressioni regolari estese, con `-o` si stampa solo la parte che corrisponde:

```bash
grep -E 'status=(bounced|deferred)' mail.log        # una cosa oppure l'altra
grep -o 'status=[a-z]*' mail.log                    # solo "status=..."
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' sshd_classic.log   # solo gli indirizzi IP
```

Attenzione ai filtri troppo larghi: `grep 404` trova anche una dimensione o una porta che contiene 404. Meglio `grep ' 404 '`, con gli spazi.

I filtri si concatenano:

```bash
grep 'Failed password' sshd_classic.log | grep -v 'invalid user'
```

## cut: estrarre colonne

```bash
cut -d' ' -f1 apache_access.log      # campo 1 con separatore spazio: l'IP
cut -d' ' -f1,9 apache_access.log    # campi 1 e 9: IP e codice di stato
cut -d' ' -f1-3 mail.log             # dal campo 1 al 3
cut -d'"' -f2 apache_access.log      # separatore virgolette: la richiesta
cut -d'"' -f6 apache_access.log      # lo user agent
cut -c1-15 sshd_classic.log          # i caratteri da 1 a 15: il timestamp
```

Campi utili di `apache_access.log` con `-d' '`: 1 = IP, 4 = data, 6 = metodo, 7 = URL, 9 = stato, 10 = dimensione.

### La trappola del doppio spazio

`cut` considera **ogni** spazio un separatore. Nel syslog classico i giorni da 1 a 9 sono scritti con due spazi (`Sep  8`), quindi tra i due c'è un campo vuoto e tutti i campi successivi slittano di uno:

```bash
grep 'Invalid user' sshd_classic.log | cut -d' ' -f1-3,8     # sbagliato nei giorni 1-9
```

Rimedi:

```bash
# comprimere gli spazi ripetuti prima del cut
grep 'Invalid user' sshd_classic.log | tr -s ' ' | cut -d' ' -f1-3,8

# usare awk, che tratta più spazi come un solo separatore
awk '/Invalid user/{print $1, $2, $3, $8}' sshd_classic.log
```

In `sshd_highprec.log` il problema non esiste, ma data e ora stanno in un solo campo, quindi i numeri cambiano: l'utente passa dal campo 8 al campo 6.

```bash
grep 'Invalid user' sshd_highprec.log | cut -d' ' -f1,6
```

Prima di fidarsi di un numero di campo conviene sempre provarlo su due o tre righe.

## sort: ordinare

```bash
sort file            # ordine alfabetico
sort -n file         # ordine numerico (altrimenti 10 viene prima di 9)
sort -r file         # ordine inverso
sort -rn file        # numerico decrescente: i più grandi in cima
sort -u file         # ordina ed elimina i doppioni
```

## uniq: righe ripetute

`uniq` confronta solo righe **adiacenti**: va sempre preceduto da `sort`. Come fare `sort -u` in pratica.

```bash
cut -d' ' -f1 apache_access.log | sort | uniq       # gli IP distinti
cut -d' ' -f1 apache_access.log | sort | uniq -c    # con il numero di occorrenze
cut -d' ' -f1 apache_access.log | sort | uniq -d    # solo quelli che compaiono più volte
```

Il finale `sort | uniq -c | sort -rn` produce una classifica, e `head` la taglia:

```bash
cut -d' ' -f9 apache_access.log | sort | uniq -c | sort -rn             # codici di stato
cut -d'"' -f6 apache_access.log | sort | uniq -c | sort -rn             # user agent
grep -o 'status=[a-z]*' mail.log | sort | uniq -c                # esiti delle consegne
cut -d' ' -f1 sshd_highprec.log | cut -dT -f1 | sort | uniq -c   # eventi per giorno
```

## sed: selezionare e trasformare

Stampare un intervallo di righe (`-n` spegne la stampa automatica, `p` stampa):

```bash
sed -n '10,12p' mail.log                              # righe da 10 a 12
```

Sostituire con `s/cerca/sostituisci/` (`g` = tutte le occorrenze della riga):

```bash
sed 's/  */ /g' sshd_classic.log                      # comprime gli spazi ripetuti
sed -E 's/([0-9]{1,3}\.){3}[0-9]{1,3}/X.X.X.X/g' sshd_classic.log   # anonimizza gli IP
```

`sed` scrive sul terminale e non tocca il file. L'opzione `-i` modifica il file sul posto: sui log non si usa.

## Ricette

```bash
# Chi fa più richieste al web server?
cut -d' ' -f1 apache_access.log | sort | uniq -c | sort -rn | head

# Quali URL ha chiesto un certo IP?
grep '^185.220.101.54 ' apache_access.log | cut -d' ' -f7

# Da quali IP arrivano i tentativi SSH falliti?
grep 'Failed password' sshd_classic.log | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn

# Su quali utenti reali si concentrano i fallimenti?
grep 'Failed password' sshd_classic.log | grep -v 'invalid user' | tr -s ' ' | cut -d' ' -f9 | sort | uniq -c

# Tutta la storia di un messaggio di posta, dato il suo queue ID
grep 'B1AF284995' mail.log

# Lo stesso IP compare in più log?
grep -l '45.9.14.207' *.log
```
