import sys
from lib import *
from xml.sax.saxutils import escape
from quadro import quadro_completo

S = []
add = lambda name, body, side=False: S.append((name, page(body, side)))

OK = "#8CE99A"      # output dei comandi nel terminale scuro
COMM = "#9AA5B1"    # commenti nel terminale scuro


def section(name, part, word, sub, color):
    add(name, [
        t(165, 340, part if isinstance(part, str) else f"PARTE {part}", 30, color, True),
        rect(110, 380, 14, 200, color, rx=7),
        t(160, 480, word, 120, INK, True),
        sub if sub.startswith("<") else t(165, 550, sub, 36, GREY),
    ], side=True)


def card(x, y, w, hh, color, title, lines, size=28, cmd=None, cmdsize=22):
    out = rect(x, y, w, hh, "#FFFFFF", color, 3, 14)
    out += rect(x, y, 14, hh, color, rx=7)
    out += t(x + 40, y + 55, title, 36, color, True)
    yy = y + 105
    for ln in lines:
        out += t(x + 40, yy, ln, size, INK)
        yy += int(size * 1.45)
    if cmd:
        c, _, _ = code(x + 30, y + hh - 80, w - 60, [cmd], cmdsize, dark=True, pad=17)
        out += c
    return out


def grid_table(cols, rows, y0, rh, size=22, hl=None):
    """cols: [(x, w, titolo)]; rows: [(nome, sottotitolo, colore, [celle: lista di righe])]"""
    out = [t(x + 18, y0 - 14, title, 22, GREY, True) for x, w, title in cols[1:]]
    for r, (name, sub, c, cells) in enumerate(rows):
        y = y0 + r * (rh + 10)
        x0, w0, _ = cols[0]
        out.append(rect(x0, y, cols[-1][0] + cols[-1][1] - x0, rh, LIGHT.get(c, "#FFFFFF") if r == hl else "#FFFFFF",
                        c, 4 if r == hl else 2, 12))
        out.append(rect(x0, y, w0, rh, c, rx=12))
        out.append(t(x0 + w0 / 2, y + rh / 2 + (0 if sub else 10), name, 28, "#FFFFFF", True, "middle"))
        if sub:
            out.append(t(x0 + w0 / 2, y + rh / 2 + 34, sub, 17, "#FFFFFF", anchor="middle"))
        for (x, w, _), lines in zip(cols[1:], cells):
            for k, ln in enumerate(lines):
                yy = y + rh / 2 + size * 0.36 - (len(lines) - 1) * size * 0.65 + k * size * 1.3
                out.append(t(x + 18, yy, ln, size, INK))
    return out


# 0 titolo
art = "".join(rect(1060, 490 + i * 130, 110, 110, c, rx=16) + t(1115, 568 + i * 130, l, 58, "#FFFFFF", True, "middle") +
              t(1200, 558 + i * 130, w, 34, c, True)
              for i, (l, w, c) in enumerate([("L", "Logging", LOKI), ("M", "Monitoring", PROM), ("T", "Troubleshooting", GRAFANA)]))
S.append(("titolo", page([
    t(110, 230, "LMT", 30, DOCKER, True),
    t(110, 330, "Logging, Monitoring,", 84, INK, True),
    t(110, 430, "Troubleshooting", 84, INK, True),
    rect(114, 470, 180, 10, DOCKER, rx=5),
    t(110, 570, "BIGNAMI", 60, NAVY, True),
    t(110, 625, "Tutto il corso, ridotto all'osso", 30, GREY),
    t(110, 760, "ITS CyberSecurity - Jesi (AN) 2026/2027", 30, INK),
    t(110, 820, "prof. Luca Ferroni", 30, NAVY, True),
    art,
], side=True)))

# 1 scopi
rows = [("Logging", LOKI, "registra gli eventi in modo immutabile:", "si aggiunge in coda, non si riscrive il passato"),
        ("Monitoring", PROM, "registra le metriche: numeri nel tempo", "(CPU, memoria, disco, richieste al secondo)"),
        ("Troubleshooting", GRAFANA, "cerca la causa radice (root cause) di un problema", "usando i log e le metriche")]
body = [h("A cosa serve ognuno")]
for i, (name, c, l1, l2) in enumerate(rows):
    y = 200 + i * 190
    body += [pill(70, y + 20, 380, name, c, 34, 100), t(500, y + 60, l1, 32, INK, True), t(500, y + 108, l2, 30, INK2)]
body.append(note(835, "I log sono davvero immutabili solo se escono dalla macchina: per questo si spediscono a Loki.", 27, GREY, False))
add("scopi", body)

# observability
eq = []
for i, (w, c) in enumerate([("Logging", LOKI), ("Monitoring", PROM), ("Troubleshooting", GRAFANA)]):
    x = [70, 410, 790][i]
    ww = [280, 320, 400][i]
    eq.append(pill(x, 200, ww, w, c, 32, 80))
    if i < 2:
        eq.append(t(x + ww + 25, 255, "+", 48, INK, True, "middle"))
eq += [t(1225, 255, "=", 48, INK, True, "middle"), pill(1260, 200, 270, "Observability", PURPLE, 32, 80)]
add("observability", [
    h("OBSERVABILITY"), *eq,
    t(70, 380, "Capire cosa succede dentro un sistema guardando quello che produce:", 32, INK, True),
    t(70, 425, "log ed eventi, metriche (e, nelle architetture più grandi, le tracce).", 30, INK2),
    bullets(100, 530, ["sapere in ogni momento cosa succede nella rete e nei servizi",
                       "correlare: stesso istante, stesso host, log e metriche affiancati in Grafana",
                       "arrivare alla root cause di un guasto in tempi rapidi"], 32, 70, INK, PURPLE),
    note(820, "Il monitoring ti dice che qualcosa non va; l'observability ti aiuta a capire perché.", 30, PURPLE, True),
])

# 2 sezione logging
section("sez-logging", 1, "LOGGING", f'<text x="165" y="550" font-size="36" fill="{GREY}">Registrare gli eventi e conservarli '
        f'<tspan font-weight="bold" fill="{INK}">a norma di legge</tspan></text>\n', LOKI)

# 3 dove finiscono i log sulla macchina
add("log-locali", [
    h("Dove finiscono i log sulla macchina", "Quattro posti da conoscere"),
    card(70, 190, 715, 320, LOKI, "systemd-journald", ["binario, si legge solo con journalctl", "è il default delle distribuzioni recenti"],
         cmd="$ journalctl -u ssh -f"),
    card(815, 190, 715, 320, TEAL, "syslog (rsyslog)", ["testo, in /var/log/syslog e /var/log/auth.log", "si legge con cat, grep, tail"],
         cmd="$ tail -f /var/log/auth.log"),
    card(70, 540, 715, 320, AMBER, "file dell'applicazione", ["in /var/log o dove decide l'applicazione", "es. Apache, Nginx, Postfix"],
         cmd="$ tail -f /var/log/apache2/access.log"),
    card(815, 540, 715, 320, DOCKER, "log di Docker", ["stdout e stderr del container", "2>&1 per passarli entrambi a grep"],
         cmd="$ docker logs -f grafana 2>&1 | grep -i error", cmdsize=20),
])

# N3 architetture per centralizzare i log
add("architetture-log", [
    h("Come si centralizzano i log", "Quattro architetture: nel corso usiamo Loki"),
    *grid_table([(70, 240, ""), (330, 340, "raccolta"), (690, 240, "storage"), (950, 220, "visualizzazione"), (1190, 340, "nota")],
                [("syslog", None, TEAL, [["inoltro al server rsyslog", "UDP/TCP 514, TLS 6514"], ["file di testo"], ["grep, tail"],
                                               ["la più semplice:", "c'è già ovunque"]]),
                 ("ELK", "Elastic Stack", AMBER, [["Beats o Logstash"], ["Elasticsearch,", "indice full-text"], ["Kibana"],
                                                                  ["ricerche potenti, ma", "pesante in RAM e disco"]]),
                 ("Graylog", None, PURPLE, [["GELF, syslog, Beats"], ["OpenSearch", "(più MongoDB)"], ["web di Graylog"],
                                            ["pronto all'uso, con", "stream e allarmi"]]),
                 ("Loki", "nel corso", LOKI, [["Alloy"], ["indicizza solo", "le etichette"], ["Grafana"],
                                             ["leggero: per questo", "lo usiamo"]])],
                235, 140, hl=3),
])

# 4 un file di log e tre one-liner
log, yb, _ = code(70, 180, 1460, [
    "Sep  7 18:43:41 srv sshd[5319]: Failed password for pippo from 10.0.0.7 port 47004 ssh2",
    "Sep  8 03:11:00 srv sshd[7438]: Failed password for invalid user admin from 185.22.1.9 port 46374 ssh2",
    "Sep 28 02:49:02 srv sshd[2208]: Accepted password for deploy from 45.9.14.207 port 42216 ssh2"], 22, 38, pad=26)
term, _, _ = code(70, yb + 30, 1460, [
    ("$ grep -c 'Failed password' sshd_classic.log", "#FFFFFF", True),
    ("49", OK),
    ("$ grep 'Failed password' sshd_classic.log | grep -o 'from [0-9.]*' | sort | uniq -c | sort -rn | head -3", "#FFFFFF", True),
    ("     36 from 45.9.14.207", OK), ("     10 from 185.22.1.9", OK), ("      3 from 10.0.0.7", OK),
    ("$ grep Accepted sshd_classic.log | grep 45.9.14.207", "#FFFFFF", True),
    ("Sep 28 02:49:02 srv sshd[2208]: Accepted password for deploy from 45.9.14.207 ...", OK)], 22, 40, dark=True, pad=26)
add("file-e-oneliner", [
    h("Un file di log e tre righe di shell", "logging/sshd_classic.log dal repository del corso"),
    log, term,
    note(830, "36 password sbagliate e poi un accesso riuscito: il brute force è andato a segno.", 30, PROM, True),
])

# 5 fail2ban
jail, _, _ = code(70, 450, 640, ["# /etc/fail2ban/jail.local", ("[sshd]", INK, True), "enabled  = true",
                                  ("maxretry = 5", AMBER, True), ("findtime = 10m", AMBER, True), ("bantime  = 1h", PROM, True)], 26, 44)
stat, _, _ = code(760, 450, 770, [("$ sudo fail2ban-client status sshd", "#FFFFFF", True),
                                   ("   |- Currently banned: 1", OK), ("   `- Banned IP list: 45.9.14.207", OK)], 24, 42, dark=True)
add("fail2ban", [
    h("fail2ban: dal log all'azione", "Legge i log e banna chi sbaglia troppe volte"),
    box(70, 200, 400, 150, LOKI, "log di sshd", 32, "auth.log o journal"),
    arrow(475, 275, 560, 275, INK, 5),
    box(570, 200, 400, 150, AMBER, "fail2ban", 36, "5 errori in 10 minuti?"),
    arrow(975, 275, 1060, 275, INK, 5),
    box(1070, 200, 460, 150, PROM, "firewall", 36, "DROP dell'IP per 1 ora"),
    jail, stat,
    t(760, 700, "Nel nostro log il brute force parte con 8 errori di fila:", 26, INK),
    t(760, 742, "sarebbe stato bannato prima dell'accesso riuscito.", 26, INK, True),
    note(840, "Lezione 2: \"fail2ban\" era il nome finto del miner. Controllate sempre il percorso del programma.", 26, GREY, False),
])

# 6 iptables -j LOG
cmds, yb, _ = code(70, 190, 1460, [
    ("$ sudo iptables -I INPUT -p tcp --dport 22 -j LOG --log-prefix \"SSH-IN: \"", "#FFFFFF", True),
    ("$ sudo journalctl -k -f | grep SSH-IN", "#FFFFFF", True),
    ("Oct 28 10:15:02 srv kernel: SSH-IN: IN=eth0 OUT= SRC=45.9.14.207 DST=203.0.113.10", OK),
    ("    ... PROTO=TCP SPT=42216 DPT=22 SYN", OK)], 23, 40, dark=True, pad=30)
add("iptables-log", [
    h("Il firewall che scrive nel log", "iptables -j LOG: ogni pacchetto che corrisponde finisce nel log del kernel"),
    cmds,
    bullets(100, yb + 80, ["SRC e DST sono il livello 3, SPT e DPT il livello 4",
                           "-j LOG non blocca: scrive e passa alla regola successiva",
                           "-I la mette in cima, prima delle regole che accettano o scartano",
                           "Sui sistemi recenti c'è nftables: stessa idea, sintassi diversa"], 32, 72, INK, PROM),
])

# 7 sezione monitoring
section("sez-monitoring", 2, "MONITORING", "Misurare lo stato nel tempo", PROM)

# indicatori chiave
KPI = [("Apparati di rete", PURPLE, "router, switch, firewall",
        ["throughput", "errori sulle interfacce", "latenza", "CPU e RAM"], "di solito via SNMP, senza agent"),
       ("Server", ALLOY, "GNU/Linux, Windows",
        ["utilizzo CPU", "RAM", "I/O disco", "spazio disco", "processi attivi"], "con un agent (Alloy, node exporter)"),
       ("Servizi e applicazioni", GRAFANA, "web, database, API",
        ["uptime", "status code HTTP", "tempi di risposta", "porte aperte"], "controllati anche da fuori (curl, nc)")]
body = [h("Classificazione degli indicatori chiave", "Cosa misurare, a seconda di cosa si osserva")]
for i, (title, c, sub, items, how) in enumerate(KPI):
    x = 70 + i * 495
    body += [rect(x, 190, 470, 640, "#FFFFFF", c, 3, 16), rect(x, 190, 470, 120, c, rx=16), rect(x, 280, 470, 30, c, rx=0),
             t(x + 235, 245, title, 32, "#FFFFFF", True, "middle"), t(x + 235, 290, sub, 24, "#FFFFFF", anchor="middle")]
    body.append(bullets(x + 45, 390, items, 32, 75, INK, c))
    body.append(t(x + 235, 800, how, 22, GREY, anchor="middle", italic=True))
add("indicatori-chiave", body)

# 8 agent, push, retention
cols = [("Agent o agentless", ALLOY, [("agent", "un programma sulla macchina"), ("", "(Alloy, node exporter)"),
                                       ("agentless", "si osserva da fuori"), ("", "(SNMP, ping)")]),
        ("Push o pull", DOCKER, [("push", "l'agent spedisce al server:"), ("", "va bene dietro un router"),
                                 ("pull", "il server va a prendere:"), ("", "deve raggiungere la macchina")]),
        ("Retention", AMBER, [("cos'è", "per quanto tempo tengo i dati"), ("", "prima di cancellarli"),
                              ("costo", "più giorni = più disco"), ("", "es. 15 giorni, 1 mese")])]
body = [h("Le tre scelte del monitoraggio")]
for i, (title, c, items) in enumerate(cols):
    x = 70 + i * 495
    body += [rect(x, 190, 470, 480, "#FFFFFF", c, 3, 16), rect(x, 190, 470, 90, c, rx=16), rect(x, 250, 470, 30, c, rx=0),
             t(x + 235, 250, title, 34, "#FFFFFF", True, "middle")]
    yy = 350
    for k, v in items:
        if k:
            body.append(t(x + 35, yy, k, 30, c, True))
            yy += 45
        body.append(t(x + 35, yy, v, 27, INK))
        yy += 60 if not k else 45
body.append(note(770, "Nel corso: agent (Alloy) che fa push, perché i PC hanno IP privati.", 30, INK, True))
add("agent-push-retention", body)

# 9 SNMP
tab = [("", "v1 / v2c", "v3"),
       ("accesso", "community (es. public)", "utente e password"),
       ("cifratura", "nessuna: tutto in chiaro", "sì (livello authPriv)"),
       ("quando", "rete fidata, sola lettura", "sempre, se l'apparato lo supporta")]
body = [h("SNMP per gli apparati di rete", "Switch, router, stampanti, UPS: niente da installare. UDP 161 (domande) e 162 (trap)")]
for r, row in enumerate(tab):
    y = 200 + r * 85
    for ci, cell in enumerate(row):
        x = [70, 330, 930][ci]
        w = [250, 590, 600][ci]
        fill = INK if r == 0 else ("#FFFFFF" if r % 2 else "#EEF1F5")
        body.append(rect(x, y, w, 80, fill, rx=8))
        body.append(t(x + 25, y + 52, cell, 28, "#FFFFFF" if r == 0 else (GREY if ci == 0 else INK), r == 0 or ci == 0))
c1, _, _ = code(70, 570, 1460, [("$ snmpget -v2c -c public 192.168.1.1 1.3.6.1.2.1.1.3.0", "#FFFFFF", True)], 22, dark=True, pad=22)
c2, _, _ = code(70, 670, 1460, [("$ snmpget -v3 -l authPriv -u monitor -a SHA -A <pwd> -x AES -X <pwd> 192.168.1.1 1.3.6.1.2.1.1.3.0", "#FFFFFF", True)], 22, dark=True, pad=22)
body += [c1, c2, note(830, "La community di v1 e v2c viaggia in chiaro: chi la intercetta legge tutto.", 28, PROM, True)]
add("snmp-versioni", body)


# metriche, eventi, alerting
body = [h("Metriche, eventi e alerting")]
for i, (title, c, l1, ex) in enumerate([("Metrica", PROM, "un numero nel tempo", "CPU all'87% alle 10:15"),
                                        ("Evento", LOKI, "un fatto puntuale", "10:15:02 servizio riavviato"),
                                        ("Alert", GRAFANA, "una situazione anomala", "CPU oltre il 90% da 5 minuti")]):
    x = 70 + i * 495
    body += [rect(x, 150, 470, 150, "#FFFFFF", c, 3, 14), rect(x, 150, 12, 150, c, rx=6),
             t(x + 35, 197, title, 30, c, True), t(x + 35, 237, l1, 24, INK),
             t(x + 35, 277, ex, 22, INK2, mono=True)]
body += [t(70, 360, "Soglie (thresholds)", 30, AMBER, True),
         t(70, 400, "statica: un valore fisso, es. disco oltre il 90%", 23, INK),
         t(70, 434, "dinamica: rispetto al normale, es. il triplo del solito", 23, INK),
         rect(70, 460, 720, 330, "#FFFFFF", INK2, 3, 14),
         t(95, 500, "Isteresi: scatta sopra il 90%, rientra solo sotto l'80%", 22, INK, True),
         rect(300, 520, 310, 250, "#FFF5F5", rx=0), t(455, 545, "alert attivo", 20, PROM, True, "middle"),
         '<line x1="95" y1="590" x2="770" y2="590" stroke="#C92A2A" stroke-width="2.5" stroke-dasharray="10 7"/>\n',
         '<line x1="95" y1="660" x2="770" y2="660" stroke="#B7791F" stroke-width="2.5" stroke-dasharray="10 7"/>\n',
         t(770, 580, "90%", 20, PROM, True, "end"), t(770, 650, "80%", 20, AMBER, True, "end"),
         '<polyline points="100,750 170,735 240,690 300,590 340,565 380,620 420,575 460,630 500,585 545,640 610,660 670,715 765,735" '
         'fill="none" stroke="#1F2933" stroke-width="4" stroke-linejoin="round"/>\n',
         t(300, 765, "scatta", 20, PROM, True, "middle"), t(610, 765, "rientra", 20, AMBER, True, "middle"),
         t(70, 835, "Senza isteresi si accenderebbe e spegnerebbe a ogni oscillazione.", 22, INK2)]
body += [t(830, 360, "Severity", 30, PROM, True)]
for i, (lev, c, d) in enumerate([("Info", TEAL, "da registrare, nessuna azione"), ("Warning", AMBER, "da guardare prima che peggiori"),
                                 ("High", GRAFANA, "da risolvere presto"), ("Critical", PROM, "servizio fermo: subito")]):
    y = 385 + i * 70
    body += [pill(830, y, 170, lev, c, 24, 52), t(1025, y + 35, d, 24, INK)]
body += [rect(830, 680, 700, 165, "#FFF5F5", PROM, 3, 14),
         t(860, 725, "Alert fatigue", 28, PROM, True),
         t(860, 765, "troppi falsi positivi: nessuno legge più gli alert,", 23, INK),
         t(860, 798, "nemmeno quello vero.", 23, INK),
         t(860, 832, "Un alert solo se serve un'azione.", 23, INK, True)]
add("metriche-eventi-alerting", body)

# N1 il flusso
STEPS = [("Raccolta", "collection", ["prende i dati", "dove nascono"],
          ["rsyslog, Alloy,", "Beats"], ["exporter, Telegraf,", "agent Zabbix, SNMP"]),
         ("Parsing", "e normalizzazione", ["stesso formato e nomi:", "etichette, unità, orari"],
          ["Logstash,", "gli stage di Alloy"], ["etichette host e job,", "unità di misura"]),
         ("Storage", "con una retention", ["conserva i dati", "per un tempo deciso"],
          ["Loki,", "Elasticsearch"], ["Prometheus,", "InfluxDB"]),
         ("Visualizzazione", "e interrogazione", ["grafici, ricerche,", "dashboard"],
          ["Grafana,", "Kibana"], ["Grafana,", "Zabbix"])]
body = [h("Dalla sorgente al grafico", "Lo stesso flusso, per i log e per le metriche")]
for i, (title, sub, what, lg, mt) in enumerate(STEPS):
    x = 70 + i * 375
    body += [rect(x, 180, 335, 110, INK, rx=14), t(x + 167, 228, title, 30, "#FFFFFF", True, "middle"),
             t(x + 167, 266, sub, 22, "#CBD2D9", anchor="middle"),
             t(x + 20, 340, what[0], 23, INK2), t(x + 20, 372, what[1], 23, INK2)]
    if i < 3:
        body.append(arrow(x + 340, 235, x + 368, 235, INK, 5))
    for (y, c, lines) in [(430, LOKI, lg), (630, PROM, mt)]:
        body += [rect(x, y, 335, 140, LIGHT[c], c, 3, 12),
                 t(x + 20, y + 60, lines[0], 25, INK, True), t(x + 20, y + 98, lines[1], 25, INK, True)]
body += [t(70, 418, "LOG", 22, LOKI, True), t(70, 618, "METRICHE", 22, PROM, True),
         note(840, "L'alerting parte dallo storage: è una query che gira da sola, ogni pochi secondi.", 28, INK, True)]
add("flusso", body)

# N2 gli strumenti di monitoraggio
add("strumenti-monitoraggio", [
    h("Gli strumenti di monitoraggio più usati", "Nel corso usiamo Prometheus: è lo standard e si integra con Alloy e Grafana"),
    *grid_table([(70, 250, ""), (340, 400, "come raccoglie"), (760, 330, "dove salva"), (1110, 420, "in una riga")],
                [("Zabbix", None, PURPLE, [["agent proprio, e agentless:", "SNMP, IPMI, ping"], ["database relazionale", "(PostgreSQL, MySQL)"],
                                           ["tutto in uno: raccolta, web,", "trigger e allarmi"]]),
                 ("TIG", "Telegraf InfluxDB Grafana", TEAL, [["Telegraf: agent con molti", "plugin, in push"], ["InfluxDB, una TSDB"],
                                                             ["come il nostro stack,", "ma in push nativo"]]),
                 ("Prometheus", None, PROM, [["pull da /metrics degli", "exporter; push con remote write"], ["TSDB propria"],
                                             ["PromQL e Alertmanager;", "lo standard per i container"]]),
                 ("Netdata", None, ALLOY, [["agent su ogni macchina,", "una metrica al secondo"], ["sulla macchina stessa", "(o inoltra a un parent)"],
                                           ["zero configurazione,", "dashboard già pronta"]]),
                 ("PCP", "Performance Co-Pilot", AMBER, [["demone pmcd, un agent", "per sottosistema"], ["archivi di pmlogger"],
                                                        ["analisi delle prestazioni,", "anche a posteriori"]])],
                215, 118, size=21, hl=2),
])


# 10 Prometheus
pq, _, ys = code(70, 610, 1460, [
    ("up", "#FFFFFF", True), ("node_load1", "#FFFFFF", True),
    ('100 - avg by (host) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100', "#FFFFFF", True)], 22, 40, dark=True, pad=24)
add("prometheus", [
    h("Prometheus", "Un database a serie temporali (TSDB) che si interroga con PromQL"),
    box(70, 200, 380, 110, ALLOY, "node exporter", 30, ":9100  metriche della macchina", 22),
    box(70, 340, 380, 110, TEAL, "postgres exporter", 30, ":9187  metriche del database", 22),
    box(70, 480, 380, 90, ALLOY, "Alloy", 30, "node exporter incluso", 22),
    arrow(455, 255, 640, 330, PROM, 4, both=False), arrow(455, 395, 640, 375, PROM, 4),
    t(500, 250, "pull", 24, PROM, True),
    arrow(455, 525, 640, 420, ALLOY, 4, "10 7"), t(545, 530, "push", 24, ALLOY, True),
    box(650, 280, 420, 180, PROM, "Prometheus", 38, "TSDB, retention 15 giorni", 24),
    arrow(1075, 370, 1150, 370, GREY, 3, "7 6"),
    box(1160, 300, 370, 140, GRAFANA, "Grafana", 36, "grafici con PromQL", 24),
    pq,
    t(1500, ys[0], "1 se il target risponde", 24, COMM, anchor="end"),
    t(1500, ys[1], "carico medio dell'ultimo minuto", 24, COMM, anchor="end"),
    t(1500, ys[2], "CPU usata in %, per host", 24, COMM, anchor="end"),
])

# 11 sezione deploy
section("sez-deploy", 3, "COME DEPLOYARE", "Un'architettura di rete per log e metriche", DOCKER)

# 12 il quadro completo
add("quadro-completo", quadro_completo())

# 13 Alloy
add("alloy", [
    h("Alloy: il demone sul PC", "Un solo programma, client di Loki e di Prometheus"),
    rect(50, 190, 930, 600, "none", INK2, 3, 18, "10 8"), t(80, 235, "il tuo PC", 28, GREY, True),
    box(90, 270, 400, 130, LOKI, "file di log", 30, "loki.source.file", 22),
    box(90, 430, 400, 130, LOKI, "journal", 30, "loki.source.journal", 22),
    box(90, 590, 400, 130, PROM, "metriche del PC", 30, "prometheus.exporter.unix", 22),
    box(600, 390, 330, 210, ALLOY, "Alloy", 48, "demone", 26),
    arrow(495, 335, 595, 450, LOKI, 4), arrow(495, 495, 595, 495, LOKI, 4), arrow(495, 655, 595, 545, PROM, 4),
    box(1110, 300, 420, 140, LOKI, "Loki :3100", 34, "loki.write", 22),
    box(1110, 560, 420, 140, PROM, "Prometheus :9090", 34, "prometheus.remote_write", 22),
    arrow(935, 450, 1100, 380, LOKI, 5), arrow(935, 540, 1100, 620, PROM, 5),
    note(850, "Gira sempre: come servizio systemd, o in un container con restart: unless-stopped.", 28, INK, True),
])

# 14 docker run
c, yb, _ = code(70, 200, 1460, [
    ("$ docker run -d --name grafana -p 3000:3000 grafana/grafana", "#FFFFFF", True),
    ("$ docker ps", "#FFFFFF", True),
    ("$ docker logs -f grafana 2>&1", "#FFFFFF", True)], 32, 60, dark=True, pad=36)
add("docker-run", [
    h("Docker: un servizio in una riga", "Immagine dal registry, container che gira, porte e log"),
    c,
    step("-d", yb + 110, "gira in background", x=130, size=32, mono=False, color=DOCKER),
    step("-p", yb + 220, "porta del PC : porta del container", x=130, size=32, mono=False, color=TEAL),
    step("2>", yb + 330, "anche lo stderr, così grep vede gli errori", x=130, size=32, mono=False, color=AMBER),
])

# 15 docker compose: tre comandi
add("compose-comandi", [
    h("Docker Compose: più container insieme", "Si lancia nella cartella che contiene compose.yml"),
    step(1, 310, "docker compose up -d", None, size=38, color=ALLOY),
    t(165, 365, "crea e avvia tutti i servizi del file", 30, INK2),
    step(2, 490, "docker compose down", None, size=38, color=DOCKER),
    t(165, 545, "ferma e cancella i container: i volumi con i dati restano", 30, INK2),
    step(3, 670, "docker compose down -v", None, size=38, color=PROM),
    t(165, 725, "cancella anche i volumi: i dati sono persi", 30, PROM, True),
    note(840, "Come con docker: docker compose ps e docker compose logs -f <servizio>.", 28, GREY, False),
])

# 16 da docker run a compose.yml
run, yb, _ = code(70, 190, 1460, [("$ docker run -d --name grafana -p 3000:3000 grafana/grafana", "#FFFFFF", True)], 30, dark=True, pad=30)
yml, _, ys = code(70, yb + 90, 900, ["services:", ("  grafana:", GRAFANA, True), ("    image: grafana/grafana", DOCKER, True),
                                      "    ports:", ('      - "3000:3000"', TEAL, True), ("    restart: unless-stopped", ALLOY, True)], 30, 54)
add("da-run-a-compose", [
    h("Da docker run a compose.yml", "La stessa riga, scritta in un file"),
    run, arrow(520, yb + 8, 520, yb + 80, INK, 5),
    yml,
    t(1010, ys[1], "← --name", 30, GRAFANA, True), t(1010, ys[2], "← l'immagine", 30, DOCKER, True),
    t(1010, ys[4], "← -p", 30, TEAL, True), t(1010, ys[5], "← in più: riparte da solo,", 30, ALLOY, True),
    t(1060, ys[5] + 42, "anche dopo un riavvio", 30, ALLOY, True),
])

# 17 compose.yml del server
P = ("    ports: [", TEAL, True)
left = ["services:", ("  loki:", LOKI, True), "    image: grafana/loki:3.7.0", "    command: -config.file=/etc/loki/config.yml",
        "    volumes:", "      - ./loki/config.yml:/etc/loki/config.yml:ro", "      - loki-data:/loki",
        ('    ports: ["3100:3100"]', TEAL, True), ("    restart: unless-stopped", ALLOY, True),
        ("  grafana:", GRAFANA, True), "    image: grafana/grafana:13.2.4", "    volumes:", "      - grafana-data:/var/lib/grafana",
        ('    ports: ["3000:3000"]', TEAL, True), ("    restart: unless-stopped", ALLOY, True)]
right = [("  prometheus:", PROM, True), "    image: prom/prometheus:v3.15.0", "    command:",
         "      - --config.file=/etc/prometheus/prometheus.yml", "      - --storage.tsdb.path=/prometheus",
         ("      - --storage.tsdb.retention.time=15d", AMBER, True), ("      - --web.enable-remote-write-receiver", PROM, True),
         "    volumes:", "      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro", "      - prometheus-data:/prometheus",
         ('    ports: ["9090:9090"]', TEAL, True), ("    restart: unless-stopped", ALLOY, True),
         "volumes:", "  loki-data:", "  grafana-data:", "  prometheus-data:"]
cl, _, _ = code(70, 175, 600, left, 18, 31, pad=24)
cr, _, _ = code(690, 175, 840, right, 18, 31, pad=24)
add("compose-server", [
    h("compose.yml del server", "Loki, Grafana e Prometheus sul VPS, nello stesso file (continua a destra)"),
    cl, cr,
    t(70, 788, "Porte esportate:", 28, INK, True),
    pill(340, 750, 220, ":3000 Grafana", GRAFANA, 24, 56), pill(580, 750, 190, ":3100 Loki", LOKI, 24, 56),
    pill(790, 750, 270, ":9090 Prometheus", PROM, 24, 56),
    t(1090, 788, "retention 15 giorni, accetta il push", 24, INK2),
])

# 18 compose.yml del client
cc, _, ys = code(70, 175, 820, ["services:", ("  alloy:", ALLOY, True), "    image: grafana/alloy:v1.20.1",
                                 ("    hostname: mario-rossi", AMBER, True), "    command:", "      - run",
                                 "      - --server.http.listen-addr=0.0.0.0:12345", "      - --storage.path=/var/lib/alloy/data",
                                 "      - /etc/alloy/config.alloy", "    volumes:", "      - ./alloy/config.alloy:/etc/alloy/config.alloy:ro",
                                 ("      - /var/log:/var/log:ro", LOKI, True), ("      - /proc:/host/proc:ro", PROM, True),
                                 ("      - /sys:/host/sys:ro", PROM, True), "      - alloy-data:/var/lib/alloy/data",
                                 ('    ports: ["127.0.0.1:12345:12345"]', TEAL, True), ("    restart: unless-stopped", ALLOY, True),
                                 "volumes:", "  alloy-data:"], 19, 33, pad=24)
add("compose-client", [
    h("compose.yml del PC", "Alloy, che spedisce a Loki e a Prometheus"),
    cc,
    t(930, ys[3], "← diventa l'etichetta host", 26, AMBER, True),
    t(930, ys[8], "← config.alloy dice dove", 26, INK2, True),
    t(960, ys[8] + 36, "spedire log e metriche", 26, INK2, True),
    t(930, ys[11], "← i log da leggere", 26, LOKI, True),
    t(930, (ys[12] + ys[13]) / 2, "← le metriche del PC", 26, PROM, True),
    t(930, ys[15], "← solo la pagina di stato,", 26, TEAL, True),
    t(960, ys[15] + 36, "visibile solo dal PC", 26, TEAL, True),
    t(930, ys[16] + 70, "Nessuna porta in ingresso:", 26, INK, True),
    t(930, ys[16] + 106, "è Alloy che apre la connessione.", 26, INK),

])

# 19 disco e retention
m, _, _ = code(70, 250, 700, [("$ df -h /", "#FFFFFF", True), ("$ docker system df", "#FFFFFF", True),
                               ("$ sudo du -sh /var/lib/docker/volumes/*", "#FFFFFF", True), ("$ journalctl --disk-usage", "#FFFFFF", True)],
                  23, 52, dark=True, pad=30)
l, _, _ = code(820, 250, 710, [("# Prometheus (compose.yml)", COMM), "--storage.tsdb.retention.time=15d", "",
                                ("# Loki (config.yml)", COMM), "limits_config:", "  retention_period: 744h",
                                "compactor:", "  retention_enabled: true", "  delete_request_store: filesystem", "",
                                ("# journald (/etc/systemd/journald.conf)", COMM), "SystemMaxUse=500M"], 20, 31, pad=26)
add("disco-retention", [
    h("Tenere d'occhio il disco", "Log e metriche crescono ogni giorno"),
    t(70, 225, "Misurare", 32, DOCKER, True), m,
    t(820, 225, "Limitare (retention)", 32, AMBER, True), l,
    t(70, 600, "Retention giusta =", 30, INK, True),
    t(70, 645, "quanto indietro devo poter guardare", 28, INK),
    t(70, 690, "e quanto disco ho a disposizione.", 28, INK),
    note(850, "Disco pieno: Loki e Prometheus smettono di scrivere, e si perdono proprio i dati del guasto.", 27, PROM, True),
])

# 20 sezione troubleshooting
section("sez-troubleshooting", 4, "TROUBLESHOOTING", "Trovare la causa, usando log e metriche", GRAFANA)

# 21 strumenti per livello
grid = [("", "dal client", "sul server"),
        ("7  applicazione", "curl -I http://host:3000", "docker compose logs -f grafana\njournalctl -u nome-servizio"),
        ("4  porta", "nc -zv host 3000", "sudo ss -lptn | grep 3000\nsudo tcpdump -ni any port 3000"),
        ("3  IP", "ping -c 3 host", "ip a\nsudo tcpdump -ni any icmp")]
colors = [None, "#C2255C", "#0C8599", "#6741D9"]
body = [h("Strumenti per livello", "Dal client si sale da 3 a 7; sul server si guarda chi ascolta e cosa dice")]
for r, row in enumerate(grid):
    y = 180 + (0 if r == 0 else 70 + (r - 1) * 200)
    hh = 60 if r == 0 else 185
    for ci, cell in enumerate(row):
        x = [70, 420, 960][ci]
        w = [330, 520, 570][ci]
        if r == 0:
            body.append(t(x + 20, y + 42, cell, 30, GREY, True))
            continue
        if ci == 0:
            body.append(rect(x, y, w, hh, colors[r], rx=12))
            body.append(t(x + 30, y + hh / 2 + 12, cell, 32, "#FFFFFF", True))
        else:
            body.append(rect(x, y, w, hh, "#FFFFFF", colors[r], 3, 12))
            ls = cell.split("\n")
            for k, ln in enumerate(ls):
                yy = y + hh / 2 + 9 - (len(ls) - 1) * 24 + k * 48
                body.append(t(x + 25, yy, ln, 26, INK, True, mono=True))
add("livelli-strumenti", body)

# APPENDICE
section("sez-appendice", "APPENDICE", "RETE E WEB", "Buste, URL e HTTP", PURPLE)


def envelope(x, y, w, hh, color, fill, label):
    out = rect(x, y, w, hh, fill, color, 4, 12)
    out += f'<path d="M{x},{y + 8} L{x + w / 2},{y + 60} L{x + w},{y + 8}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0.5"/>\n'
    out += pill(x + 20, y - 22, len(label) * 15 + 40, label, color, 22, 44)
    return out


def field(x, y, k, v, color):
    return t(x, y, k, 20, GREY) + t(x, y + 34, v, 28, color, True, mono=True)


def who(y, color, title, lines, tool):
    out = rect(1060, y, 10, 150, color, rx=4) + t(1090, y + 28, title, 26, color, True)
    for i, ln in enumerate(lines):
        out += t(1090, y + 66 + i * 32, ln, 22, INK2)
    return out + t(1530, y + 28, tool, 22, color, True, "end", mono=True)


add("buste", [
    h("Incapsulamento: tre buste", "Il browser chiede una pagina a Grafana sul VPS"),
    envelope(70, 200, 930, 660, PURPLE, "#F3F0FF", "LIVELLO 3 · busta IP"),
    field(110, 290, "mittente", "IP del PC", PURPLE), field(560, 290, "destinatario", "IP del VPS", PURPLE),
    envelope(120, 390, 830, 440, TEAL, "#E3FAFC", "LIVELLO 4 · busta della porta"),
    field(160, 470, "porta mittente (a caso)", "50432", TEAL), field(560, 470, "porta destinatario", "3000", TEAL),
    '<path d="M170,580 L860,580 L900,620 L900,800 L170,800 Z" fill="#FFFFFF" stroke="#C2255C" stroke-width="4"/>\n'
    '<path d="M860,580 L860,620 L900,620" fill="#FFF0F6" stroke="#C2255C" stroke-width="3"/>\n',
    pill(190, 558, 420, "LIVELLO 7 · il messaggio HTTP", PINK, 22, 44),
    t(210, 650, "GET / HTTP/1.1", 26, INK, mono=True),
    t(210, 692, "Host: its.fabersoft.net:3000", 26, INK, mono=True),
    t(210, 734, "User-Agent: Firefox", 26, INK, mono=True),
    t(1060, 225, "Chi apre quale busta", 30, INK, True),
    who(270, PURPLE, "3 · indirizzo IP", ["I router lungo Internet:", "portano il pacchetto al VPS."], "ping"),
    who(475, TEAL, "4 · porta", ["Il sistema operativo del VPS:", "consegna al programma in ascolto."], "nc -zv"),
    who(680, PINK, "7 · messaggio", ["Solo il programma, qui Grafana:", "legge la richiesta e risponde."], "curl"),
])

# URL
SEG = [("https", PINK, "proto"), ("://", None, None), ("it.wikipedia.org", PURPLE, "fqdn"), (":", None, None),
       ("443", TEAL, "port"), ("/", None, None), ("wiki/Uniform_Resource_Locator", NAVY, "path"), ("?", None, None),
       ("uselang=it", AMBER, "querystring"), ("#", None, None), ("cite_note-2", ALLOY, "anchor")]
FS, X0, YU = 28, 115, 280
CW = FS * 0.602
body = [h("Uniform Resource Locator (URL)", "Fonte: it.wikipedia.org/wiki/Uniform_Resource_Locator"),
        rect(70, 185, 1460, 225, "#FFFFFF", INK2, 3, 14)]
x, spans = X0, ""
for txt, c, lab in SEG:
    w = len(txt) * CW
    if c is None:
        body.append(rect(x - 2, YU - 30, w + 4, 42, "#FFE066", rx=5))
        spans += f'<tspan fill="{INK}" font-weight="bold">{escape(txt)}</tspan>'
    else:
        spans += f'<tspan fill="{c}" font-weight="bold">{escape(txt)}</tspan>'
        body.append(f'<path d="M{x + 2},{YU + 24} L{x + 2},{YU + 36} L{x + w - 2},{YU + 36} L{x + w - 2},{YU + 24}" fill="none" stroke="{c}" stroke-width="3"/>\n')
        body.append(t(x + w / 2, YU + 76, f"<{lab}>", 24, c, True, "middle", mono=True))
    x += w
body.append(f'<text xml:space="preserve" x="{X0}" y="{YU}" font-size="{FS}" font-family="{MONO}">{spans}</text>\n')
body.append(t(115, 225, "In giallo i separatori:  ://   :   /   ?   #", 22, GREY))
parts = [("<proto>", PINK, "il protocollo di livello 7: http o https", "finisce con  ://"),
         ("<fqdn>", PURPLE, "il nome completo del server: il DNS", "lo traduce nell'indirizzo IP (livello 3)"),
         ("<port>", TEAL, "la porta (livello 4), dopo i  :", "si omette se è quella standard: 80 o 443"),
         ("<path>", NAVY, "la risorsa sul server, dopo la prima  /", "è quello che finisce nei log del web server"),
         ("<querystring>", AMBER, "parametri per il server, dopo il  ?", "nome=valore, più parametri uniti da  &"),
         ("<anchor>", ALLOY, "un punto della pagina, dopo il  #", "resta nel browser: non arriva al server")]
for i, (lab, c, l1, l2) in enumerate(parts):
    x, y = 70 + (i // 3) * 745, 440 + (i % 3) * 145
    body += [rect(x, y, 715, 130, "#FFFFFF", c, 3, 12), rect(x, y, 12, 130, c, rx=6),
             t(x + 35, y + 42, lab, 26, c, True, mono=True),
             t(x + 35, y + 80, l1, 22, INK), t(x + 35, y + 112, l2, 22, INK2)]
add("url", body)

# HTTP
req, _, ry = code(70, 225, 700, [("GET /wiki/Uniform_Resource_Locator?uselang=it HTTP/1.1", PINK, True),
                                  "Host: it.wikipedia.org", "User-Agent: curl/8.5.0", "Accept: */*", ""], 19, 32, pad=24)
res, _, sy = code(820, 225, 710, [("HTTP/1.1 200 OK", OK, True), "Date: Wed, 28 Oct 2026 10:15:02 GMT",
                                   "Content-Type: text/html; charset=UTF-8", "Content-Language: it", "",
                                   ("<!DOCTYPE html>", COMM), ('<html class="client-nojs" lang="it" dir="ltr">', COMM),
                                   ("... (il resto della pagina)", COMM)], 19, 32, dark=True, pad=24)


def small(x, title, color, lines, comment):
    c, _, _ = code(x, 600, 715, lines, 20, 34, dark=True, pad=22)
    return t(x, 585, title, 28, color, True) + c + t(x, 760, comment, 22, INK2)


add("http", [
    h("HTTP/1.1: richiesta e risposta", "La pagina di Wikipedia sull'URL, e le risposte da riconoscere"),
    t(70, 210, "richiesta (dal client)", 24, PINK, True), t(820, 210, "risposta (dal server)", 24, ALLOY, True),
    req, res, arrow(775, 300, 812, 300, INK, 4),
    t(70, ry[4] + 64, "La riga vuota chiude la richiesta.", 22, INK2),
    t(70, ry[4] + 98, "#cite_note-2 non c'è: l'anchor resta nel browser.", 22, INK2, True),
    t(1505, sy[4], "riga vuota: poi arriva il body", 18, COMM, anchor="end"),
    t(745, ry[4], "riga vuota", 18, GREY, anchor="end"),
    small(70, "302 Found: vai altrove", AMBER, [("$ curl -I http://its.fabersoft.net:3000", "#FFFFFF", True),
                                               ("HTTP/1.1 302 Found", "#FFD43B", True), ("Location: /login", "#FFD43B")],
          "Grafana risponde e rimanda alla pagina di login."),
    small(815, "404 Not Found: non esiste", PROM, [("GET /wiki/Pagina_che_non_esiste HTTP/1.1", "#FFFFFF", True),
                                                  ("HTTP/1.1 404 Not Found", "#FF8787", True), ("Content-Type: text/html; charset=UTF-8", "#FF8787")],
          "Il server risponde, ma quel path non c'è."),
    note(850, "Qualsiasi codice vuol dire che il livello 7 risponde: 2xx ok, 3xx altrove, 4xx errore del client, 5xx del server.", 22, INK, True),
])

# Varianti per i deck delle lezioni (non entrano nel Bignami)
EXTRA = {}
c1, yb, _ = code(70, 260, 1460, [("$ snmpget -v2c -c public 192.168.1.1 1.3.6.1.2.1.1.3.0", "#FFFFFF", True),
                                  ("iso.3.6.1.2.1.1.3.0 = Timeticks: (8640000) 1 day, 0:00:00.00", OK)], 24, 42, dark=True, pad=28)
c2, yb2, _ = code(70, yb + 90, 1460, [("$ snmpget -v3 -l authPriv -u monitor -a SHA -A <pwd> -x AES -X <pwd> \\", "#FFFFFF", True),
                                       ("      192.168.1.1 1.3.6.1.2.1.1.3.0", "#FFFFFF", True)], 24, 42, dark=True, pad=28)
EXTRA["snmp-comandi"] = page([
    h("SNMP in pratica", "La stessa domanda (da quanto è acceso l'apparato?) in v2c e in v3"),
    t(70, 240, "v2c: basta la community, che viaggia in chiaro", 28, PROM, True), c1,
    t(70, yb + 70, "v3: utente, autenticazione (SHA) e cifratura (AES)", 28, ALLOY, True), c2,
    note(yb2 + 70, "1.3.6.1.2.1.1.3.0 è l'OID di sysUpTime: il tempo dall'ultimo avvio.", 28, INK, False),
    note(yb2 + 130, "Con tcpdump sulla porta UDP 161 la community di v2c si legge; con v3 no.", 28, PROM, True),
])

B = dict(S)
B.update(EXTRA)

if __name__ == "__main__":
    save(sys.argv[1], S)
