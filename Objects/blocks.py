import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, h):
        super().__init__()
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (100, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= 4
        self.mask = pygame.mask.from_surface(self.image)


class TopBlock(Block):
    def __init__(self, x, y, h):
        super().__init__('Extra files/tp.png', x, y, h)


class BottomBlock(Block):
    def __init__(self, x, y, h):
        super().__init__('Extra files/bp.png', x, y, h)
