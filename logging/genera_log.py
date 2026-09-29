#!/usr/bin/env python3
"""
Generatore di log per corso di logging.

Produce quattro file di log con scenari "piantati" e coerenti, piu' un file
soluzioni.txt con le risposte attese agli esercizi. Le soluzioni sono calcolate
dai dati effettivamente generati, quindi restano corrette anche cambiando seed.

File prodotti:
  sshd_classic.log    syslog classico, INCLUDE giorni da 1 a 9 (spazio doppio)
  sshd_highprec.log   stessi eventi SSH, formato rsyslog alta precisione
  apache_access.log   Apache combined
  mail.log            Postfix syslog classico, SOLO giorni 10-31
  soluzioni.txt       risposte attese

Uso:
  python3 genera_log.py                 # seed fisso (default), log riproducibili
  python3 genera_log.py --seed random   # seed casuale, un file diverso ogni volta
  python3 genera_log.py --seed 42        # seed specifico
  python3 genera_log.py --out ./logs     # cartella di output
"""

import argparse
import os
import random
from datetime import datetime, timedelta

MESI = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

HOST = "srv"

# ----------------------------------------------------------------------------
# Formattazione dei timestamp
# ----------------------------------------------------------------------------

def ts_syslog(dt):
    """'Sep  8 09:14:33' — giorno allineato a destra in 2 caratteri.
    I giorni da 1 a 9 producono il doppio spazio che rompe cut -d' '."""
    return f"{MESI[dt.month - 1]} {dt.day:2d} {dt:%H:%M:%S}"

def ts_highprec(dt):
    """'2026-09-28T15:51:02.123456+02:00' — data e ora in un solo campo."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond:06d}" + "+02:00"

def ts_apache(dt):
    """'28/Sep/2026:15:51:02 +0200'."""
    return f"{dt.day:02d}/{MESI[dt.month - 1]}/{dt.year}:{dt:%H:%M:%S} +0200"


# ----------------------------------------------------------------------------
# Generazione eventi SSH
# ----------------------------------------------------------------------------

def genera_ssh(rnd):
    """Ritorna (lista_eventi, statistiche).
    Ogni evento e' un dict: {dt, pid, kind, **campi}.
    kind in {'invalid', 'failed', 'accepted'}."""
    eventi = []
    stat = {}

    ip_legittimi = ["10.0.0.7", "10.0.0.12", "192.168.1.30"]
    utenti_reali = ["pippo", "deploy", "anna", "admin_lab"]
    utenti_spray = ["admin", "test", "oracle", "ubuntu", "git",
                    "postgres", "user", "ftp", "www-data", "guest"]

    def pid():
        return rnd.randint(1000, 9999)

    # --- Rumore di fondo: login riusciti legittimi sparsi su piu' giorni,
    #     alcuni con giorno da 1 a 9 per esercitare lo spazio doppio ---
    for giorno in [6, 7, 8, 9, 15, 22, 28]:
        n = rnd.randint(1, 3)
        for _ in range(n):
            dt = datetime(2026, 9, giorno,
                          rnd.randint(7, 19), rnd.randint(0, 59), rnd.randint(0, 59))
            eventi.append(dict(dt=dt, pid=pid(), kind="accepted",
                               user=rnd.choice(utenti_reali),
                               ip=rnd.choice(ip_legittimi),
                               port=rnd.randint(40000, 60000)))

    # --- Qualche fallimento sparso e innocuo su utenti reali (dita storte) ---
    for giorno in [7, 15, 28]:
        dt = datetime(2026, 9, giorno,
                      rnd.randint(8, 18), rnd.randint(0, 59), rnd.randint(0, 59))
        eventi.append(dict(dt=dt, pid=pid(), kind="failed",
                           user="pippo", ip="10.0.0.7",
                           port=rnd.randint(40000, 60000)))

    # --- Password spraying: un IP prova gli utenti comuni una volta ciascuno ---
    ip_spray = "185.22.1.9"
    stat["spray_ip"] = ip_spray
    dt = datetime(2026, 9, 8, 3, 11, 0)  # giorno 8: singola cifra, spazio doppio
    spray_count = 0
    for u in utenti_spray:
        p = pid()
        porta = rnd.randint(40000, 60000)
        eventi.append(dict(dt=dt, pid=p, kind="invalid",
                           user=u, ip=ip_spray, port=porta))
        # riga di follow-up realistica
        eventi.append(dict(dt=dt + timedelta(seconds=0), pid=p, kind="failed",
                           user=u, ip=ip_spray, port=porta, invalid=True))
        spray_count += 1
        dt += timedelta(seconds=rnd.randint(1, 4))
    stat["spray_count"] = spray_count

    # --- Brute force su un utente reale, con timing crescente,
    #     che alla fine RIESCE (accesso riuscito dopo N fallimenti) ---
    ip_brute = "45.9.14.207"
    utente_bersaglio = "deploy"
    stat["brute_ip"] = ip_brute
    stat["brute_user"] = utente_bersaglio
    dt = datetime(2026, 9, 28, 2, 47, 3)
    n_fallimenti = rnd.randint(28, 42)
    intervallo = 1.0
    for _ in range(n_fallimenti):
        eventi.append(dict(dt=dt, pid=pid(), kind="failed",
                           user=utente_bersaglio, ip=ip_brute,
                           port=rnd.randint(40000, 60000)))
        dt += timedelta(seconds=intervallo)
        intervallo *= 1.06  # timing leggermente crescente
    # il successo
    eventi.append(dict(dt=dt, pid=pid(), kind="accepted",
                       user=utente_bersaglio, ip=ip_brute,
                       port=rnd.randint(40000, 60000)))
    stat["brute_fallimenti"] = n_fallimenti

    # --- Un po' di rumore invalid isolato da IP vari ---
    rumore_invalid = 0
    for giorno in [9, 22]:
        for _ in range(rnd.randint(2, 4)):
            dt = datetime(2026, 9, giorno,
                          rnd.randint(0, 23), rnd.randint(0, 59), rnd.randint(0, 59))
            eventi.append(dict(dt=dt, pid=pid(), kind="invalid",
                               user=rnd.choice(utenti_spray),
                               ip=f"{rnd.randint(11,223)}.{rnd.randint(0,255)}."
                                  f"{rnd.randint(0,255)}.{rnd.randint(1,254)}",
                               port=rnd.randint(40000, 60000)))
            rumore_invalid += 1

    eventi.sort(key=lambda e: e["dt"])

    # statistiche aggregate
    stat["tot_invalid"] = sum(1 for e in eventi if e["kind"] == "invalid")
    stat["tot_failed"] = sum(1 for e in eventi if e["kind"] == "failed")
    stat["tot_accepted"] = sum(1 for e in eventi if e["kind"] == "accepted")
    stat["failed_pippo"] = sum(1 for e in eventi
                               if e["kind"] == "failed" and e["user"] == "pippo")
    return eventi, stat


def riga_ssh(ts, ev):
    """Costruisce il testo del messaggio SSH a partire dall'evento."""
    tag = f"sshd[{ev['pid']}]:"
    if ev["kind"] == "invalid":
        msg = f"Invalid user {ev['user']} from {ev['ip']} port {ev['port']}"
    elif ev["kind"] == "failed":
        if ev.get("invalid"):
            msg = (f"Failed password for invalid user {ev['user']} "
                   f"from {ev['ip']} port {ev['port']} ssh2")
        else:
            msg = (f"Failed password for {ev['user']} "
                   f"from {ev['ip']} port {ev['port']} ssh2")
    else:  # accepted
        msg = (f"Accepted password for {ev['user']} "
               f"from {ev['ip']} port {ev['port']} ssh2")
    return f"{ts} {HOST} {tag} {msg}"


# ----------------------------------------------------------------------------
# Generazione eventi Apache (combined)
# ----------------------------------------------------------------------------

def genera_apache(rnd):
    eventi = []
    stat = {}

    ua_browser = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/128.0 Safari/537.36")
    ua_scanner = "Mozilla/5.0 zgrab/0.x"
    ua_curl = "curl/8.5.0"

    ip_utenti = ["10.0.0.7", "10.0.0.12", "192.168.1.30", "93.44.10.2"]
    pagine_ok = ["/", "/index.php", "/products.php?id=12", "/products.php?id=7",
                 "/about.html", "/cart.php", "/static/style.css",
                 "/static/logo.png", "/login.php"]

    # --- Traffico normale ---
    base = datetime(2026, 9, 28, 9, 0, 0)
    tot_normali = 0
    for _ in range(rnd.randint(25, 35)):
        base += timedelta(seconds=rnd.randint(1, 40))
        url = rnd.choice(pagine_ok)
        size = rnd.randint(200, 8000)
        eventi.append(dict(dt=base, ip=rnd.choice(ip_utenti),
                           method="GET", url=url, status=200, size=size,
                           ref="https://shop.lab/", ua=ua_browser))
        tot_normali += 1

    # --- Scanner: raffica di 404 su directory tipiche, un unico IP ---
    ip_scanner = "185.220.101.54"
    stat["scanner_ip"] = ip_scanner
    dirs = ["/wp-admin/", "/wp-login.php", "/.env", "/.git/config",
            "/admin/", "/phpmyadmin/", "/backup.zip", "/config.php.bak",
            "/administrator/", "/xmlrpc.php", "/vendor/", "/.aws/credentials",
            "/.git/HEAD", "/wp-content/", "/.ssh/id_rsa", "/server-status",
            "/cgi-bin/", "/shell.php", "/wp-config.php.bak", "/.env.local",
            "/adminer.php", "/db.sql", "/old/", "/test.php", "/info.php",
            "/.htaccess", "/config/database.yml", "/api/v1/users",
            "/robots.txt.bak", "/sitemap.xml.bak", "/dump.sql",
            "/backup/", "/uploads/shell.php", "/wp-json/wp/v2/users",
            "/.git/logs/HEAD", "/composer.json", "/package.json.bak",
            "/.svn/entries", "/web.config", "/phpinfo.php", "/console",
            "/actuator/env", "/.dockerenv", "/id_rsa", "/credentials.json"]
    dt = datetime(2026, 9, 28, 14, 3, 0)
    tot_404_scanner = 0
    for d in dirs:
        eventi.append(dict(dt=dt, ip=ip_scanner, method="GET", url=d,
                           status=404, size=196, ref="-", ua=ua_scanner))
        tot_404_scanner += 1
        dt += timedelta(seconds=rnd.randint(0, 2))

    # --- Tentativi di SQL injection sullo stesso endpoint ---
    ip_sqli = "45.9.14.207"
    stat["sqli_ip"] = ip_sqli
    payloads = ["/products.php?id=12'", "/products.php?id=12+OR+1=1",
                "/products.php?id=12+UNION+SELECT+1,2,3--",
                "/products.php?id=12;DROP+TABLE+users--",
                "/products.php?id=-1'+UNION+SELECT+username,password+FROM+users--"]
    dt = datetime(2026, 9, 28, 14, 20, 0)
    tot_sqli = 0
    for p in payloads:
        st = rnd.choice([200, 200, 500])  # qualche 500 da errore SQL
        eventi.append(dict(dt=dt, ip=ip_sqli, method="GET", url=p,
                           status=st, size=rnd.randint(0, 3000),
                           ref="-", ua=ua_curl))
        tot_sqli += 1
        dt += timedelta(seconds=rnd.randint(1, 5))

    # --- Qualche 404 legittimo sparso (link rotti) ---
    tot_404_legit = 0
    for _ in range(rnd.randint(2, 4)):
        t = datetime(2026, 9, 28, rnd.randint(9, 17),
                     rnd.randint(0, 59), rnd.randint(0, 59))
        eventi.append(dict(dt=t, ip=rnd.choice(ip_utenti), method="GET",
                           url="/vecchia-pagina.html", status=404, size=196,
                           ref="https://shop.lab/", ua=ua_browser))
        tot_404_legit += 1

    eventi.sort(key=lambda e: e["dt"])

    stat["tot_404"] = tot_404_scanner + tot_404_legit
    stat["tot_404_scanner"] = tot_404_scanner
    stat["tot_richieste"] = len(eventi)
    return eventi, stat


def riga_apache(ev):
    size = ev["size"] if ev["size"] > 0 else "-"
    return (f'{ev["ip"]} - - [{ts_apache(ev["dt"])}] '
            f'"{ev["method"]} {ev["url"]} HTTP/1.1" {ev["status"]} {size} '
            f'"{ev["ref"]}" "{ev["ua"]}"')


# ----------------------------------------------------------------------------
# Generazione eventi Postfix (mail.log) — SOLO giorni 10-31
# ----------------------------------------------------------------------------

def queue_id(rnd):
    return "".join(rnd.choice("0123456789ABCDEF") for _ in range(10))

def genera_mail(rnd):
    """Genera messaggi con from/to/status coerenti via queue ID.
    Include sent (250), bounced (550/552) e deferred (4xx) con retry."""
    righe = []  # (dt, testo_messaggio)
    stat = dict(sent=0, bounced=0, deferred=0, from_example=0)

    mittenti_example = ["mario@example.com", "lucia@example.com",
                        "info@example.com"]
    mittenti_altri = ["ordini@shop.lab", "noreply@newsletter.it",
                      "carlo@altrodominio.org"]
    destinatari = ["anna@dest.it", "luca@dest.it", "paolo@posta.net",
                   "giulia@dest.it", "team@cliente.com"]

    def emetti(dt, pid_qmgr, pid_smtp, frm, dests_status):
        """dests_status: lista di (dest, status, codice, testo).
        status in {sent, bounced, deferred}."""
        qid = queue_id(rnd)
        nrcpt = len(dests_status)
        size = rnd.randint(900, 9000)
        # riga qmgr con il mittente
        righe.append((dt, f"postfix/qmgr[{pid_qmgr}]: {qid}: "
                          f"from=<{frm}>, size={size}, nrcpt={nrcpt} (queue active)"))
        if frm in mittenti_example:
            stat["from_example"] += 1
        t = dt + timedelta(seconds=1)
        for (dest, status, codice, testo) in dests_status:
            if status == "sent":
                dsn = "2.0.0"
                coda = f"status=sent (250 2.0.0 OK {codice})" if codice else \
                       "status=sent (250 2.0.0 OK)"
                relay = "mx.dest.it[5.6.7.8]:25"
                stat["sent"] += 1
            elif status == "bounced":
                dsn = "5.1.1" if "550" in testo else "5.2.2"
                coda = (f"status=bounced (host mx.dest.it[5.6.7.8] said: "
                        f"{testo} (in reply to RCPT TO command))")
                relay = "mx.dest.it[5.6.7.8]:25"
                stat["bounced"] += 1
            else:  # deferred
                dsn = "4.4.1"
                coda = f"status=deferred ({testo})"
                relay = "mx.dest.it[5.6.7.8]:25"
                stat["deferred"] += 1
            righe.append((t, f"postfix/smtp[{pid_smtp}]: {qid}: "
                             f"to=<{dest}>, relay={relay}, delay={rnd.uniform(0.3,4.0):.1f}, "
                             f"dsn={dsn}, {coda}"))
            t += timedelta(seconds=1)
        return qid

    def pid():
        return rnd.randint(700, 999)

    # --- Alcuni messaggi consegnati (250) ---
    for giorno in [15, 22, 28]:
        for _ in range(rnd.randint(2, 4)):
            dt = datetime(2026, 9, giorno,
                          rnd.randint(8, 18), rnd.randint(0, 59), rnd.randint(0, 59))
            frm = rnd.choice(mittenti_example + mittenti_altri)
            dests = [(rnd.choice(destinatari), "sent", "", "")]
            if rnd.random() < 0.4:  # a volte due destinatari
                dests.append((rnd.choice(destinatari), "sent", "", ""))
            emetti(dt, pid(), pid(), frm, dests)

    # --- Bounce: 550 user unknown ---
    dt = datetime(2026, 9, 22, 11, 5, 0)
    emetti(dt, pid(), pid(), "info@example.com",
           [("inesistente@dest.it", "bounced", "", "550 5.1.1 <inesistente@dest.it>: "
             "Recipient address rejected: User unknown in virtual mailbox table")])

    # --- Bounce: 552 mailbox full ---
    dt = datetime(2026, 9, 28, 16, 40, 0)
    emetti(dt, pid(), pid(), "noreply@newsletter.it",
           [("paolo@posta.net", "bounced", "", "552 5.2.2 <paolo@posta.net>: "
             "Recipient address rejected: Mailbox full")])

    # --- Deferred che al retry diventa SENT (stesso queue ID due volte) ---
    dt = datetime(2026, 9, 15, 9, 30, 0)
    qid_def = queue_id(rnd)
    p1, p2 = pid(), pid()
    righe.append((dt, f"postfix/qmgr[{p1}]: {qid_def}: "
                      f"from=<mario@example.com>, size=2210, nrcpt=1 (queue active)"))
    stat["from_example"] += 1
    righe.append((dt + timedelta(seconds=1),
                  f"postfix/smtp[{p2}]: {qid_def}: to=<giulia@dest.it>, "
                  f"relay=mx.dest.it[5.6.7.8]:25, delay=30, dsn=4.4.1, "
                  f"status=deferred (connect to mx.dest.it[5.6.7.8]:25: "
                  f"Connection timed out)"))
    stat["deferred"] += 1
    # retry dopo ~15 minuti: consegnato
    dt2 = dt + timedelta(minutes=15, seconds=2)
    righe.append((dt2, f"postfix/qmgr[{p1}]: {qid_def}: "
                       f"from=<mario@example.com>, size=2210, nrcpt=1 (queue active)"))
    stat["from_example"] += 1
    righe.append((dt2 + timedelta(seconds=1),
                  f"postfix/smtp[{p2}]: {qid_def}: to=<giulia@dest.it>, "
                  f"relay=mx.dest.it[5.6.7.8]:25, delay=902, dsn=2.0.0, "
                  f"status=sent (250 2.0.0 OK)"))
    stat["sent"] += 1

    # --- Deferred che al retry diventa BOUNCED ---
    dt = datetime(2026, 9, 22, 14, 12, 0)
    qid_db = queue_id(rnd)
    p1, p2 = pid(), pid()
    righe.append((dt, f"postfix/qmgr[{p1}]: {qid_db}: "
                      f"from=<ordini@shop.lab>, size=1500, nrcpt=1 (queue active)"))
    righe.append((dt + timedelta(seconds=1),
                  f"postfix/smtp[{p2}]: {qid_db}: to=<team@cliente.com>, "
                  f"relay=none, delay=10, dsn=4.4.3, "
                  f"status=deferred (Host or domain name not found. "
                  f"Name service error for name=cliente.com type=MX: "
                  f"Host not found, try again)"))
    stat["deferred"] += 1
    dt2 = dt + timedelta(hours=4)
    righe.append((dt2, f"postfix/qmgr[{p1}]: {qid_db}: "
                       f"from=<ordini@shop.lab>, size=1500, nrcpt=1 (queue active)"))
    righe.append((dt2 + timedelta(seconds=1),
                  f"postfix/smtp[{p2}]: {qid_db}: to=<team@cliente.com>, "
                  f"relay=none, delay=14400, dsn=5.4.4, "
                  f"status=bounced (Host or domain name not found. "
                  f"Name service error for name=cliente.com type=MX: "
                  f"Host not found)"))
    stat["bounced"] += 1

    righe.sort(key=lambda r: r[0])
    return righe, stat


# ----------------------------------------------------------------------------
# Scrittura file e soluzioni
# ----------------------------------------------------------------------------

def scrivi(path, righe):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(righe) + "\n")

def main():
    ap = argparse.ArgumentParser(description="Genera log per il corso di logging.")
    ap.add_argument("--seed", default="1337",
                    help="intero per log riproducibili (default 1337) "
                         "oppure 'random' per un file diverso ogni volta")
    ap.add_argument("--out", default=".", help="cartella di output")
    args = ap.parse_args()

    if args.seed == "random":
        seme = random.randrange(1, 10**9)
    else:
        seme = int(args.seed)
    rnd = random.Random(seme)

    os.makedirs(args.out, exist_ok=True)

    # SSH
    ssh_ev, ssh_stat = genera_ssh(rnd)
    scrivi(os.path.join(args.out, "sshd_classic.log"),
           [riga_ssh(ts_syslog(e["dt"]), e) for e in ssh_ev])
    scrivi(os.path.join(args.out, "sshd_highprec.log"),
           [riga_ssh(ts_highprec(e["dt"]), e) for e in ssh_ev])

    # Apache
    ap_ev, ap_stat = genera_apache(rnd)
    scrivi(os.path.join(args.out, "apache_access.log"),
           [riga_apache(e) for e in ap_ev])

    # Mail
    mail_righe, mail_stat = genera_mail(rnd)
    scrivi(os.path.join(args.out, "mail.log"),
           [f"{ts_syslog(dt)} {HOST} {msg}" for (dt, msg) in mail_righe])

    # Soluzioni
    sol = []
    sol.append(f"SOLUZIONI — seed usato: {seme}")
    sol.append("=" * 60)
    sol.append("")
    sol.append("SSH (sshd_classic.log / sshd_highprec.log)")
    sol.append("-" * 60)
    sol.append(f"Fallimenti su utente 'pippo' (Failed password): {ssh_stat['failed_pippo']}")
    sol.append(f"Totale righe 'Invalid user': {ssh_stat['tot_invalid']}")
    sol.append(f"Totale righe 'Failed password': {ssh_stat['tot_failed']}")
    sol.append(f"Totale accessi riusciti (Accepted): {ssh_stat['tot_accepted']}")
    sol.append(f"Password spraying dall'IP {ssh_stat['spray_ip']}: "
               f"{ssh_stat['spray_count']} utenti diversi provati")
    sol.append(f"Brute force dall'IP {ssh_stat['brute_ip']} su utente "
               f"'{ssh_stat['brute_user']}': {ssh_stat['brute_fallimenti']} "
               f"fallimenti seguiti da UN accesso riuscito")
    sol.append("  -> L'IP che riesce a entrare dopo molti fallimenti e' "
               f"{ssh_stat['brute_ip']} (cerca 'Accepted' con quell'IP).")
    sol.append("  NOTA cut vs awk: nei giorni da 1 a 9 (es. 'Sep  8') il doppio")
    sol.append("  spazio sposta i campi di cut -d' '. awk li tratta come un solo")
    sol.append("  separatore, quindi awk '{print $8}' resta corretto. In alta")
    sol.append("  precisione data+ora sono nel campo 1: l'utente invalid passa")
    sol.append("  dal campo 8 al campo 6.")
    sol.append("")
    sol.append("APACHE (apache_access.log)")
    sol.append("-" * 60)
    sol.append(f"Totale richieste: {ap_stat['tot_richieste']}")
    sol.append(f"Totale 404: {ap_stat['tot_404']} "
               f"(di cui {ap_stat['tot_404_scanner']} dallo scanner)")
    sol.append(f"IP che scansiona directory (raffica di 404): {ap_stat['scanner_ip']}")
    sol.append(f"IP con tentativi di SQL injection: {ap_stat['sqli_ip']}")
    sol.append("  -> 'Contare le richieste per ogni IP' mette in cima proprio")
    sol.append("     lo scanner e l'IP SQLi.")
    sol.append("")
    sol.append("MAIL (mail.log)")
    sol.append("-" * 60)
    sol.append(f"Righe status=sent: {mail_stat['sent']}")
    sol.append(f"Righe status=bounced: {mail_stat['bounced']}")
    sol.append(f"Righe status=deferred: {mail_stat['deferred']}")
    sol.append(f"Righe from=<...@example.com>: {mail_stat['from_example']}")
    sol.append("  NOTA: due queue ID compaiono in piu' stati per via del retry")
    sol.append("  (deferred -> sent, e deferred -> bounced). Contare i 'sent'")
    sol.append("  conta i destinatari consegnati, non i messaggi unici.")
    sol.append("")
    scrivi(os.path.join(args.out, "soluzioni.txt"), sol)

    print(f"Generati in '{args.out}' con seed {seme}:")
    for nome in ["sshd_classic.log", "sshd_highprec.log",
                 "apache_access.log", "mail.log", "soluzioni.txt"]:
        p = os.path.join(args.out, nome)
        n = sum(1 for _ in open(p, encoding="utf-8"))
        print(f"  {nome:20s} {n:4d} righe")


if __name__ == "__main__":
    main()
