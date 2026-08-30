"""Generación del contenido de cada nivel.

Todo lo que aparece se coloca respetando una zona segura alrededor del punto
de aparición del jugador, para que nunca reciba daño nada más entrar al nivel.
"""

import random

import pygame

from juego import config

# Rangos de colocación (x_min, x_max) e (y_min, y_max).
RANGO_FRAGMENTO = ((100, 1030), (130, 600))
RANGO_MONEDA = ((80, 1080), (120, 650))
RANGO_ENEMIGO = ((120, 1000), (130, 620))
RANGO_TRAMPA = ((100, 1050), (130, 620))

TAM_FRAGMENTO = (22, 22)
TAM_MONEDA = (14, 14)
TAM_ENEMIGO = (34, 34)
TAM_TRAMPA = (35, 35)

INTENTOS_COLOCACION = 80


def zona_segura():
    """Área alrededor del spawn donde no debe aparecer nada peligroso."""
    x, y = config.SPAWN_JUGADOR
    lado = config.TAM_JUGADOR
    jugador = pygame.Rect(0, 0, lado, lado)
    jugador.center = (x, y)
    return jugador.inflate(config.MARGEN_SPAWN, config.MARGEN_SPAWN)


def _colocar(rng, rango, tam, evitar):
    """Busca un rectángulo libre; si no lo consigue, devuelve el último intento.

    El bucle está acotado a propósito: nunca se puede colgar aunque el mapa
    esté muy lleno.
    """
    (x_min, x_max), (y_min, y_max) = rango
    ancho, alto = tam
    rect = None

    for _ in range(INTENTOS_COLOCACION):
        rect = pygame.Rect(
            rng.randint(x_min, x_max),
            rng.randint(y_min, y_max),
            ancho,
            alto,
        )
        if not any(rect.colliderect(otro) for otro in evitar):
            return rect

    return rect


def generar(nivel, rng=None):
    """Crea el contenido de un nivel.

    Devuelve un diccionario con las claves: fragmentos, monedas, enemigos,
    trampas y puerta.
    """
    rng = rng or random
    segura = zona_segura()
    puerta = pygame.Rect(*config.PUERTA)

    # Los fragmentos van primero: son el objetivo, deben quedar accesibles.
    ocupado = [segura, puerta.inflate(80, 80)]
    fragmentos = []
    for _ in range(config.FRAGMENTOS_OBJETIVO):
        r = _colocar(rng, RANGO_FRAGMENTO, TAM_FRAGMENTO, ocupado)
        fragmentos.append(r)
        ocupado.append(r.inflate(60, 60))

    # Las trampas evitan el spawn, la puerta y los fragmentos, para que ningún
    # fragmento quede encima de una trampa.
    trampas = []
    for _ in range(nivel + 2):
        r = _colocar(rng, RANGO_TRAMPA, TAM_TRAMPA, ocupado)
        trampas.append(r)
        ocupado.append(r)

    # Los enemigos se mueven, así que basta con que no nazcan sobre el jugador.
    enemigos = []
    for _ in range(max(1, nivel)):
        r = _colocar(rng, RANGO_ENEMIGO, TAM_ENEMIGO, [segura])
        enemigos.append({
            "rect": r,
            "x": float(r.x),
            "y": float(r.y),
            # Velocidades en píxeles por segundo (antes eran por frame).
            "vx": rng.choice([-120.0, -90.0, 90.0, 120.0]),
            "vy": rng.choice([-90.0, 90.0]),
        })

    # Las monedas son inofensivas: pueden aparecer en cualquier parte.
    monedas = [
        pygame.Rect(
            rng.randint(*RANGO_MONEDA[0]),
            rng.randint(*RANGO_MONEDA[1]),
            *TAM_MONEDA,
        )
        for _ in range(config.MONEDAS_POR_NIVEL)
    ]

    return {
        "fragmentos": fragmentos,
        "monedas": monedas,
        "enemigos": enemigos,
        "trampas": trampas,
        "puerta": puerta,
    }
