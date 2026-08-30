"""Utilidades de dibujo y sprites del personaje.

Ninguna función de este módulo modifica el estado del juego: reciben lo que
necesitan por parámetro y solo pintan.
"""

import pygame

from juego.config import BLANCO, CIAN, VERDE, VERDE2, VERDE3, AMARILLO


APARIENCIAS = [
    {
        "nombre": "Búho clásico",
        "cuerpo": (48, 48, 58),
        "ojos": BLANCO,
        "pico": AMARILLO,
    },
    {
        "nombre": "Búho bosque",
        "cuerpo": (75, 125, 70),
        "ojos": (225, 245, 190),
        "pico": AMARILLO,
    },
    {
        "nombre": "Búho Matrix",
        "cuerpo": (45, 180, 145),
        "ojos": (180, 255, 235),
        "pico": CIAN,
    },
    {
        "nombre": "Búho nocturno",
        "cuerpo": (70, 55, 105),
        "ojos": (235, 220, 255),
        "pico": AMARILLO,
    },
]


def texto(pantalla, cadena, fuente, color, x, y, centro=True):
    """Dibuja una línea de texto. `centro` alinea al centro o arriba-izquierda."""
    superficie = fuente.render(cadena, True, color)
    if centro:
        rect = superficie.get_rect(center=(x, y))
    else:
        rect = superficie.get_rect(topleft=(x, y))
    pantalla.blit(superficie, rect)


def envolver(cadena, fuente, ancho_max):
    """Parte una cadena en líneas que quepan en `ancho_max` píxeles."""
    lineas = []
    actual = ""

    for palabra in cadena.split():
        prueba = (actual + " " + palabra).strip()
        if actual and fuente.size(prueba)[0] > ancho_max:
            lineas.append(actual)
            actual = palabra
        else:
            actual = prueba

    if actual:
        lineas.append(actual)

    return lineas


def dibujar_buho(pantalla, centro, apariencia, dash=False, escala=1.0):
    """Dibuja el búho centrado en `centro`.

    `apariencia` es uno de los diccionarios de APARIENCIAS.
    """
    x, y = centro
    cuerpo = apariencia["cuerpo"]
    ojos = apariencia["ojos"]
    pico = apariencia["pico"]

    def e(valor):
        return int(valor * escala)

    # Sombra
    pygame.draw.ellipse(pantalla, (0, 0, 0),
                        (x - e(24), y + e(18), e(48), e(12)))

    # Cuerpo
    pygame.draw.ellipse(pantalla, cuerpo,
                        (x - e(22), y - e(5), e(44), e(52)))

    # Alas
    pygame.draw.ellipse(pantalla, cuerpo,
                        (x - e(34), y + e(3), e(23), e(34)))
    pygame.draw.ellipse(pantalla, cuerpo,
                        (x + e(11), y + e(3), e(23), e(34)))

    # Cabeza
    pygame.draw.circle(pantalla, cuerpo, (x, y - e(20)), e(28))

    # Orejas
    pygame.draw.polygon(pantalla, cuerpo, [
        (x - e(23), y - e(36)),
        (x - e(16), y - e(60)),
        (x - e(3), y - e(37)),
    ])
    pygame.draw.polygon(pantalla, cuerpo, [
        (x + e(23), y - e(36)),
        (x + e(16), y - e(60)),
        (x + e(3), y - e(37)),
    ])

    # Ojos
    for ex in (x - e(10), x + e(10)):
        pygame.draw.circle(pantalla, ojos, (ex, y - e(20)), e(9))
        pygame.draw.circle(pantalla, (15, 15, 20), (ex, y - e(20)), e(4))

    # Pico
    pygame.draw.polygon(pantalla, pico, [
        (x - e(6), y - e(7)),
        (x + e(6), y - e(7)),
        (x, y + e(5)),
    ])

    # Brillo
    pygame.draw.circle(pantalla, BLANCO, (x - e(12), y - e(23)), max(1, e(2)))

    # Estela del impulso
    if dash:
        pygame.draw.circle(pantalla, CIAN, (x, y), e(34), 2)


def arbol(pantalla, x, y, s=1):
    """Dibuja un árbol decorativo con escala `s`."""
    pygame.draw.rect(pantalla, (75, 48, 30),
                     (x - 8 * s, y + 5 * s, 16 * s, 45 * s))
    pygame.draw.circle(pantalla, VERDE3, (x, y), int(30 * s))
    pygame.draw.circle(pantalla, VERDE,
                       (int(x - 20 * s), int(y + 4 * s)), int(24 * s))
    pygame.draw.circle(pantalla, VERDE2,
                       (int(x + 18 * s), int(y + 2 * s)), int(22 * s))
