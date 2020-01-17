import pygame
from random import randint


class Block(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, h):
        super().__init__()
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (100, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, score, speed=None):
        self.rect.x -= 4 + score // 10 if speed is None else speed
        self.mask = pygame.mask.from_surface(self.image)


class TopBlock(Block):
    def __init__(self, x, y, h):
        super().__init__('Extra files/tp.png', x, y, h)


class BottomBlock(Block):
    def __init__(self, x, y, h):
        super().__init__('Extra files/bp.png', x, y, h)


class Circle:
    def __init__(self, screen):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.screen = screen
        self.x = randint(10, 950)
        self.y = randint(10, 640)
        self.size = randint(50, 90)

    def update(self, score, speed=None):
        self.x -= 4 + score // 10 if speed is None else speed
        self.size -= 1
        if self.size < 0:
            self.size = 0
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)


class Abilities(pygame.sprite.Sprite):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, score, speed=None):
        self.rect.x -= 4 + score // 10 if speed is None else speed
        self.mask = pygame.mask.from_surface(self.image)


class Ghost(Abilities):
    def __init__(self, x, y):
        super().__init__(x, y, 'Extra Files/ghost.png')


class ExtraSpeed(Abilities):
    def __init__(self, x, y):
        super().__init__(x, y, 'Extra Files/speed.png')


class FixWidth(Abilities):
    def __init__(self, x, y):
        super().__init__(x, y, 'Extra Files/fixwidth.png')
