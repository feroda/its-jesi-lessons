import sys
from lib import *

S = []
add = lambda name, body, side=False: S.append((name, page(body, side)))

art = (rect(1130, 380, 360, 300, "#FFFFFF", INK2, 3, 12) +
       "".join(f'<circle cx="1180" cy="{440 + i * 55}" r="14" fill="{ALLOY}"/>' +
               rect(1215, 430 + i * 55, 230 - (i % 2) * 60, 20, "#E4E7EB", rx=6) for i in range(5)))
S.append(("titolo", titlepage("LEZIONE 6", "Ripasso", "e compito", art)))

# 1 il quadro completo
from quadro import quadro_completo
S.append(("quadro-completo", page(quadro_completo())))

# 1 il percorso
items = [("1", "Troubleshooting di un caso reale: Grafana non risponde"),
         ("2", "I log del sistema e i comandi per leggerli"),
         ("3", "Docker: immagini, container, docker run"),
         ("4", "Docker Compose e log centralizzati"),
         ("5", "Monitoraggio: metriche, Prometheus, SNMP")]
body = [h("Il percorso", "Dal sistema completo giù fino alla riga di comando, e di nuovo su")]
for i, (n, s) in enumerate(items):
    body.append(step("L" + n, 270 + i * 110, s, size=32, mono=False))
add("percorso", body)

def ripasso(name, n, title, qs, color=DOCKER):
    body = [h(f"Ripasso {n} · {title}")]
    for i, q in enumerate(qs):
        body.append(step(i + 1, 280 + i * 120, q, size=34, mono=False, color=color))
    add(name, body)

ripasso("ripasso-architettura", 1, "L'architettura", [
    "Chi raccoglie i log, e su quale porta?",
    "Chi li mostra, e su quale porta?",
    "Chi apre la connessione: il PC o il server?",
    "Cosa cambia se il PC ha un IP privato?"], LOKI)

add("ripasso-troubleshooting", [
    h("Ripasso 2 · Troubleshooting dal client", "A quale livello lavora ogni comando?"),
    step(1, 290, "ping its.fabersoft.net", "livello ?", size=34),
    step(2, 400, "nc -zv its.fabersoft.net 3000", "livello ?", size=34),
    step(3, 510, "curl -I http://its.fabersoft.net:3000", "livello ?", size=34),
    rect(70, 610, 1460, 180, "#FFFFFF"),
    t(110, 680, "Il ping non risponde ma nc sì: il servizio è raggiungibile?", 32, INK, True),
    t(110, 735, "(ricordate befair3 nella lezione 1)", 28, INK2),
])

ripasso("ripasso-comandi", 3, "I comandi sui log", [
    "Cosa fanno grep -v, grep -c, cut -d' ' -f, wc -l?",
    "Perché prima di uniq serve sort?",
    "Perché cut sbaglia sulle righe di Sep  8?",
    "Come trovo il valore che compare più volte?"], TEAL)

add("ripasso-hello-world", [
    h("Ripasso 4 · Il primo container"),
    code(70, 200, 1460, ["$ docker run hello-world"], 40, dark=True, pad=30)[0],
    step(1, 420, "Quali sono i 4 passi che stampa?", size=34, mono=False),
    step(2, 530, "Perché docker ps non lo mostra e docker ps -a sì?", size=34, mono=False),
    step(3, 640, "Con quale comando leggo i suoi log?", size=34, mono=False),
])

ripasso("ripasso-compose", 5, "Docker e Docker Compose", [
    "docker run e docker compose up: che differenza c'è?",
    "Scrivete il compose.yml di un docker run -p 8080:80.",
    "Cosa fa docker compose down? E cosa resta?",
    "A cosa serve restart: unless-stopped?"], ALLOY)

ripasso("ripasso-sistema", 6, "Il vostro sistema", [
    "Agent o agentless: cosa scegliete per i PC?",
    "Push o pull: e perché?",
    "Dove finiscono i log e dove le metriche?",
    "Per quanti giorni li tenete (retention)?"], PROM)

add("il-compito", [
    t(100, 110, "Il compito", 56, INK, True),
    step(1, 240, "2 ore e 30 minuti, da soli", x=130, size=36, mono=False),
    step(2, 350, "Ammessi: repository del corso e cheatsheet", x=130, size=36, mono=False),
    step(3, 460, "Vietati: chat, messaggi, AI", x=130, size=36, mono=False),
    step(4, 570, "Si consegna un file di testo con nome e cognome", x=130, size=36, mono=False),
    rect(100, 660, 1430, 140, "#FFFFFF"),
    t(140, 745, "24 punti su 40 per la sufficienza.", 34, INK, True),
], side=True)

# Slide prese dal Bignami
from bignami import B


def dopo(nome, *nuove):
    i = [n for n, _ in S].index(nome)
    S[i + 1:i + 1] = [(n, B[n]) for n in nuove]

dopo("titolo", "scopi")
dopo("ripasso-comandi", "file-e-oneliner")

save(sys.argv[1], S)
