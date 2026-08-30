"""Constantes de configuracion del juego.

Este modulo no importa pygame ni crea recursos: solo define valores.
Asi puede importarse desde cualquier parte sin efectos secundarios.
"""

import os


# ---------------------------------------------------------------------------
# Ventana
# ---------------------------------------------------------------------------

ANCHO = 1200
ALTO = 760
FPS = 60

TITULO = "Las Aventuras del Buho - Colegio Diocesano Ricaurte"


# ---------------------------------------------------------------------------
# Modo desarrollo
# ---------------------------------------------------------------------------
# Los atajos de prueba (F6 / F7) y los argumentos de linea de comandos
# ("nivel6", "final") solo funcionan con DEBUG activo. En la entrega final
# debe quedar desactivado para que no se pueda saltar el juego.
#
# Para activarlo durante el desarrollo:
#     Windows PowerShell:  $env:BUHO_DEBUG = "1"; python main.py
#     Linux / macOS:       BUHO_DEBUG=1 python main.py

DEBUG = os.environ.get("BUHO_DEBUG", "0") == "1"


# ---------------------------------------------------------------------------
# Paleta de colores
# ---------------------------------------------------------------------------

NEGRO = (10, 10, 18)
BLANCO = (245, 245, 250)
GRIS = (120, 125, 140)

VERDE = (35, 115, 65)
VERDE2 = (65, 165, 85)
VERDE3 = (18, 65, 40)

AZUL = (40, 105, 175)
AZUL2 = (80, 175, 235)

MORADO = (105, 65, 160)
MORADO2 = (165, 105, 230)

ROJO = (215, 55, 70)
AMARILLO = (245, 210, 75)
NARANJA = (235, 135, 55)

CIAN = (65, 220, 210)
ARENA = (190, 145, 80)
TIERRA = (105, 70, 45)
DORADO = (255, 225, 105)


# ---------------------------------------------------------------------------
# Estados de la maquina de estados principal
# ---------------------------------------------------------------------------

MENU = 0
PERSONAJE = 1
HISTORIA = 2
JUGANDO = 3
PREGUNTA = 4
PAUSA = 5
VICTORIA = 6
DERROTA = 7


# ---------------------------------------------------------------------------
# Reglas de juego
# ---------------------------------------------------------------------------

NIVEL_MAX = 6
FRAGMENTOS_OBJETIVO = 4
VIDAS_INICIALES = 3

MONEDAS_POR_NIVEL = 12
PUNTOS_MONEDA = 25

# Puntos por acertar: PUNTOS_BASE + nivel * PUNTOS_POR_NIVEL
PUNTOS_BASE = 100
PUNTOS_POR_NIVEL = 35

# Fallar una pregunta no cuesta vidas: resta puntos y deja reintentar con
# otra pregunta. Las vidas se pierden solo con enemigos y trampas.
PENALIZACION_ERROR = 50

# Velocidades en pixeles por SEGUNDO (el movimiento usa delta-time, no frames).
VELOCIDAD_JUGADOR = 270.0
MULTIPLICADOR_DASH = 2.2
DURACION_DASH = 0.22
ESPERA_DASH = 0.6
DURACION_INVULNERABLE = 1.5

# Invulnerabilidad al aparecer en un nivel nuevo.
GRACIA_ENTRADA = 1.2

DIAGONAL = 0.7071067811865476


# ---------------------------------------------------------------------------
# Geometria del escenario
# ---------------------------------------------------------------------------

# Rectangulo por el que puede moverse el jugador (x, y, ancho, alto).
ZONA_JUEGO = (55, 85, ANCHO - 110, ALTO - 155)

# Limites de rebote de los enemigos.
LIMITE_ENEMIGO_IZQ = 70
LIMITE_ENEMIGO_DER = 1130
LIMITE_ENEMIGO_ARRIBA = 95
LIMITE_ENEMIGO_ABAJO = 640

SPAWN_JUGADOR = (100, 110)
TAM_JUGADOR = 44

PUERTA = (1085, 580, 58, 70)

# Distancia minima (en pixeles inflados) que debe haber entre el punto de
# aparicion del jugador y cualquier objeto peligroso o interactuable.
MARGEN_SPAWN = 180


# ---------------------------------------------------------------------------
# Niveles
# ---------------------------------------------------------------------------

NOMBRES = {
    1: "Bosque del Conocimiento",
    2: "Desierto del Tiempo",
    3: "Ciudad del Saber",
    4: "Templo de los Recuerdos",
    5: "Abismo del Conocimiento",
    6: "La Puerta de la Matrix",
}

DIFICULTAD = {
    1: "Fácil",
    2: "Fácil+",
    3: "Media",
    4: "Media+",
    5: "Difícil",
    6: "Final",
}
