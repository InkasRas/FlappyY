import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Extra files/1.png')
        self.image = pygame.transform.scale(self.image, (85, 60))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x = x
        self.y = y

    def update(self, score):
        self.y += 3 + score // 20 * 0.4
        if 30 < self.y < 630:
            self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
