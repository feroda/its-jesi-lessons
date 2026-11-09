import sys
from lib import *

S = []
add = lambda name, body, side=False: S.append((name, page(body, side)))

# 0 titolo
art = (box(1130, 300, 200, 90, ALLOY, "Alloy", 28) + box(1130, 420, 200, 90, ALLOY, "Alloy", 28) +
       box(1130, 540, 200, 90, ALLOY, "Alloy", 28) +
       arrow(1335, 345, 1405, 440, ALLOY, 4) + arrow(1335, 465, 1405, 465, ALLOY, 4) + arrow(1335, 585, 1405, 490, ALLOY, 4) +
       box(1410, 410, 150, 110, LOKI, "Loki", 28) +
       t(1335, 700, "tanti PC, un solo posto", 26, GREY, anchor="middle"))
S.append(("titolo", titlepage("LEZIONE 4", "Log", "centralizzati", art)))

# 1 dove eravamo
add("dove-eravamo", [
    h("Dove eravamo", "Lezione 3: Docker fino al primo container"),
    step(1, 290, "docker run hello-world", "il primo container"),
    step(2, 400, "docker ps -a", "anche quelli fermi"),
    step(3, 510, "-p 8007:80", "porta fuori : porta dentro"),
    rect(70, 620, 1460, 200, "#FFFFFF"),
    t(110, 700, "Oggi: dal comando al file compose.yml,", 36, INK, True),
    t(110, 760, "e poi i log di tutta la classe in un posto solo.", 36, INK, True),
])

# 2 da run a compose
c, _, ys = code(70, 190, 1460, ["$ docker run -d --name web -p 8080:80 nginx:alpine"], 30, dark=True, pad=30)
c2, _, _ = code(70, 390, 900, ["services:", ("  web:", PINK, True), ("    image: nginx:alpine", DOCKER, True),
                            "    ports:", ('      - "8080:80"', TEAL, True)], 32)
add("da-run-a-compose", [
    h("Da docker run a compose.yml"), c, t(70, 365, "compose.yml", 28, GREY, True, mono=True), c2,
    t(1020, 480, "Stesso container,", 34, INK, True), t(1020, 530, "scritto in un file.", 34, INK, True),
    t(1020, 620, "Si legge, si copia,", 30, INK2), t(1020, 665, "si versiona con git.", 30, INK2),
    t(1020, 750, "YAML: spazi, mai tab.", 30, INK2),
])

# 3 ports
add("ports", [
    h("ports: fuori e dentro", "La stessa regola di docker run -p"),
    t(800, 300, '"3100:3100"', 80, TEAL, True, "middle", mono=True),
    t(640, 380, "porta del server", 30, INK2, anchor="middle"), t(1000, 380, "porta del container", 30, INK2, anchor="middle"),
    box(110, 470, 420, 150, INK2, "server", 36, "its.fabersoft.net", fill="#FFFFFF"),
    pill(535, 515, 150, ":3100", TEAL),
    arrow(690, 545, 905, 545, TEAL, 5),
    pill(910, 515, 150, ":3100", LOKI),
    box(1065, 470, 420, 150, LOKI, "container loki", 34),
    note(760, "Chi arriva da fuori bussa alla porta del server: Docker lo passa al container.", 30, INK2, False),
])

# 4 volumes
add("volumes", [
    h("volumes: i dati stanno fuori", "Due modi di mettere qualcosa dentro un container"),
    code(70, 210, 1460, [("loki-data:/loki", AMBER, True)], 34, pad=28)[0],
    t(110, 360, "Un disco gestito da Docker.", 32, INK, True),
    t(110, 410, "Butti via il container, i log restano.", 30, INK2),
    code(70, 490, 1460, [("./loki/config.yml:/etc/loki/config.yml:ro", AMBER, True)], 34, pad=28)[0],
    t(110, 640, "Un file della tua cartella, visto dentro il container.", 32, INK, True),
    t(110, 690, ":ro = sola lettura: il container lo legge, non lo cambia.", 30, INK2),
])

# 5 restart
add("restart", [
    h("restart: unless-stopped", "Il caso della lezione 1: Grafana spento, nessuno lo riaccende"),
    code(70, 230, 1460, [("restart: unless-stopped", ALLOY, True)], 44, pad=34)[0],
    bullets(120, 460, ["Si ferma da solo o si riavvia il server: riparte.",
                       "L'hai fermato tu: resta fermo."], 36, 90, dot=ALLOY),
    note(760, "Lo mettiamo in tutti i servizi, server e client.", 32, INK2, False),
])

# 6 comandi
add("comandi", [
    h("I comandi di docker compose", "Sempre dalla cartella dove c'è il compose.yml"),
    step(1, 290, "docker compose up -d", "avvia tutto"),
    step(2, 400, "docker compose ps", "chi gira?"),
    step(3, 510, "docker compose logs -f alloy", "log in tempo reale"),
    step(4, 620, "docker compose down", "ferma e cancella i container"),
    note(760, "I volumi restano: down non cancella i dati.", 30, INK2, False),
])

# 7 run o up
add("run-o-up", [
    h("docker run o docker compose up?"),
    rect(70, 200, 700, 560, "#FFFFFF", DOCKER, 3), rect(830, 200, 700, 560, "#FFFFFF", ALLOY, 3),
    t(420, 290, "docker run", 44, DOCKER, True, "middle", mono=True),
    t(420, 380, "un container", 34, INK, True, "middle"),
    t(420, 470, "tutto scritto", 30, INK2, anchor="middle"), t(420, 515, "sulla riga di comando", 30, INK2, anchor="middle"),
    t(420, 620, "lo rilanci: un altro", 30, INK2, anchor="middle"), t(420, 665, "container (o un errore)", 30, INK2, anchor="middle"),
    t(1180, 290, "docker compose up", 44, ALLOY, True, "middle", mono=True),
    t(1180, 380, "tutti i servizi del file", 34, INK, True, "middle"),
    t(1180, 470, "tutto scritto", 30, INK2, anchor="middle"), t(1180, 515, "in compose.yml", 30, INK2, anchor="middle"),
    t(1180, 620, "lo rilanci: cambia solo", 30, INK2, anchor="middle"), t(1180, 665, "quello che hai modificato", 30, INK2, anchor="middle"),
])

# 8 cosa costruiamo
pcs = ""
for i, (y, n) in enumerate([(220, "PC di Anna"), (420, "PC di Mario"), (620, "il tuo PC")]):
    pcs += rect(70, y, 330, 140, "#FFFFFF", INK2, 3, 12) + t(235, y + 45, n, 26, INK2, True, "middle")
    pcs += box(120, y + 65, 230, 55, ALLOY, "Alloy", 26)
    pcs += arrow(405, y + 92, 644, 400 + i * 30, ALLOY, 4)
add("cosa-costruiamo", [
    h("Cosa costruiamo"),
    rect(590, 220, 560, 560, "#FFFFFF", INK, 4, 18), t(870, 270, "VPS its.fabersoft.net", 28, INK, True, "middle"),
    pcs, t(405, 200, "push :3100", 28, ALLOY, True),
    box(650, 370, 440, 120, LOKI, "Loki", 36, "raccoglie i log"),
    box(650, 590, 440, 120, GRAFANA, "Grafana", 36, "li mostra"),
    arrow(870, 588, 870, 496, GREY, 3, "7 6"),
    box(1290, 590, 240, 120, INK2, "browser", 32, fill="#FFFFFF"),
    arrow(1285, 650, 1096, 650, GRAFANA, 4), t(1215, 700, ":3000", 26, GRAFANA, True, "middle"),
])

# 9 perché push
add("perche-push", [
    h("Perché è il PC a spedire", "Livello 3: chi riesce a raggiungere chi?"),
    rect(70, 230, 500, 520, "#FFFFFF", INK2, 3, 18, "10 8"), t(300, 290, "casa o scuola (rete privata)", 26, GREY, True, "middle"),
    box(100, 420, 310, 140, ALLOY, "il tuo PC", 32, "192.168.1.23", 26),
    arrow(415, 490, 462, 490, ALLOY, 5),
    box(470, 400, 200, 180, INK2, "router", 32, "IP pubblico", 24, fill="#FFFFFF"),
    box(1080, 420, 450, 140, INK, "VPS", 36, "IP pubblico", fill="#FFFFFF"),
    arrow(675, 450, 1070, 450, ALLOY, 6), t(872, 425, "il PC raggiunge il VPS", 26, ALLOY, True, "middle"),
    arrow(1070, 540, 680, 540, PROM, 6, "14 10"), t(872, 595, "il VPS vede solo il router", 26, PROM, True, "middle"),
    note(820, "Quindi è Alloy, sul PC, ad aprire la connessione e spedire.", 32, INK, True),
])

# 10 server: loki
c, _, ys = code(70, 190, 1000, ["services:", ("  loki:", LOKI, True), ("    image: grafana/loki:3.7.0", DOCKER, True),
                                "    command: -config.file=/etc/loki/config.yml", "    volumes:",
                                ("      - ./loki/config.yml:/etc/loki/config.yml:ro", AMBER, True),
                                ("      - loki-data:/loki", AMBER, True), "    ports:", ('      - "3100:3100"', TEAL, True),
                                ("    restart: unless-stopped", ALLOY, True)], 26, 52)
add("server-loki", [
    h("Il server (1/2): Loki", "logging/vps-corso/compose.yml"), c,
    t(1110, ys[2], "← immagine e versione", 28, DOCKER, True),
    t(1110, ys[3], "← il file di configurazione", 28, INK2, True),
    t(1110, (ys[5] + ys[6]) / 2 + 14, "← configurazione e dati", 28, AMBER, True),
    t(1110, ys[8], "← dove arrivano i log", 28, TEAL, True),
    t(1110, ys[9], "← riparte da solo", 28, ALLOY, True),
])

# 11 server: grafana
c, _, ys = code(70, 190, 1000, [("  grafana:", GRAFANA, True), ("    image: grafana/grafana:13.2.4", DOCKER, True), "    volumes:",
                                ("      - grafana-data:/var/lib/grafana", AMBER, True), "    ports:", ('      - "3000:3000"', TEAL, True),
                                ("    restart: unless-stopped", ALLOY, True), "", "volumes:", ("  loki-data:", AMBER, True),
                                ("  grafana-data:", AMBER, True)], 26, 50)
add("server-grafana", [
    h("Il server (2/2): Grafana", "logging/vps-corso/compose.yml, continua"), c,
    t(1110, ys[3], "← utenti e cruscotti", 28, AMBER, True),
    t(1110, ys[5], "← qui apri il browser", 28, TEAL, True),
    t(1110, ys[9], "← i volumi di Docker,", 28, AMBER, True),
    t(1140, ys[10], "dichiarati in fondo", 28, AMBER, True),
])

# 12 lo avviamo insieme
add("avvio-server", [
    h("Il server: lo avviamo insieme", "Sul VPS, lo faccio io: voi controllate dal vostro PC"),
    step(1, 270, "cd its-jesi-lessons/logging/vps-corso", size=30),
    step(2, 370, "docker compose up -d", size=30),
    step(3, 470, "docker compose ps", "tutti e due Up?", size=30),
    step(4, 570, "curl http://its.fabersoft.net:3100/ready", "ready", size=30),
    step(5, 670, "http://its.fabersoft.net:3000", "admin / admin", size=30),
    step(6, 770, "Sorgente dati Loki: http://loki:3100", size=30),
])

# 13 client compose
c, _, ys = code(70, 175, 960, ["services:", ("  alloy:", ALLOY, True), ("    image: grafana/alloy:v1.20.1", DOCKER, True),
                               ("    hostname: mario-rossi", PROM, True), "    command:", "      - run",
                               "      - --server.http.listen-addr=0.0.0.0:12345", "      - --storage.path=/var/lib/alloy/data",
                               "      - /etc/alloy/config.alloy", "    ports:", ('      - "127.0.0.1:12345:12345"', TEAL, True),
                               "    volumes:", ("      - ./alloy/config.alloy:/etc/alloy/config.alloy:ro", AMBER, True),
                               ("      - ..:/log-corso:ro", AMBER, True), ("      - alloy-data:/var/lib/alloy/data", AMBER, True),
                               ("    restart: unless-stopped", ALLOY, True)], 23, 39, pad=28)
add("client-compose", [
    h("Il client: Alloy sul tuo PC", "logging/pc-studente/compose.yml"), c,
    t(1060, ys[3], "← il TUO nome", 30, PROM, True),
    t(1060, ys[6], "← avvia Alloy con", 26, INK2, True), t(1090, ys[7], "il suo file di configurazione", 26, INK2, True),
    t(1060, ys[10], "← pagina di Alloy, solo dal PC", 26, TEAL, True),
    t(1060, ys[12], "← la configurazione", 26, AMBER, True),
    t(1060, ys[13], "← i .log della lezione 2", 26, AMBER, True),
    t(1060, ys[14], "← dove è arrivato a leggere", 26, AMBER, True),
])

# 14 config.alloy
c, _, ys = code(70, 175, 1110, [('local.file_match "corso" {', ALLOY, True),
                                '  path_targets = [{"__path__" = "/log-corso/*.log", job = "corso"}]', "}", "",
                                ('loki.source.file "corso" {', TEAL, True), "  targets    = local.file_match.corso.targets",
                                "  forward_to = [loki.write.vps.receiver]", "}", "",
                                ('loki.write "vps" {', LOKI, True), "  endpoint {",
                                '    url = "http://its.fabersoft.net:3100/loki/api/v1/push"', "  }",
                                "  external_labels = { host = constants.hostname }", "}"], 23, 40, pad=28)
add("config-alloy", [
    h("Il client: config.alloy", "logging/pc-studente/alloy/config.alloy"), c,
    t(1220, ys[1], "1. trova i file", 34, ALLOY, True),
    t(1220, ys[5], "2. leggili", 34, TEAL, True),
    t(1220, ys[10], "3. spediscili", 34, LOKI, True), t(1220, ys[11] + 5, "a Loki, con", 28, INK2),
    t(1220, ys[12] + 10, "l'etichetta host", 28, INK2),
])

# 15 una riga
add("una-riga", [
    h("Una sola riga da cambiare", "In pc-studente/compose.yml"),
    code(70, 240, 1460, [("hostname: mario-rossi", PROM, True)], 48, pad=36)[0],
    arrow(800, 400, 800, 520, INK, 6), t(830, 475, "in Grafana diventa", 30, GREY),
    code(70, 540, 1460, [('{host="mario-rossi"}', LOKI, True)], 48, pad=36)[0],
    note(810, "Nome e cognome, minuscolo, con il trattino. Due studenti, due nomi diversi.", 30, INK2, False),
])

# 16 avvio client
add("avvio-client", [
    h("Il client: avvio e verifica", "Sul tuo PC"),
    step(1, 280, "cd its-jesi-lessons/logging/pc-studente", size=30, color=ALLOY),
    step(2, 390, "docker compose up -d", size=30, color=ALLOY),
    step(3, 500, "docker compose logs -f alloy", "errori?", size=30, color=ALLOY),
    step(4, 610, "http://localhost:12345", "tutto verde?", size=30, color=ALLOY),
    note(760, "Se docker compose up resta fermo a scaricare: l'immagine si scarica da casa.", 28, INK2, False),
])

# 17 explore
add("grafana-explore", [
    h("Grafana: Explore", "http://its.fabersoft.net:3000"),
    step(1, 290, "Menu → Explore", mono=False, color=GRAFANA),
    step(2, 400, "Sorgente dati: Loki", mono=False, color=GRAFANA),
    step(3, 510, '{host="mario-rossi"}', "il tuo nome", color=GRAFANA),
    step(4, 620, "Run query", mono=False, color=GRAFANA),
    note(760, "Le righe di sshd_classic.log, apache_access.log e mail.log: le stesse della lezione 2.", 28, INK2, False),
])

# 18 logql è grep
add("logql-grep", [
    h("LogQL è il vostro grep", "A sinistra la lezione 2, a destra Grafana"),
    t(70, 250, "Shell", 30, GREY, True), t(820, 250, "Grafana (LogQL)", 30, GREY, True),
    code(70, 280, 700, ['grep "Failed password" \\', "  sshd_classic.log"], 24)[0],
    code(820, 280, 710, ['{filename="/log-corso/sshd_classic.log"}', ('  |= "Failed password"', LOKI, True)], 24)[0],
    code(70, 500, 700, ['grep -v "Accepted" \\', "  sshd_classic.log"], 24)[0],
    code(820, 500, 710, ['{filename="/log-corso/sshd_classic.log"}', ('  != "Accepted"', LOKI, True)], 24)[0],
    note(770, "|= tiene le righe che contengono il testo, != le toglie.", 32, INK, True),
])

# 19 stesso numero
add("stesso-numero", [
    h("Stesso numero", "Quante righe parlano dell'IP 45.9.14.207?"),
    code(70, 220, 1460, ["$ cat *.log | grep -c 45.9.14.207", ("79", ALLOY, True)], 30, dark=True)[0],
    code(70, 480, 1460, ['sum(count_over_time({host="mario-rossi"} |= "45.9.14.207" [1h]))', ("79", ALLOY, True)], 28)[0],
    note(790, "Stessi log, stessa domanda, stessa risposta: ma ora sono tutti in un posto.", 30, INK2, False),
])

# 20 tutta la classe
rows = ""
for i, (n, v) in enumerate([("anna-bianchi", "282"), ("luca-verdi", "282"), ("mario-rossi", "282"), ("...", "")]):
    y = 470 + i * 70
    rows += t(150, y, n, 30, INK, False, mono=True) + t(900, y, v, 30, LOKI, True, "end", mono=True)
add("tutta-la-classe", [
    h("Tutta la classe in un posto", "Una sola domanda, una riga per ogni studente"),
    code(70, 200, 1460, ['sum by (host) (count_over_time({job="corso"} [1h]))'], 30)[0],
    rect(110, 410, 830, 320, "#FFFFFF", INK2, 2), rows,
    t(1000, 520, "Questo vuol dire", 34, INK, True), t(1000, 575, "centralizzato.", 34, INK, True),
    t(1000, 680, "282 = le righe dei 4 file", 26, INK2),
])

# 21 non arrivano
add("non-arrivano", [
    h("I log non arrivano?", "Un livello alla volta, come nella lezione 1"),
    step(1, 280, "nc -zv its.fabersoft.net 3100", "livello 4: la porta risponde?", size=30, note_x=1530),
    step(2, 390, "curl http://its.fabersoft.net:3100/ready", "livello 7", size=30),
    step(3, 500, "docker compose ps", "Alloy gira?", size=30),
    step(4, 610, "docker compose logs alloy", "cosa dice?", size=30),
    note(760, "Gli errori di Alloy dicono quasi sempre cosa non va: URL, porta o una virgola.", 28, INK2, False),
])

# 22 prima di uscire
add("prima-di-uscire", [
    t(100, 110, "Prima di uscire", 56, INK, True),
    step(1, 220, "Cosa fa docker compose up -d?", x=130, size=34, mono=False),
    step(2, 315, "Perché è il PC a spedire i log al VPS?", x=130, size=34, mono=False),
    step(3, 410, "Come vedo in Grafana i log di un compagno?", x=130, size=34, mono=False),
    rect(100, 560, 1430, 220, "#FFFFFF"),
    t(140, 625, "Per la lezione 5", 32, INK, True),
    t(140, 680, "Lasciate la cartella pc-studente com'è:", 30, INK2),
    t(140, 730, "ad Alloy aggiungiamo le metriche del PC.", 30, INK2),
], side=True)

# Slide prese dal Bignami
from bignami import B


def dopo(nome, *nuove):
    i = [n for n, _ in S].index(nome)
    S[i + 1:i + 1] = [(n, B[n]) for n in nuove]

B["log-locali"] = B["log-locali"].replace("Quattro posti da conoscere",
    "Quattro posti. I log vanno conservati a norma di legge, anche fuori dalla macchina")
dopo("run-o-up", "log-locali", "architetture-log")
dopo("tutta-la-classe", "buste", "url", "http")
dopo("non-arrivano", "livelli-strumenti")

save(sys.argv[1], S)
