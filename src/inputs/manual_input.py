from typing import Optional, Tuple
import pygame

Angles = Tuple[float, float, float]

class ManualInput:
    """
    Uses keyboard to adjust angles:
      Q/A -> J1 +/-
      W/S -> J2 +/-
      E/D -> J3 +/-
      ESC -> quit
    Returns angles every tick.
    """

    def __init__(self, start: Angles = (90.0, 90.0, 90.0), step: float = 1.0):
        self.a1, self.a2, self.a3 = start
        self.step = step
        self.running = True

    def next(self) -> Optional[Angles]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]: self.a1 += self.step
        if keys[pygame.K_a]: self.a1 -= self.step
        if keys[pygame.K_w]: self.a2 += self.step
        if keys[pygame.K_s]: self.a2 -= self.step
        if keys[pygame.K_e]: self.a3 += self.step
        if keys[pygame.K_d]: self.a3 -= self.step

        if not self.running:
            return None

        return (self.a1, self.a2, self.a3)

    def close(self):
        pass
