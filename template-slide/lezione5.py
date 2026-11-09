import sys
from lib import *

S = []
add = lambda name, body, side=False: S.append((name, page(body, side)))

# 0 titolo: un piccolo grafico come immagine
pts = [(1130, 640), (1180, 600), (1230, 620), (1280, 520), (1330, 560), (1380, 470), (1430, 500), (1480, 430)]
art = (rect(1100, 380, 420, 300, "#FFFFFF", INK2, 3, 12) +
       f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{PROM}" stroke-width="6" stroke-linejoin="round"/>' +
       t(1310, 730, "un numero nel tempo", 26, GREY, anchor="middle"))
S.append(("titolo", titlepage("LEZIONE 5", "Monitoraggio", "e Prometheus", art)))

# 1 log o metrica
spark = [(880, 640), (930, 600), (980, 615), (1030, 540), (1080, 570), (1130, 500), (1180, 520), (1230, 470), (1280, 500), (1330, 440)]
add("log-o-metrica", [
    h("Log o metrica?"),
    rect(70, 200, 700, 560, "#FFFFFF", LOKI, 3), rect(830, 200, 700, 560, "#FFFFFF", PROM, 3),
    t(420, 280, "Log", 48, LOKI, True, "middle"),
    t(110, 380, "sshd[812]: Failed password", 26, INK, mono=True),
    t(110, 420, "for root from 45.9.14.207", 26, INK, mono=True),
    t(420, 560, "racconta un evento", 34, INK, True, "middle"),
    t(420, 620, "parole, una riga per fatto", 28, INK2, anchor="middle"),
    t(1180, 280, "Metrica", 48, PROM, True, "middle"),
    f'<polyline points="{" ".join(f"{x},{340 + (y - 440) * 0.6:.0f}" for x, y in spark)}" fill="none" stroke="{PROM}" stroke-width="6" stroke-linejoin="round"/>',
    t(1180, 560, "misura un numero", 34, INK, True, "middle"),
    t(1180, 620, "CPU al 37%, ogni 15 secondi", 28, INK2, anchor="middle"),
])

# 2 serie temporale
rows = ""
for i, (tt, v) in enumerate([("10:00:00", "0.42"), ("10:00:15", "0.51"), ("10:00:30", "0.47"), ("10:00:45", "0.63")]):
    rows += t(200, 520 + i * 60, tt, 32, INK, mono=True) + t(560, 520 + i * 60, v, 32, PROM, True, mono=True)
add("serie-temporale", [
    h("Una serie temporale", "Nome + etichette + tante coppie (istante, valore)"),
    t(70, 290, "node_load1", 48, PROM, True, mono=True), t(390, 290, '{host="mario-rossi"}', 48, LOKI, True, mono=True),
    t(70, 345, "il nome: il carico del PC", 26, PROM), t(400, 345, "le etichette: di chi è", 26, LOKI),
    rect(150, 430, 560, 300, "#FFFFFF", INK2, 2), t(200, 470, "istante", 24, GREY, True), t(560, 470, "valore", 24, GREY, True), rows,
    t(800, 560, "Ogni 15 secondi", 34, INK, True), t(800, 610, "una riga in più.", 34, INK, True),
])

# 3 tsdb
add("tsdb", [
    h("Database a serie temporali", "TSDB, in inglese: time series database"),
    bullets(120, 300, ["Aggiunge numeri in fondo, in ordine di tempo.",
                       "Si legge per intervalli: ultimi 5 minuti, ultima ora.",
                       "Prometheus ne ha uno dentro: la cartella /prometheus."], 36, 110, dot=PROM),
    note(760, "Non si cancella riga per riga: si buttano via i giorni vecchi.", 30, INK2, False),
])

# 4 retention
add("retention", [
    h("Retention", "Per quanto tempo tengo i dati?"),
    code(70, 230, 1460, [("--storage.tsdb.retention.time=15d", PROM, True)], 44, pad=34)[0],
    bullets(120, 470, ["Più giorni = più disco.",
                       "Dopo 15 giorni i dati più vecchi spariscono.",
                       "Vale anche per i log, in Loki."], 36, 90, dot=PROM),
])

# 5 agent
add("agent", [
    h("Agent", "Un programma che gira sulla macchina da osservare"),
    rect(70, 220, 520, 360, "#FFFFFF", INK2, 3, 18), t(330, 280, "il tuo PC", 30, INK2, True, "middle"),
    box(150, 340, 360, 110, ALLOY, "Alloy", 36, "l'agent"),
    t(330, 520, "CPU, RAM, disco, log", 26, GREY, anchor="middle"),
    t(680, 330, "Vede tutto da dentro.", 36, ALLOY, True),
    t(680, 450, "Ma va installato e aggiornato", 32, PROM, True), t(680, 500, "su ogni macchina.", 32, PROM, True),
    note(740, "Alloy è il nostro agent: è lui a leggere i log e misurare il PC.", 30, INK2, False),
])

# 6 agentless
add("agentless", [
    h("Agentless", "Si osserva da fuori, senza installare niente"),
    step(1, 290, "ping its.fabersoft.net", "è acceso?", color=GREY),
    step(2, 400, "curl -I http://its.fabersoft.net:3000", "il sito risponde?", color=GREY),
    step(3, 510, "SNMP", "fra poco", color=GREY),
    note(650, "Il troubleshooting della lezione 1 era agentless.", 34, INK, True),
    note(730, "Vede solo quello che la macchina mostra a chi sta fuori.", 30, INK2, False),
])

# 7 pull
add("pull", [
    h("Pull: il server va a chiedere", "Prometheus, di base, fa così"),
    box(70, 380, 360, 140, PROM, "Prometheus", 36),
    box(1100, 230, 400, 110, INK2, "macchina 1", 30, fill="#FFFFFF"),
    box(1100, 395, 400, 110, INK2, "macchina 2", 30, fill="#FFFFFF"),
    box(1100, 560, 400, 110, INK2, "macchina 3", 30, fill="#FFFFFF"),
    arrow(435, 430, 1095, 285, PROM, 4), arrow(435, 450, 1095, 450, PROM, 4), arrow(435, 470, 1095, 615, PROM, 4),
    t(760, 425, "ogni 15 s: come stai?", 28, PROM, True, "middle"),
    note(790, "Il server deve riuscire a raggiungere ogni macchina.", 32, INK, True),
])

# 8 push
add("push", [
    h("Push: è la macchina a spedire", "Alloy verso Loki e verso Prometheus"),
    box(70, 230, 400, 110, ALLOY, "Alloy", 30, "PC 1"), box(70, 395, 400, 110, ALLOY, "Alloy", 30, "PC 2"),
    box(70, 560, 400, 110, ALLOY, "Alloy", 30, "PC 3"),
    box(1140, 380, 380, 140, PROM, "Prometheus", 36),
    arrow(475, 285, 1135, 430, ALLOY, 4), arrow(475, 450, 1135, 450, ALLOY, 4), arrow(475, 615, 1135, 470, ALLOY, 4),
    t(800, 425, "ecco i miei numeri", 28, ALLOY, True, "middle"),
    note(790, "Funziona anche da dietro il router di casa.", 32, INK, True),
])

# 9 perché push qui
add("pull-o-push", [
    h("Pull o push?"),
    rect(70, 190, 700, 480, "#FFFFFF", PROM, 3), rect(830, 190, 700, 480, "#FFFFFF", ALLOY, 3),
    t(420, 270, "Pull", 44, PROM, True, "middle"),
    t(110, 360, "+ il server sa subito chi è giù", 28, INK), t(110, 420, "+ si decide tutto sul server", 28, INK),
    t(110, 510, "- deve raggiungere ogni macchina", 28, INK2), t(110, 570, "- niente IP privati", 28, INK2),
    t(1180, 270, "Push", 44, ALLOY, True, "middle"),
    t(870, 360, "+ va bene dietro un router", 28, INK), t(870, 420, "+ i PC non aprono porte: ascolta solo il server", 28, INK),
    t(870, 510, "- se l'agent tace, non sai perché", 28, INK2), t(870, 570, "- ogni PC va configurato", 28, INK2),
    note(770, "I vostri PC hanno IP privati: push. Come per i log in lezione 4.", 32, INK, True),
])

# 10 snmp
add("snmp", [
    h("SNMP", "Per gli apparati dove non installi niente: switch, router, stampanti, UPS"),
    box(70, 360, 400, 140, PURPLE, "manager", 36, "chi chiede"),
    box(1130, 360, 400, 140, INK2, "agent SNMP", 34, "dentro lo switch", fill="#FFFFFF"),
    arrow(475, 400, 1125, 400, PURPLE, 5), t(800, 380, "domanda: UDP 161", 30, PURPLE, True, "middle"),
    arrow(1125, 470, 475, 470, PROM, 5), t(800, 530, "allarme (trap): UDP 162", 30, PROM, True, "middle"),
    note(740, "Lo switch ha già il suo piccolo agent, messo dal costruttore.", 30, INK2, False),
])

# 11 oid
add("oid-mib", [
    h("OID e MIB", "Ogni valore ha un indirizzo fatto di numeri"),
    code(70, 220, 1460, ["$ snmpget -v2c -c public 192.168.1.1 1.3.6.1.2.1.1.3.0"], 30, dark=True)[0],
    t(800, 420, "1.3.6.1.2.1.1.3.0", 56, PURPLE, True, "middle", mono=True),
    t(800, 490, "= da quanto tempo è acceso (sysUpTime)", 32, INK, anchor="middle"),
    note(660, "OID: l'indirizzo numerico di un valore.", 32, INK, True),
    note(730, "MIB: il dizionario che dà un nome ai numeri.", 32, INK, True),
])

# 12 snmp sicurezza
add("snmp-sicurezza", [
    h("SNMP e sicurezza"),
    rect(70, 190, 700, 500, "#FFFFFF", PROM, 3), rect(830, 190, 700, 500, "#FFFFFF", ALLOY, 3),
    t(420, 270, "v1, v2c", 44, PROM, True, "middle"),
    t(420, 370, "community \"public\"", 32, INK, True, "middle"),
    t(420, 440, "è una password", 28, INK2, anchor="middle"), t(420, 485, "che tutti conoscono", 28, INK2, anchor="middle"),
    t(420, 580, "e viaggia in chiaro", 28, PROM, True, "middle"),
    t(1180, 270, "v3", 44, ALLOY, True, "middle"),
    t(1180, 370, "utente e password", 32, INK, True, "middle"),
    t(1180, 440, "autenticazione", 28, INK2, anchor="middle"), t(1180, 485, "e cifratura", 28, INK2, anchor="middle"),
    note(790, "Con tcpdump, chi è sulla stessa rete legge la community.", 30, INK2, False),
])

# 13 server prometheus
c, _, ys = code(70, 180, 1060, [("  prometheus:", PROM, True), ("    image: prom/prometheus:v3.15.0", DOCKER, True), "    command:",
                                "      - --config.file=/etc/prometheus/prometheus.yml", "      - --storage.tsdb.path=/prometheus",
                                ("      - --storage.tsdb.retention.time=15d", PROM, True),
                                ("      - --web.enable-remote-write-receiver", PROM, True), "    volumes:",
                                ("      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro", AMBER, True),
                                ("      - prometheus-data:/prometheus", AMBER, True), "    ports:", ('      - "9090:9090"', TEAL, True),
                                ("    restart: unless-stopped", ALLOY, True)], 22, 40, pad=28)
add("server-prometheus", [
    h("Il server: arriva Prometheus", "Un servizio in più in vps-corso/compose.yml"), c,
    t(1160, ys[5], "← retention", 28, PROM, True), t(1160, ys[6], "← accetta il push", 28, PROM, True),
    t(1160, ys[9], "← il database", 28, AMBER, True), t(1160, ys[11], "← web e push", 28, TEAL, True),
    note(800, "In fondo al file, tra i volumes, una riga in più: prometheus-data:", 28, INK2, False),
])

# 14 due righe
add("due-righe", [
    h("Due righe da capire"),
    code(70, 200, 1460, [("--storage.tsdb.retention.time=15d", PROM, True)], 38, pad=30)[0],
    t(110, 360, "Tiene 15 giorni di metriche, poi butta i più vecchi.", 32, INK),
    code(70, 460, 1460, [("--web.enable-remote-write-receiver", PROM, True)], 38, pad=30)[0],
    t(110, 620, "Accetta i dati spediti dagli Alloy (push).", 32, INK),
    t(110, 670, "Senza questa riga Prometheus sa solo chiedere (pull).", 32, INK2),
])

# 15 client metriche
c, _, ys = code(70, 180, 1060, [('prometheus.exporter.unix "pc" {', ALLOY, True), '  procfs_path = "/host/proc"',
                                '  sysfs_path  = "/host/sys"', "}", "",
                                ('prometheus.scrape "pc" {', TEAL, True), "  targets    = prometheus.exporter.unix.pc.targets",
                                "  forward_to = [prometheus.remote_write.vps.receiver]", "}", "",
                                ('prometheus.remote_write "vps" {', PROM, True),
                                "  endpoint {", '    url = "http://its.fabersoft.net:9090/api/v1/write"', "  }",
                                "  external_labels = { host = constants.hostname }", "}"], 22, 38, pad=26)
add("client-metriche", [
    h("Il client: Alloy fa da node exporter", "Tre blocchi in più in pc-studente/alloy/config.alloy"), c,
    t(1180, ys[0], "1. misura il PC", 32, ALLOY, True),
    t(1180, ys[5], "2. raccogli", 32, TEAL, True), t(1180, ys[6] + 6, "ogni 15 s", 26, INK2),
    t(1180, ys[10], "3. spedisci", 32, PROM, True), t(1180, ys[11] + 6, "a Prometheus,", 26, INK2),
    t(1180, ys[12] + 10, "con l'etichetta host", 26, INK2),
])

# 16 due volumi
add("client-volumi", [
    h("Il client: due volumi in più", "In pc-studente/compose.yml, sotto volumes"),
    code(70, 220, 1460, [("      - /proc:/host/proc:ro", AMBER, True), ("      - /sys:/host/sys:ro", AMBER, True)], 38, pad=34)[0],
    t(110, 470, "Alloy legge da lì CPU, memoria, disco e rete.", 32, INK),
    rect(70, 590, 1460, 180, "#FFFFFF"),
    t(110, 660, "Su Windows (WSL2 o Docker Desktop):", 32, INK, True),
    t(110, 715, "misurate la macchina virtuale Linux, non Windows.", 30, INK2),
])

# 17 verifica
add("verifica", [
    h("Riavvio e verifica"),
    step(1, 260, "cd its-jesi-lessons/logging/pc-studente", size=30, color=ALLOY),
    step(2, 360, "docker compose up -d", "ricrea Alloy", size=30, color=ALLOY),
    step(3, 460, "http://its.fabersoft.net:9090", "Prometheus", size=30, color=PROM),
    step(4, 560, "up", "chi sta spedendo?", size=30, color=PROM),
    step(5, 660, 'node_load1{host="mario-rossi"}', "il tuo PC", size=30, color=PROM),
])

# 18 primo pannello
add("primo-pannello", [
    h("Il primo pannello in Grafana", "Dashboards → New → sorgente dati Prometheus"),
    code(70, 220, 1460, ["100 * (1 - avg by (host) (", '  rate(node_cpu_seconds_total{mode="idle"}[1m])))'], 32)[0],
    t(110, 470, "= la percentuale di CPU usata, una linea per ogni studente", 32, INK, True),
    note(640, "idle = il tempo in cui la CPU non fa niente.", 30, INK2, False),
    note(700, "100 meno il tempo libero = il tempo occupato.", 30, INK2, False),
])

# 19 observability
add("observability", [
    h("Observability", "Capire cosa succede dentro un sistema guardandolo da fuori"),
    box(70, 230, 440, 200, LOKI, "Log", 44, "Loki: cosa è successo"),
    box(580, 230, 440, 200, PROM, "Metriche", 44, "Prometheus: quanto"),
    box(1090, 230, 440, 200, GREY, "Trace", 44, "il percorso di una richiesta", fill="#FFFFFF"),
    t(290, 480, "visti", 28, ALLOY, True, "middle"), t(800, 480, "visti", 28, ALLOY, True, "middle"),
    t(1310, 480, "non li vediamo", 28, GREY, True, "middle"),
    rect(70, 560, 1460, 200, "#FFFFFF"),
    t(110, 630, "Stessa etichetta host nei log e nelle metriche:", 32, INK, True),
    t(110, 690, "dal picco di CPU delle 10:15 ai log di quel minuto.", 32, INK2),
])

# 20 quadro finale
add("quadro-finale", [
    h("Il quadro finale", "Lo stesso su befair3 e sul VPS del corso"),
    rect(70, 300, 380, 340, "#FFFFFF", INK2, 3, 18), t(260, 350, "i PC", 30, INK2, True, "middle"),
    box(110, 400, 300, 180, ALLOY, "Alloy", 40, "su ogni PC"),
    rect(640, 200, 600, 620, "#FFFFFF", INK, 4, 18), t(940, 245, "server", 28, INK, True, "middle"),
    box(690, 280, 280, 120, LOKI, "Loki", 34, ":3100"), box(690, 620, 280, 120, PROM, "Prometheus", 30, ":9090"),
    box(1010, 450, 200, 120, GRAFANA, "Grafana", 28, ":3000"),
    arrow(455, 400, 684, 340, LOKI, 5), t(560, 345, "log", 28, LOKI, True, "middle"),
    arrow(455, 540, 684, 680, PROM, 5), t(540, 660, "metriche", 28, PROM, True, "middle"),
    arrow(1060, 446, 975, 345, GREY, 3, "7 6"), arrow(1060, 574, 975, 675, GREY, 3, "7 6"),
    box(1300, 450, 230, 120, INK2, "browser", 30, fill="#FFFFFF"), arrow(1295, 510, 1215, 510, GRAFANA, 4),
])

# 21 prima di uscire
add("prima-di-uscire", [
    t(100, 110, "Prima di uscire", 56, INK, True),
    step(1, 220, "Che differenza c'è tra un log e una metrica?", x=130, size=34, mono=False),
    step(2, 315, "Pull o push: cosa usiamo, e perché?", x=130, size=34, mono=False),
    step(3, 410, "Cosa vuol dire retention di 15 giorni?", x=130, size=34, mono=False),
    step(4, 505, "Quando uso SNMP?", x=130, size=34, mono=False),
    rect(100, 610, 1430, 180, "#FFFFFF"),
    t(140, 685, "Ora: simulazione del compito", 34, INK, True),
    t(140, 740, "La prossima lezione: ripasso e compito.", 30, INK2),
], side=True)

# Slide prese dal Bignami
from bignami import B


def dopo(nome, *nuove):
    i = [n for n, _ in S].index(nome)
    S[i + 1:i + 1] = [(n, B[n]) for n in nuove]

dopo("log-o-metrica", "indicatori-chiave")
dopo("retention", "disco-retention")
dopo("snmp-sicurezza", "snmp-comandi", "flusso", "strumenti-monitoraggio", "prometheus")
dopo("primo-pannello", "metriche-eventi-alerting")
S[[n for n, _ in S].index("observability")] = ("observability", B["observability"])
dopo("quadro-finale", "fail2ban", "iptables-log")

save(sys.argv[1], S)
