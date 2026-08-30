"""Pantallas completas: menú, selección de personaje, historia, pregunta,
pausa, victoria y derrota.

Todas reciben `(pantalla, fuentes, juego)` y solo dibujan.
"""

import pygame

from juego import config
from juego.config import (
    ALTO, ANCHO, BLANCO, CIAN, DORADO, GRIS, MORADO2, ROJO,
)
from juego.dibujo import APARIENCIAS, dibujar_buho, envolver, texto

# Los rectángulos de las respuestas son fijos: se definen una vez y los usan
# tanto el dibujo como la detección de clic. En el original se obtenían
# volviendo a dibujar toda la pantalla desde el bucle de eventos.
BOTONES_RESPUESTA = [
    pygame.Rect(145, 300 + i * 72, 910, 56) for i in range(4)
]

LETRAS = ["A", "B", "C", "D"]

CREDITOS = [
    "JOSE PALENCIA",
    "JUAN PIÑERO",
    "JUAN JOSE RODRIGUEZ",
    "CARLOS FERNANDEZ",
]

HISTORIA_LINEAS = [
    "El Búho ha despertado dentro de una Matrix educativa.",
    "Los guardianes han escondido fragmentos del conocimiento.",
    "Cada respuesta correcta abre un nuevo camino.",
    "Pero los desafíos se harán cada vez más difíciles.",
    "",
    "Supera los 6 niveles, consigue la llave dorada",
    "y encuentra la puerta final para escapar.",
    "",
    "Fallar una pregunta no te quita vidas: solo puntos.",
    "Cuidado con las trampas y los guardianes.",
]


def _estrellas(pantalla, color, cantidad, paso_x, paso_y, alto_max):
    """Fondo de estrellas determinista (no parpadea entre frames)."""
    for i in range(cantidad):
        x = (i * paso_x + 40) % ANCHO
        y = (i * paso_y + 70) % alto_max
        pygame.draw.circle(pantalla, color, (x, y), 1 + (i % 3))


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def menu(pantalla, fuentes, juego):
    pantalla.fill((8, 9, 17))
    _estrellas(pantalla, (80, 90, 115), 45, 83, 47, 600)

    texto(pantalla, "LAS AVENTURAS", fuentes.titulo, BLANCO, 600, 75)
    texto(pantalla, "DEL BÚHO", fuentes.titulo, DORADO, 600, 135)
    texto(pantalla, "Juego creado por", fuentes.peq, GRIS, 600, 190)
    texto(pantalla, "Colegio Diocesano Ricaurte", fuentes.grande, DORADO,
          600, 230)

    dibujar_buho(pantalla, (600, 335), APARIENCIAS[juego.apariencia])

    texto(pantalla, "ESCAPE DE LA MATRIX", fuentes.grande, CIAN, 600, 430)

    pygame.draw.rect(pantalla, (35, 35, 55), (330, 465, 540, 60),
                     border_radius=18)
    texto(pantalla, "ENTER  •  Comenzar aventura", fuentes.normal, BLANCO,
          600, 495)

    texto(pantalla, "C  •  Personalizar personaje", fuentes.peq, GRIS, 600, 550)
    texto(pantalla, "WASD / FLECHAS  •  Moverse", fuentes.peq, GRIS, 600, 580)
    texto(pantalla, "P  •  Pausa     ESC  •  Salir", fuentes.peq, GRIS,
          600, 610)

    if config.DEBUG:
        texto(pantalla, "MODO DESARROLLO ACTIVO (F6/F7 disponibles)",
              fuentes.mini, ROJO, 600, 730)


# ---------------------------------------------------------------------------
# Selección de personaje
# ---------------------------------------------------------------------------

def personaje(pantalla, fuentes, juego):
    pantalla.fill((13, 14, 25))

    texto(pantalla, "PERSONALIZA TU BÚHO", fuentes.titulo, DORADO, 600, 70)
    texto(pantalla, "Usa ← → para cambiar y ENTER para confirmar",
          fuentes.peq, GRIS, 600, 115)

    for i, apariencia in enumerate(APARIENCIAS):
        x = 180 + i * 270
        marco = pygame.Rect(x, 170, 230, 340)

        pygame.draw.rect(pantalla, (35, 35, 52), marco, border_radius=20)
        if i == juego.apariencia:
            pygame.draw.rect(pantalla, CIAN, marco, 4, border_radius=20)

        texto(pantalla, apariencia["nombre"], fuentes.peq, BLANCO,
              x + 115, 205)

        dibujar_buho(pantalla, (x + 115, 355), apariencia, escala=1.5)

        if i == juego.apariencia:
            texto(pantalla, "ELEGIDO", fuentes.peq, CIAN, x + 115, 480)


# ---------------------------------------------------------------------------
# Historia
# ---------------------------------------------------------------------------

def historia(pantalla, fuentes, juego):
    pantalla.fill((8, 9, 17))

    texto(pantalla, "LA ÚLTIMA PUERTA", fuentes.titulo, DORADO, 600, 90)

    for i, linea in enumerate(HISTORIA_LINEAS):
        texto(pantalla, linea, fuentes.normal, BLANCO, 600, 170 + i * 40)

    texto(pantalla, "ENTER  •  Comenzar", fuentes.normal, DORADO, 600, 665)


# ---------------------------------------------------------------------------
# Pregunta
# ---------------------------------------------------------------------------

def pregunta(pantalla, fuentes, juego):
    pantalla.fill((8, 9, 18))

    actual = juego.pregunta_actual
    if actual is None:
        return

    texto(pantalla, "DESAFÍO — NIVEL %d" % juego.nivel,
          fuentes.grande, CIAN, 600, 70)
    texto(pantalla, actual["categoria"], fuentes.peq, DORADO, 600, 110)

    pygame.draw.rect(pantalla, (27, 28, 45), (80, 145, 1040, 490),
                     border_radius=25)

    for i, linea in enumerate(envolver(actual["pregunta"],
                                       fuentes.normal, 900)):
        texto(pantalla, linea, fuentes.normal, BLANCO, 600, 195 + i * 32)

    raton = pygame.mouse.get_pos()

    for i, boton in enumerate(BOTONES_RESPUESTA):
        resaltado = boton.collidepoint(raton)
        fondo = (60, 90, 125) if resaltado else (45, 45, 65)

        pygame.draw.rect(pantalla, fondo, boton, border_radius=14)
        pygame.draw.rect(pantalla, (100, 105, 135), boton, 2, border_radius=14)

        # La letra se genera aquí, después de barajar, para que siempre
        # coincida con la posición real de la opción.
        etiqueta = "%s)  %s" % (LETRAS[i], actual["opciones"][i])
        texto(pantalla, etiqueta, fuentes.normal, BLANCO,
              boton.x + 20, boton.y + 15, False)

    texto(pantalla, "Haz clic, o pulsa 1-4 o A-D para responder",
          fuentes.peq, GRIS, 600, 670)


# ---------------------------------------------------------------------------
# Pausa
# ---------------------------------------------------------------------------

def pausa(pantalla, fuentes, juego):
    pantalla.fill((8, 8, 15))

    texto(pantalla, "PAUSA", fuentes.titulo, DORADO, 600, 180)
    texto(pantalla, "P  •  Continuar", fuentes.normal, BLANCO, 600, 300)
    texto(pantalla, "ESC  •  Salir", fuentes.normal, GRIS, 600, 350)

    texto(pantalla, "Nivel %d/%d — %s" % (juego.nivel, config.NIVEL_MAX,
                                          config.NOMBRES[juego.nivel]),
          fuentes.peq, GRIS, 600, 430)
    texto(pantalla, "Puntos: %d    Fragmentos: %d/%d    Vidas: %d"
          % (juego.puntos, juego.fragmentos,
             config.FRAGMENTOS_OBJETIVO, juego.vidas),
          fuentes.peq, GRIS, 600, 465)


# ---------------------------------------------------------------------------
# Victoria y derrota
# ---------------------------------------------------------------------------

def victoria(pantalla, fuentes, juego):
    pantalla.fill((5, 25, 22))
    _estrellas(pantalla, DORADO, 50, 97, 53, ALTO)

    texto(pantalla, "¡ESCAPASTE DE LA MATRIX!", fuentes.titulo, DORADO, 600, 65)
    texto(pantalla, "LA AVENTURA HA TERMINADO", fuentes.grande, CIAN, 600, 120)
    texto(pantalla, "La llave abrió la última puerta.", fuentes.normal,
          BLANCO, 600, 165)
    texto(pantalla, "PUNTUACIÓN FINAL: %d" % juego.puntos,
          fuentes.grande, DORADO, 600, 215)

    pygame.draw.line(pantalla, CIAN, (350, 255), (850, 255), 3)

    texto(pantalla, "CRÉDITOS", fuentes.titulo, BLANCO, 600, 295)
    texto(pantalla, "Juego creado por", fuentes.peq, GRIS, 600, 340)

    for i, nombre in enumerate(CREDITOS):
        texto(pantalla, nombre, fuentes.normal, BLANCO, 600, 385 + i * 40)

    pygame.draw.line(pantalla, MORADO2, (400, 540), (800, 540), 2)

    texto(pantalla, "Colegio Diocesano Ricaurte", fuentes.grande, DORADO,
          600, 580)
    texto(pantalla, "¡Gracias por jugar!", fuentes.normal, CIAN, 600, 625)
    texto(pantalla, "ENTER  •  Jugar otra vez", fuentes.peq, GRIS, 600, 680)


def derrota(pantalla, fuentes, juego):
    pantalla.fill((45, 8, 18))

    texto(pantalla, "EL BÚHO HA CAÍDO", fuentes.titulo, ROJO, 600, 190)
    texto(pantalla, "Los guardianes de la Matrix fueron demasiado fuertes.",
          fuentes.normal, BLANCO, 600, 290)
    texto(pantalla, "Llegaste al nivel %d: %s"
          % (juego.nivel, config.NOMBRES[juego.nivel]),
          fuentes.peq, GRIS, 600, 335)
    texto(pantalla, "Puntuación: %d" % juego.puntos,
          fuentes.grande, DORADO, 600, 400)
    texto(pantalla, "ENTER  •  Intentar nuevamente", fuentes.normal, BLANCO,
          600, 500)
