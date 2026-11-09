"""Il quadro completo: browser, PC con Alloy, VPS con Grafana, Loki e Prometheus."""
from lib import *

def curve(x1, y1, x2, y2, color, w=5):
    m = MARK.get(color, "K")
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" marker-end="url(#a{m})"/>\n')

def port(y, label, color):
    return rect(925, y - 30, 130, 60, color, rx=8) + t(990, y + 11, label, 30, "#FFFFFF", True, "middle")

cloud = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EEF1F5" stroke="#A0AAB4" stroke-width="3"/>'
                for x, y, r in [(560, 560, 90), (665, 515, 100), (750, 580, 85), (510, 610, 70), (640, 630, 90)])
cloud += "".join(f'<circle cx="{x}" cy="{y}" r="{r - 2}" fill="#EEF1F5"/>'
                 for x, y, r in [(560, 560, 90), (665, 515, 100), (750, 580, 85), (510, 610, 70), (640, 630, 90)])
cloud += t(650, 495, "Internet", 34, GREY, True, "middle")

def pc(y, name):
    return (rect(40, y, 260, 130, "#FFFFFF", INK2, 3, 12) + t(170, y + 45, name, 28, INK, True, "middle") +
            box(70, y + 65, 200, 48, ALLOY, "Alloy", 26))


def quadro_completo():
    return [
    h("Il quadro completo", "Chi guarda log e metriche, e chi li manda"),
    rect(990, 180, 570, 690, "#F5F7FA", INK, 4, 18),
    t(1275, 222, "VPS its.fabersoft.net", 30, INK, True, "middle"),
    rect(1040, 245, 490, 605, "none", DOCKER, 3, 14, "12 8"),
    t(1285, 280, "docker compose", 26, DOCKER, True, "middle"),
    box(1090, 300, 370, 120, GRAFANA, "Grafana", 38, "guarda log e metriche"),
    box(1090, 475, 300, 115, LOKI, "Loki", 36, "i log"),
    box(1090, 675, 300, 115, PROM, "Prometheus", 36, "le metriche"),
    arrow(1240, 424, 1240, 468, GREY, 3, "7 6"),
    f'<path d="M1462,360 L1495,360 L1495,732 L1398,732" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="7 6" marker-end="url(#aY)"/>',
    t(1255, 455, "interroga", 22, GREY),
    rect(1055, 360, 35, 4, GRAFANA, rx=0), rect(1055, 530, 35, 4, LOKI, rx=0), rect(1055, 730, 35, 4, PROM, rx=0),
    cloud,
    rect(40, 290, 260, 110, "#FFFFFF", INK2, 3, 12), rect(42, 292, 256, 28, "#CBD2D9", rx=10),
    '<circle cx="62" cy="306" r="6" fill="#E03131"/><circle cx="80" cy="306" r="6" fill="#F59F00"/><circle cx="98" cy="306" r="6" fill="#2F9E44"/>',
    rect(55, 330, 230, 30, "#F5F7FA", "#A0AAB4", 1.5, 6), t(65, 351, "its.fabersoft.net:3000", 16, INK2, mono=True),
    t(170, 388, "browser", 26, INK, True, "middle"),
    pc(500, "PC di Anna"), pc(690, "PC di Mario"),
    curve(305, 345, 915, 360, GRAFANA),
    curve(305, 560, 915, 520, LOKI), curve(305, 755, 915, 540, LOKI),
    curve(305, 600, 915, 720, PROM), curve(305, 790, 915, 740, PROM),
    port(360, ":3000", GRAFANA), port(530, ":3100", LOKI), port(730, ":9090", PROM),
    t(560, 300, "HTTP, porta 3000", 26, GRAFANA, True, "middle"),
    t(70, 865, "Alloy spedisce i log a Loki", 26, LOKI, True),
    t(520, 865, "e le metriche a Prometheus", 26, PROM, True),
]
