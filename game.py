import pygame
import sys
from random import randint

pygame.init()
screen_size = width, height = (900, 650)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()


class MainGame:
    def __init__(self):
        self.FPS = 60
        self.score = 0
        self.end_game = False
        self.speed = 10

    def terminate(self):
        pygame.quit()
        sys.exit()

    def get_events(self):
        for event in pygame.event.get():
            clock.tick(self.FPS)
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.ESC_RETURN:
                    pass

    def start(self):
        pygame.display.flip()
        while True:
            self.get_events()
