import pygame
from random import randint


class Block(pygame.sprite.Sprite):  # Класс с общими свойствами блоков
    def __init__(self, file_name, x, y, w, h):
        super().__init__()
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, score, speed=None):  # Обновления состояния блоков
        self.rect.x -= 4 + score // 10 if speed is None else speed
        self.mask = pygame.mask.from_surface(self.image)


class TopBlock(Block):  # Класс для верхней части преграды
    def __init__(self, x, y, h):
        super().__init__('Extra files/Images/tp.png', x, y, 100, h)


class BottomBlock(Block):  # Класс для нижней части преграды
    def __init__(self, x, y, h):
        super().__init__('Extra files/Images/bp.png', x, y, 100, h)


class Circle:  # Класс для кругов на заднем плане
    def __init__(self, screen):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.screen = screen
        self.x = randint(10, 950)
        self.y = randint(10, 640)
        self.size = randint(50, 90)

    def update(self, score, speed=None):  # Обновления состояние круга и его перерисовка
        self.x -= 4 + score // 10 if speed is None else speed
        self.size -= 1
        if self.size < 0:
            self.size = 0
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)


class Ghost(Block):
    # Класс для способности призрак: позволяет проходить через препятствия, не задевая их
    def __init__(self, x, y):
        super().__init__('Extra Files/Images/ghost.png', x, y, 40, 40)


class ExtraSpeed(Block):
    # Класс для способности дополнительной скорости: делает постоянную скорость = 6
    def __init__(self, x, y):
        super().__init__('Extra Files/Images/speed.png', x, y, 40, 40)


class FixWidth(Block):
    # Класс для способности "фиксированная ширина":
    # делает расстояние между нижним и верхни препятствием const = 180
    def __init__(self, x, y):
        super().__init__('Extra Files/Images/fixwidth.png', x, y, 40, 40)
