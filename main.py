import pygame
from menu import Menu

pygame.init()
screen_size = width, height = (900, 650)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_icon(pygame.image.load('Extra Files/Images/1.png'))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
pygame.display.set_caption('FlappyY')

menu_obj = Menu(screen, screen_size, clock)
menu_obj.menu()