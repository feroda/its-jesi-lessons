# Cheat sheet: troubleshooting di rete e servizi

Si procede un livello alla volta, dal basso verso l'alto.
Nella metafora: prima il centro commerciale (IP), poi la porta del negozio, poi la lingua del negozio.

Negli esempi il server è `befair3.befair.it` (128.140.61.87), con Grafana sulla porta 3000 e Loki sulla 3100.

## Dal client

### Livello 3 · IP: il centro commerciale è raggiungibile?

```bash
ping -c 3 befair3.befair.it
```

- Risposte `64 bytes from ...`: il server è raggiungibile.
- `100% packet loss`: **non vuol dire che il server sia spento.** Molti server bloccano il ping (ICMP). befair3 non risponde al ping, ma è acceso. Passa al livello 4.

### Livello 4 · porta: il negozio è aperto?

```bash
nc -zv befair3.befair.it 3100
# alternativa
telnet befair3.befair.it 3100
```

| Risultato | Significato |
|---|---|
| `succeeded` / `Connected` | la porta è aperta, qualcuno ascolta |
| `Connection refused` | il server c'è, ma nessuno ascolta su quella porta |
| nessuna risposta / timeout | un firewall blocca, oppure il server non è raggiungibile |

### Livello 7 · HTTP: il negozio risponde nella sua lingua?

```bash
curl http://befair3.befair.it:3100/ready            # Loki: risponde "ready"
curl -v http://befair3.befair.it:3000/api/health    # Grafana: -v mostra richiesta e risposta
wget -qO- http://befair3.befair.it:3100/ready       # alternativa a curl
```

- Codice `200`: il servizio risponde correttamente.
- Codice `4xx` o `5xx`: la porta è aperta, ma il servizio ha un problema. Guarda i log sul server.

## Sul server

### Chi è in ascolto e su quale porta? (livello 4)

```bash
sudo ss -lptn
# -l in ascolto, -p processo, -t TCP, -n numeri invece dei nomi
sudo ss -lptn | grep 3000
```

- Sostituisce `netstat -pltn`, che su molte distribuzioni non è più installato.
- Con Docker il processo che vedi sulla porta è `docker-proxy`, non `grafana`.

### Cosa dice il sistema? (log)

```bash
journalctl -n 100 -f                         # ultime 100 righe, poi continua a seguire
journalctl --since "1 hour ago"              # da un'ora fa
journalctl --since "2026-10-05 03:00"        # da un momento preciso
journalctl -u docker --since "1 hour ago"    # solo il servizio docker
```

I log dei container Docker normalmente **non** finiscono in journalctl. Si leggono dalla directory del compose:

```bash
cd /opt/loki-grafana
docker compose ps                  # quali container girano
docker compose logs -f grafana     # log di un container, in tempo reale
docker compose logs --since 1h loki
```

### I pacchi arrivano davvero fin qui? (livelli 3 e 4)

```bash
sudo tcpdump -ni any port 3100       # pacchetti da e verso la porta 3100
sudo tcpdump -ni any -A port 3000    # -A mostra anche il contenuto (HTTP in chiaro)
```

- Ogni riga mostra mittente e destinatario come `IP.porta > IP.porta`.
- Se qui non arriva niente, il problema è prima del server: rete, firewall, indirizzo sbagliato.
- Si ferma con `Ctrl+C`.

## Percorso tipico

1. Il client vede un errore: `ping` (L3), poi `nc` (L4), poi `curl` (L7).
2. Il problema compare a un certo livello? Entra nel server.
3. `ss -lptn`: il servizio è in ascolto sulla porta giusta?
4. `docker compose ps` e `docker compose logs`, oppure `journalctl`: cosa dice il servizio?
5. Ancora nessuna risposta? `tcpdump`: i pacchetti arrivano?
