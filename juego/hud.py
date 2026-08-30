"""Interfaz durante la partida: marcador, barra de progreso y avisos."""

import pygame

from juego import config
from juego.config import (
    ANCHO, BLANCO, CIAN, DORADO, GRIS, ROJO, VERDE2,
)
from juego.dibujo import envolver, texto

BARRA_ANCHO = 260
BARRA_Y = 650


def interfaz(pantalla, fuentes, juego):
    """Barra superior con el marcador y barra inferior con el progreso."""
    pygame.draw.rect(pantalla, (8, 10, 18), (0, 0, ANCHO, 70))

    texto(pantalla, "VIDAS: %d" % juego.vidas,
          fuentes.normal, ROJO, 25, 20, False)
    texto(pantalla, "PUNTOS: %d" % juego.puntos,
          fuentes.normal, DORADO, 180, 20, False)
    texto(pantalla, "FRAGMENTOS: %d/%d" % (juego.fragmentos,
                                           config.FRAGMENTOS_OBJETIVO),
          fuentes.normal, BLANCO, 360, 20, False)
    texto(pantalla, "NIVEL %d/%d" % (juego.nivel, config.NIVEL_MAX),
          fuentes.normal, CIAN, 610, 14, False)
    texto(pantalla, config.NOMBRES[juego.nivel],
          fuentes.peq, BLANCO, 790, 12, False)
    texto(pantalla, "Dificultad: %s" % config.DIFICULTAD[juego.nivel],
          fuentes.mini, GRIS, 790, 36, False)

    # Barra de fragmentos
    pygame.draw.rect(pantalla, (45, 45, 60),
                     (25, BARRA_Y, BARRA_ANCHO, 16), border_radius=8)
    progreso = min(1.0, juego.fragmentos / config.FRAGMENTOS_OBJETIVO)
    if progreso > 0:
        pygame.draw.rect(pantalla, CIAN,
                         (25, BARRA_Y, int(BARRA_ANCHO * progreso), 16),
                         border_radius=8)

    texto(pantalla, "E: interactuar   ESPACIO: impulso   P: pausa",
          fuentes.mini, GRIS, 305, BARRA_Y, False)

    if juego.nivel == config.NIVEL_MAX:
        texto(pantalla,
              "LLAVE: " + ("SÍ" if juego.llave else "NO"),
              fuentes.mini,
              DORADO if juego.llave else GRIS,
              1000, BARRA_Y, False)


def pista_interaccion(pantalla, fuentes, juego):
    """Texto de ayuda contextual encima de la barra inferior."""
    cerca = juego.objeto_cerca

    if cerca and cerca[0] == "fragmento":
        texto(pantalla, "E • Responder desafío",
              fuentes.peq, DORADO, 600, 626)
        return

    if cerca and cerca[0] == "puerta":
        if juego.puerta_abierta():
            etiqueta = ("E • ABRIR PUERTA FINAL"
                        if juego.nivel == config.NIVEL_MAX
                        else "E • Avanzar al siguiente nivel")
            texto(pantalla, etiqueta, fuentes.peq, VERDE2, 600, 626)
        else:
            texto(pantalla,
                  "Puerta cerrada: te faltan %d fragmentos"
                  % (config.FRAGMENTOS_OBJETIVO - juego.fragmentos),
                  fuentes.peq, GRIS, 600, 626)
        return

    if juego.puerta_abierta():
        texto(pantalla,
              "¡Ya tienes los fragmentos! Busca la puerta (abajo a la derecha).",
              fuentes.peq, DORADO, 600, 626)


def dibujar_mensaje(pantalla, fuentes, juego):
    """Aviso temporal. El temporizador lo descuenta `Juego.actualizar`."""
    if not juego.mensaje or juego.mensaje_t <= 0:
        return

    lineas = envolver(juego.mensaje, fuentes.peq, 660)
    alto = 20 + 24 * len(lineas)
    caja = pygame.Rect(0, 0, 700, alto)
    caja.midbottom = (600, 605)

    pygame.draw.rect(pantalla, (15, 15, 25), caja, border_radius=15)
    pygame.draw.rect(pantalla, (60, 62, 85), caja, 2, border_radius=15)

    for i, linea in enumerate(lineas):
        texto(pantalla, linea, fuentes.peq, BLANCO,
              600, caja.y + 22 + i * 24)
