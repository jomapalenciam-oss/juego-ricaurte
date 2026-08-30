"""Bucle principal: arranque de pygame, eventos y dibujo por estado."""

import pygame

from juego import config, hud, pantallas
from juego.audio import Musica
from juego.dibujo import APARIENCIAS, dibujar_buho
from juego.escenario import dibujar_objetos, fondo_nivel
from juego.estado import Juego
from juego.fuentes import Fuentes


def _teclas_respuesta():
    """Teclas que responden una pregunta: números, teclado numérico y A-D.

    Los nombres del teclado numérico cambiaron entre versiones de pygame, así
    que se buscan con `getattr` y se ignoran los que no existan.
    """
    mapa = {}
    nombres = [
        ("K_1", "K_KP1", "K_KP_1", "K_a"),
        ("K_2", "K_KP2", "K_KP_2", "K_b"),
        ("K_3", "K_KP3", "K_KP_3", "K_c"),
        ("K_4", "K_KP4", "K_KP_4", "K_d"),
    ]
    for indice, grupo in enumerate(nombres):
        for nombre in grupo:
            tecla = getattr(pygame, nombre, None)
            if tecla is not None:
                mapa[tecla] = indice
    return mapa


TECLAS_RESPUESTA = _teclas_respuesta()

# Si un frame tarda muchísimo (por ejemplo mientras se genera la música), se
# limita el delta para que nadie atraviese paredes de golpe.
DT_MAXIMO = 0.05


class Aplicacion:
    """Une pygame, el estado del juego y las pantallas."""

    def __init__(self):
        Musica.preparar()
        pygame.init()

        self.pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
        pygame.display.set_caption(config.TITULO)

        self.reloj = pygame.time.Clock()
        self.fuentes = Fuentes()
        self.musica = Musica()
        self.juego = Juego()
        self.ejecutando = True

    # ------------------------------------------------------------------
    # Arranque
    # ------------------------------------------------------------------

    def aplicar_argumento(self, argumento):
        """Atajos de prueba por línea de comandos (solo con DEBUG activo)."""
        if not config.DEBUG:
            return False

        argumento = argumento.lower()
        if argumento == "nivel6":
            self.saltar_a_nivel_final(con_llave=False)
            return True
        if argumento == "final":
            self.saltar_a_nivel_final(con_llave=True)
            return True
        return False

    def saltar_a_nivel_final(self, con_llave):
        juego = self.juego
        juego.entrar_a_nivel(config.NIVEL_MAX)
        juego.vidas = config.VIDAS_INICIALES
        juego.estado = config.JUGANDO

        if con_llave:
            juego.fragmentos = config.FRAGMENTOS_OBJETIVO
            juego.fragmentos_nivel = []
            juego.llave = True
            juego.mostrar_mensaje(
                "MODO PRUEBA: nivel 6 con la llave. Ve a la puerta.")
        else:
            juego.mostrar_mensaje(
                "MODO PRUEBA: nivel 6. Encuentra los fragmentos.")

    def ejecutar(self):
        while self.ejecutando:
            dt = min(self.reloj.tick(config.FPS) / 1000.0, DT_MAXIMO)

            self.procesar_eventos()

            if self.juego.estado == config.JUGANDO:
                self.juego.actualizar(dt, pygame.key.get_pressed())

            self.dibujar()
            pygame.display.flip()

            # Va después de pintar: generar una pista nueva tarda un momento y
            # así la ventana nunca aparece congelada mientras se crea.
            self.musica.cambiar(self.juego.nivel)

        self.cerrar()

    def cerrar(self):
        self.musica.detener()
        pygame.quit()

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------

    def procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                self.tecla_pulsada(evento.key)

            elif (evento.type == pygame.MOUSEBUTTONDOWN
                  and evento.button == 1
                  and self.juego.estado == config.PREGUNTA):
                self.clic_respuesta(evento.pos)

    def tecla_pulsada(self, tecla):
        juego = self.juego

        if tecla == pygame.K_ESCAPE:
            self.ejecutando = False
            return

        if config.DEBUG:
            if tecla == pygame.K_F6:
                self.saltar_a_nivel_final(con_llave=False)
                return
            if tecla == pygame.K_F7:
                self.saltar_a_nivel_final(con_llave=True)
                return

        if juego.estado == config.MENU:
            if tecla == pygame.K_RETURN:
                juego.reiniciar()
            elif tecla == pygame.K_c:
                juego.estado = config.PERSONAJE

        elif juego.estado == config.PERSONAJE:
            if tecla == pygame.K_LEFT:
                juego.apariencia = (juego.apariencia - 1) % len(APARIENCIAS)
            elif tecla == pygame.K_RIGHT:
                juego.apariencia = (juego.apariencia + 1) % len(APARIENCIAS)
            elif tecla == pygame.K_RETURN:
                juego.estado = config.MENU

        elif juego.estado == config.HISTORIA:
            if tecla == pygame.K_RETURN:
                juego.estado = config.JUGANDO

        elif juego.estado == config.JUGANDO:
            if tecla == pygame.K_p:
                juego.estado = config.PAUSA
            elif tecla == pygame.K_e:
                juego.interactuar()
            elif tecla == pygame.K_SPACE:
                juego.intentar_dash()

        elif juego.estado == config.PREGUNTA:
            if tecla in TECLAS_RESPUESTA:
                juego.responder(TECLAS_RESPUESTA[tecla])

        elif juego.estado == config.PAUSA:
            if tecla == pygame.K_p:
                juego.estado = config.JUGANDO

        elif juego.estado in (config.VICTORIA, config.DERROTA):
            if tecla == pygame.K_RETURN:
                juego.reiniciar()

    def clic_respuesta(self, posicion):
        for i, boton in enumerate(pantallas.BOTONES_RESPUESTA):
            if boton.collidepoint(posicion):
                self.juego.responder(i)
                return

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------

    def dibujar(self):
        estado = self.juego.estado

        if estado == config.JUGANDO:
            self.dibujar_partida()
            return

        pantalla_fn = {
            config.MENU: pantallas.menu,
            config.PERSONAJE: pantallas.personaje,
            config.HISTORIA: pantallas.historia,
            config.PREGUNTA: pantallas.pregunta,
            config.PAUSA: pantallas.pausa,
            config.VICTORIA: pantallas.victoria,
            config.DERROTA: pantallas.derrota,
        }.get(estado)

        if pantalla_fn:
            pantalla_fn(self.pantalla, self.fuentes, self.juego)

    def dibujar_partida(self):
        juego = self.juego

        fondo_nivel(self.pantalla, self.fuentes, juego.nivel)
        dibujar_objetos(self.pantalla, self.fuentes, juego)

        # Parpadeo mientras dura la invulnerabilidad tras recibir daño.
        visible = (juego.invulnerable <= 0
                   or int(juego.invulnerable * 12) % 2 == 0)
        if visible:
            dibujar_buho(self.pantalla, juego.jugador.center,
                         APARIENCIAS[juego.apariencia],
                         dash=juego.dash_t > 0)

        hud.interfaz(self.pantalla, self.fuentes, juego)
        hud.pista_interaccion(self.pantalla, self.fuentes, juego)
        hud.dibujar_mensaje(self.pantalla, self.fuentes, juego)
