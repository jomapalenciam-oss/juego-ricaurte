"""Música de fondo generada por código (sin archivos externos).

Los .wav se escriben en la carpeta temporal del sistema, NO en el repositorio.
Se generan una sola vez por nivel y quedan cacheados en disco entre partidas.
"""

import array
import math
import os
import sys
import tempfile
import wave

import pygame

from juego.config import NIVEL_MAX

FRECUENCIA_MUESTREO = 44100
DURACION_PISTA = 8.0
VOLUMEN = 0.22

NOTAS = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}

PROGRESIONES = [
    ["C", "E", "G", "C"],
    ["A", "C", "E", "A"],
    ["D", "F", "A", "D"],
    ["G", "B", "D", "G"],
    ["E", "G", "B", "E"],
    ["C", "F", "A", "C"],
]


def carpeta_temporal():
    """Carpeta donde se guardan las pistas generadas."""
    ruta = os.path.join(tempfile.gettempdir(), "buho_ricaurte_audio")
    os.makedirs(ruta, exist_ok=True)
    return ruta


def generar_pista(nivel):
    """Genera (o reutiliza) el .wav del nivel. Devuelve la ruta o None."""
    ruta = os.path.join(carpeta_temporal(), "matrix_classical_%d.wav" % nivel)

    if os.path.exists(ruta):
        return ruta

    try:
        sr = FRECUENCIA_MUESTREO
        duracion = DURACION_PISTA
        total = int(sr * duracion)

        progresion = PROGRESIONES[(nivel - 1) % len(PROGRESIONES)]
        bpm = 68 + nivel * 3
        beat = 60.0 / bpm

        dos_pi = 2.0 * math.pi
        muestras = []

        for k in range(total):
            t = k / sr
            indice = int(t / beat)
            frecuencia = NOTAS[progresion[indice % len(progresion)]]

            # Cada cuarto tiempo sube una octava.
            if indice % 4 == 2:
                frecuencia *= 2

            valor = 0.15 * math.sin(dos_pi * frecuencia * t)
            valor += 0.07 * math.sin(dos_pi * (frecuencia / 2) * t)

            if indice % 2 == 1:
                valor += 0.035 * math.sin(dos_pi * (frecuencia * 1.5) * t)

            # Envolvente: entrada suave al principio, salida suave al final.
            ataque = min(1.0, t / 0.2)
            salida = min(1.0, (duracion - t) / 0.7)
            valor *= ataque * salida

            muestra = int(max(-1.0, min(1.0, valor)) * 32767)
            muestras.append(muestra)
            muestras.append(muestra)  # canal derecho (mismo audio)

        # `array` empaqueta los enteros de golpe: `struct.pack` obligaría a
        # pasar cientos de miles de argumentos sueltos.
        datos = array.array("h", muestras)
        if sys.byteorder == "big":
            datos.byteswap()  # el formato WAV es little-endian

        with wave.open(ruta, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(datos.tobytes())

        return ruta

    except (OSError, wave.Error, ValueError, OverflowError):
        # Sin permisos de escritura o sin espacio: el juego sigue sin música.
        return None


class Musica:
    """Controla la música de fondo. Si el mezclador falla, no hace nada."""

    @staticmethod
    def preparar():
        """Configura el mezclador ANTES de `pygame.init()`.

        `pygame.init()` arranca el mezclador con valores por defecto; si se
        llama a `mixer.init()` después, los parámetros se ignoran. `pre_init`
        es la forma correcta de fijarlos.
        """
        try:
            pygame.mixer.pre_init(frequency=FRECUENCIA_MUESTREO, size=-16,
                                  channels=2, buffer=512)
        except pygame.error:
            pass

    def __init__(self):
        self.activa = False
        self._cache = {}
        self._nivel_actual = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=FRECUENCIA_MUESTREO, size=-16,
                                  channels=2, buffer=512)
            self.activa = pygame.mixer.get_init() is not None
        except pygame.error:
            self.activa = False

    def cambiar(self, nivel):
        """Reproduce en bucle la pista del nivel indicado."""
        if not self.activa or nivel == self._nivel_actual:
            return

        if not 1 <= nivel <= NIVEL_MAX:
            return

        if nivel not in self._cache:
            self._cache[nivel] = generar_pista(nivel)

        ruta = self._cache[nivel]
        if not ruta:
            return

        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(VOLUMEN)
            pygame.mixer.music.play(-1)
            self._nivel_actual = nivel
        except pygame.error:
            self.activa = False

    def detener(self):
        if not self.activa:
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
