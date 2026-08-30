"""Estado y reglas de la partida.

Toda la información mutable vive en la clase `Juego`. Los módulos de dibujo
solo la leen: no modifican nada. Así se elimina el uso de variables globales.
"""

import pygame

from juego import config, nivel as generador
from juego.preguntas import BancoPreguntas


class Juego:
    """Estado completo de una partida."""

    def __init__(self, banco=None):
        self.banco = banco or BancoPreguntas()

        self.jugador = pygame.Rect(0, 0, config.TAM_JUGADOR, config.TAM_JUGADOR)
        # Posición real en coma flotante: el Rect solo guarda enteros y
        # redondear en cada frame haría perder velocidad (bug del original).
        self._x = 0.0
        self._y = 0.0

        self.apariencia = 0

        self.fragmentos_nivel = []
        self.monedas = []
        self.enemigos = []
        self.trampas = []
        self.puerta = pygame.Rect(*config.PUERTA)

        self.reiniciar()
        # La partida arranca en el menú; `reiniciar` deja el estado en HISTORIA
        # porque también se usa al pulsar ENTER desde el menú o tras perder.
        self.estado = config.MENU

    # ------------------------------------------------------------------
    # Ciclo de vida de la partida
    # ------------------------------------------------------------------

    def reiniciar(self):
        """Vuelve al principio: nivel 1, marcador y vidas a cero."""
        self.estado = config.HISTORIA
        self.nivel = 1
        self.vidas = config.VIDAS_INICIALES
        self.puntos = 0
        self.fragmentos = 0
        self.llave = False

        self.mensaje = ""
        self.mensaje_t = 0.0

        self.invulnerable = 0.0
        self.dash_t = 0.0
        self.dash_espera = 0.0

        self.pregunta_actual = None
        self.objeto_actual = None
        self.objeto_cerca = None

        self.banco.reiniciar()
        self.entrar_a_nivel(1)

    def entrar_a_nivel(self, numero):
        """Genera el nivel indicado y coloca al jugador en la entrada."""
        self.nivel = numero
        self.fragmentos = 0
        self.llave = False

        contenido = generador.generar(numero)
        self.fragmentos_nivel = contenido["fragmentos"]
        self.monedas = contenido["monedas"]
        self.enemigos = contenido["enemigos"]
        self.trampas = contenido["trampas"]
        self.puerta = contenido["puerta"]

        self.pregunta_actual = None
        self.objeto_actual = None
        self.objeto_cerca = None
        self.dash_t = 0.0
        self.dash_espera = 0.0

        # Periodo de gracia al aparecer: aunque un enemigo se acerque a la
        # entrada, el jugador nunca recibe daño nada más empezar el nivel.
        self.invulnerable = config.GRACIA_ENTRADA

        self.colocar_en_entrada()

    def colocar_en_entrada(self):
        self.jugador.center = config.SPAWN_JUGADOR
        self._x = float(self.jugador.x)
        self._y = float(self.jugador.y)

    # ------------------------------------------------------------------
    # Mensajes en pantalla
    # ------------------------------------------------------------------

    def mostrar_mensaje(self, texto, segundos=2.5):
        self.mensaje = texto
        self.mensaje_t = segundos

    # ------------------------------------------------------------------
    # Actualización por frame (todo en función de dt, no de frames)
    # ------------------------------------------------------------------

    def actualizar(self, dt, teclas):
        self._mover_jugador(dt, teclas)
        self._mover_enemigos(dt)
        self._recoger_monedas()
        self._comprobar_peligros()

        # Se calcula una sola vez por frame y lo reutilizan el HUD y la tecla E.
        self.objeto_cerca = self._buscar_objeto_cercano()

        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.dash_t = max(0.0, self.dash_t - dt)
        self.dash_espera = max(0.0, self.dash_espera - dt)
        self.mensaje_t = max(0.0, self.mensaje_t - dt)

    def _mover_jugador(self, dt, teclas):
        dx = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - \
             (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
        dy = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - \
             (teclas[pygame.K_w] or teclas[pygame.K_UP])

        if dx == 0 and dy == 0:
            return

        if dx and dy:
            dx *= config.DIAGONAL
            dy *= config.DIAGONAL

        multiplicador = config.MULTIPLICADOR_DASH if self.dash_t > 0 else 1.0
        paso = config.VELOCIDAD_JUGADOR * multiplicador * dt

        self._x += dx * paso
        self._y += dy * paso

        self.jugador.x = round(self._x)
        self.jugador.y = round(self._y)

        antes = self.jugador.topleft
        self.jugador.clamp_ip(pygame.Rect(*config.ZONA_JUEGO))

        # Solo se resincroniza la posición flotante si el borde nos frenó;
        # si no, se perderían los decimales en cada frame.
        if self.jugador.topleft != antes:
            self._x = float(self.jugador.x)
            self._y = float(self.jugador.y)

    def _mover_enemigos(self, dt):
        for enemigo in self.enemigos:
            rect = enemigo["rect"]

            enemigo["x"] += enemigo["vx"] * dt
            enemigo["y"] += enemigo["vy"] * dt
            rect.x = round(enemigo["x"])
            rect.y = round(enemigo["y"])

            # Rebote: se reposiciona además de invertir, para que no quede
            # atascado invirtiendo la velocidad frame tras frame.
            if rect.left < config.LIMITE_ENEMIGO_IZQ:
                rect.left = config.LIMITE_ENEMIGO_IZQ
                enemigo["x"] = float(rect.x)
                enemigo["vx"] = abs(enemigo["vx"])
            elif rect.right > config.LIMITE_ENEMIGO_DER:
                rect.right = config.LIMITE_ENEMIGO_DER
                enemigo["x"] = float(rect.x)
                enemigo["vx"] = -abs(enemigo["vx"])

            if rect.top < config.LIMITE_ENEMIGO_ARRIBA:
                rect.top = config.LIMITE_ENEMIGO_ARRIBA
                enemigo["y"] = float(rect.y)
                enemigo["vy"] = abs(enemigo["vy"])
            elif rect.bottom > config.LIMITE_ENEMIGO_ABAJO:
                rect.bottom = config.LIMITE_ENEMIGO_ABAJO
                enemigo["y"] = float(rect.y)
                enemigo["vy"] = -abs(enemigo["vy"])

    def _recoger_monedas(self):
        restantes = []
        for moneda in self.monedas:
            if self.jugador.colliderect(moneda.inflate(12, 12)):
                self.puntos += config.PUNTOS_MONEDA
            else:
                restantes.append(moneda)
        self.monedas = restantes

    def _comprobar_peligros(self):
        if self.invulnerable > 0:
            return

        for trampa in self.trampas:
            if self.jugador.colliderect(trampa):
                self.recibir_dano()
                return

        for enemigo in self.enemigos:
            if self.jugador.colliderect(enemigo["rect"].inflate(-5, -5)):
                self.recibir_dano()
                return

    def recibir_dano(self):
        """Quita una vida, salvo que el jugador esté en periodo de gracia."""
        if self.invulnerable > 0:
            return

        self.vidas -= 1
        self.invulnerable = config.DURACION_INVULNERABLE
        self.mostrar_mensaje("¡Cuidado! Has perdido una vida.")

        if self.vidas <= 0:
            self.estado = config.DERROTA

    def intentar_dash(self):
        if self.dash_t <= 0 and self.dash_espera <= 0:
            self.dash_t = config.DURACION_DASH
            self.dash_espera = config.ESPERA_DASH

    # ------------------------------------------------------------------
    # Interacción con el escenario
    # ------------------------------------------------------------------

    def _buscar_objeto_cercano(self):
        for fragmento in self.fragmentos_nivel:
            if self.jugador.colliderect(fragmento.inflate(55, 55)):
                return ("fragmento", fragmento)

        if self.jugador.colliderect(self.puerta.inflate(45, 45)):
            return ("puerta", self.puerta)

        return None

    def puerta_abierta(self):
        return self.fragmentos >= config.FRAGMENTOS_OBJETIVO

    def interactuar(self):
        """Responde a la tecla E."""
        if self.objeto_cerca is None:
            return

        tipo = self.objeto_cerca[0]

        if tipo == "fragmento":
            self.objeto_actual = self.objeto_cerca
            self.abrir_pregunta()
        else:
            self.usar_puerta()

    def usar_puerta(self):
        if not self.puerta_abierta():
            self.mostrar_mensaje(
                "La puerta está cerrada. Fragmentos: %d/%d"
                % (self.fragmentos, config.FRAGMENTOS_OBJETIVO)
            )
            return

        if self.nivel < config.NIVEL_MAX:
            self.avanzar_nivel()
        else:
            self.llave = True
            self.estado = config.VICTORIA

    def avanzar_nivel(self):
        siguiente = self.nivel + 1
        self.entrar_a_nivel(siguiente)
        self.mostrar_mensaje(
            "¡Nivel %d! %s" % (siguiente, config.NOMBRES[siguiente])
        )

    # ------------------------------------------------------------------
    # Preguntas
    # ------------------------------------------------------------------

    def abrir_pregunta(self):
        self.pregunta_actual = self.banco.siguiente(self.nivel)
        if self.pregunta_actual:
            self.estado = config.PREGUNTA
        else:
            self.mostrar_mensaje("No hay preguntas disponibles para este nivel.")

    def responder(self, indice):
        """Procesa la opción elegida (0-3).

        Fallar NO cuesta vidas: resta puntos, muestra la explicación y deja
        reintentar el mismo fragmento con otra pregunta. Las vidas se pierden
        solo con enemigos y trampas.
        """
        pregunta = self.pregunta_actual

        if pregunta is None:
            self.estado = config.JUGANDO
            return

        self.pregunta_actual = None
        self.estado = config.JUGANDO

        if indice != pregunta["correcta"]:
            self.puntos = max(0, self.puntos - config.PENALIZACION_ERROR)
            self.objeto_actual = None
            self.mostrar_mensaje(
                "Incorrecto (-%d puntos). %s"
                % (config.PENALIZACION_ERROR, pregunta["explicacion"]),
                4.5,
            )
            return

        ganados = config.PUNTOS_BASE + self.nivel * config.PUNTOS_POR_NIVEL
        self.puntos += ganados

        self.mostrar_mensaje(
            "¡Correcto! +%d. %s" % (ganados, pregunta["explicacion"]),
            4.0,
        )

        # Va después: si se completan los fragmentos, su aviso es más
        # importante y debe sustituir al mensaje de "correcto".
        self._recoger_fragmento()

    def _recoger_fragmento(self):
        if not self.objeto_actual or self.objeto_actual[0] != "fragmento":
            return

        fragmento = self.objeto_actual[1]
        self.objeto_actual = None

        if fragmento not in self.fragmentos_nivel:
            return

        self.fragmentos_nivel.remove(fragmento)
        self.fragmentos += 1

        if not self.puerta_abierta():
            return

        if self.nivel == config.NIVEL_MAX:
            self.llave = True
            self.mostrar_mensaje(
                "¡LLAVE DORADA CONSEGUIDA! Ve a la puerta final y pulsa E.", 4.0
            )
        else:
            self.mostrar_mensaje(
                "¡Conseguiste los %d fragmentos! Busca la puerta."
                % config.FRAGMENTOS_OBJETIVO,
                4.0,
            )
