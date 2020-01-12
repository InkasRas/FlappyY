import pygame
from game import MainGame

pygame.init()
screen_size = width, height = (900, 650)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

game = MainGame(screen, clock, screen_size)
while True:
    game.start()
