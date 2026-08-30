"""Carga de tipografías.

Se agrupan en una clase porque `pygame.font.SysFont` solo puede llamarse
después de `pygame.init()`. Así el módulo se puede importar sin efectos
secundarios y las fuentes se crean cuando toca.
"""

import pygame


class Fuentes:
    """Conjunto de tipografías usadas en todo el juego."""

    def __init__(self, familia="arial"):
        self.titulo = pygame.font.SysFont(familia, 52, True)
        self.grande = pygame.font.SysFont(familia, 36, True)
        self.normal = pygame.font.SysFont(familia, 24)
        self.peq = pygame.font.SysFont(familia, 18)
        self.mini = pygame.font.SysFont(familia, 15)
