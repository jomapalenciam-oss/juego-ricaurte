"""Dibujo del fondo de cada nivel y de los objetos que hay en él."""

import random

import pygame

from juego import config
from juego.config import (
    ARENA, AZUL, BLANCO, CIAN, DORADO, GRIS, MORADO, ROJO, VERDE2,
)
from juego.dibujo import arbol, texto

# Las decoraciones aleatorias (estrellas del nivel 3, grietas del nivel 5) se
# calculan UNA vez por nivel con una semilla fija. En el original se sorteaban
# en cada frame y parpadeaban.
_decoracion = {}


def _deco(nivel):
    if nivel not in _decoracion:
        rng = random.Random(1000 + nivel)
        _decoracion[nivel] = {
            "estrellas": [
                (rng.randint(50, 1150), rng.randint(90, 700)) for _ in range(25)
            ],
            "grietas": [rng.randint(-30, 30) for _ in range(15)],
        }
    return _decoracion[nivel]


def _suelo(pantalla, color):
    pygame.draw.rect(pantalla, color, (35, 80, 1130, 630), border_radius=28)


def _fondo_bosque(pantalla, fuentes):
    pantalla.fill((14, 45, 29))
    _suelo(pantalla, (25, 90, 48))

    for x, y in [(100, 150), (250, 100), (420, 170), (650, 115), (900, 150),
                 (1080, 240), (180, 610), (430, 620), (780, 610), (1040, 560)]:
        arbol(pantalla, x, y, 1)

    pygame.draw.rect(pantalla, (105, 75, 48), (80, 330, 1050, 80),
                     border_radius=30)
    pygame.draw.rect(pantalla, (55, 115, 170), (70, 95, 190, 105),
                     border_radius=20)


def _fondo_desierto(pantalla, fuentes):
    pantalla.fill((95, 62, 35))
    _suelo(pantalla, ARENA)

    pygame.draw.rect(pantalla, (225, 185, 110), (80, 330, 1050, 75),
                     border_radius=30)

    for x, y in [(230, 150), (500, 130), (850, 170),
                 (1020, 500), (260, 570), (760, 600)]:
        pygame.draw.circle(pantalla, (160, 115, 60), (x, y), 65)

    pygame.draw.ellipse(pantalla, AZUL, (70, 100, 190, 100))


def _fondo_ciudad(pantalla, fuentes):
    pantalla.fill((12, 12, 35))
    _suelo(pantalla, (25, 30, 75))

    for x in range(100, 1150, 100):
        pygame.draw.line(pantalla, (45, 70, 130), (x, 100), (x, 700), 1)

    for y in range(120, 700, 60):
        pygame.draw.line(pantalla, (45, 70, 130), (50, y), (1150, y), 1)

    for x, y in _deco(3)["estrellas"]:
        pygame.draw.circle(pantalla, CIAN, (x, y), 2)


def _fondo_templo(pantalla, fuentes):
    pantalla.fill((35, 22, 52))
    _suelo(pantalla, (70, 42, 88))

    for x in range(100, 1150, 120):
        pygame.draw.rect(pantalla, (100, 60, 115), (x, 150, 50, 420),
                         border_radius=12)

    pygame.draw.rect(pantalla, (45, 28, 60), (80, 330, 1050, 80),
                     border_radius=25)


def _fondo_abismo(pantalla, fuentes):
    pantalla.fill((8, 8, 20))
    _suelo(pantalla, (25, 15, 45))

    for i, desvio in enumerate(_deco(5)["grietas"]):
        x = 70 + i * 75
        pygame.draw.line(pantalla, MORADO, (x, 100), (x + desvio, 700), 2)

    for i in range(12):
        y = 120 + i * 50
        pygame.draw.line(pantalla, (45, 35, 80), (50, y), (1150, y), 1)


def _fondo_matrix(pantalla, fuentes):
    pantalla.fill((5, 10, 14))
    _suelo(pantalla, (10, 40, 42))

    # Lluvia de código: la posición depende del reloj, no del azar.
    ticks = pygame.time.get_ticks()
    for x in range(70, 1150, 55):
        y = (ticks // 8 + x * 7) % 620 + 90
        texto(pantalla, "1", fuentes.mini, CIAN, x, y, False)


FONDOS = {
    1: _fondo_bosque,
    2: _fondo_desierto,
    3: _fondo_ciudad,
    4: _fondo_templo,
    5: _fondo_abismo,
    6: _fondo_matrix,
}


def fondo_nivel(pantalla, fuentes, nivel):
    FONDOS.get(nivel, _fondo_matrix)(pantalla, fuentes)


# ---------------------------------------------------------------------------
# Objetos del nivel
# ---------------------------------------------------------------------------

def _dibujar_monedas(pantalla, monedas):
    for r in monedas:
        pygame.draw.circle(pantalla, DORADO, r.center, 8)
        pygame.draw.circle(pantalla, config.AMARILLO, r.center, 4)


def _dibujar_fragmentos(pantalla, fragmentos):
    for r in fragmentos:
        pygame.draw.polygon(pantalla, CIAN, [
            (r.centerx, r.y - 5),
            (r.right, r.centery),
            (r.centerx, r.bottom + 5),
            (r.x, r.centery),
        ])
        pygame.draw.polygon(pantalla, BLANCO, [
            (r.centerx, r.y + 1),
            (r.right - 7, r.centery),
            (r.centerx, r.bottom - 1),
            (r.x + 7, r.centery),
        ])


def _dibujar_trampas(pantalla, trampas):
    for r in trampas:
        pygame.draw.rect(pantalla, (100, 20, 35), r, border_radius=7)
        pygame.draw.line(pantalla, ROJO, r.topleft, r.bottomright, 3)
        pygame.draw.line(pantalla, ROJO, r.topright, r.bottomleft, 3)


def _dibujar_enemigos(pantalla, enemigos):
    for enemigo in enemigos:
        r = enemigo["rect"]
        pygame.draw.circle(pantalla, (80, 45, 105), r.center, 18)
        pygame.draw.circle(pantalla, ROJO, (r.centerx - 6, r.centery - 4), 4)
        pygame.draw.circle(pantalla, ROJO, (r.centerx + 6, r.centery - 4), 4)


def _dibujar_puerta(pantalla, fuentes, juego):
    abierta = juego.puerta_abierta()
    color = DORADO if abierta else GRIS

    pygame.draw.rect(pantalla, (20, 25, 30), juego.puerta, border_radius=8)
    pygame.draw.rect(pantalla, color, juego.puerta, 3, border_radius=8)
    pygame.draw.circle(pantalla, color, juego.puerta.center, 7)

    if juego.nivel == config.NIVEL_MAX:
        etiqueta = "ABIERTA" if abierta else "BLOQUEADA"
        pygame.draw.rect(pantalla, (12, 14, 20),
                         (juego.puerta.centerx - 52, juego.puerta.y - 30,
                          104, 22), border_radius=6)
        texto(pantalla, etiqueta, fuentes.mini,
              VERDE2 if abierta else ROJO,
              juego.puerta.centerx, juego.puerta.y - 19)


def dibujar_objetos(pantalla, fuentes, juego):
    _dibujar_monedas(pantalla, juego.monedas)
    _dibujar_fragmentos(pantalla, juego.fragmentos_nivel)
    _dibujar_trampas(pantalla, juego.trampas)
    _dibujar_enemigos(pantalla, juego.enemigos)
    _dibujar_puerta(pantalla, fuentes, juego)
