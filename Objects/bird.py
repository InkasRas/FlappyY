import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Extra files/1.png')
        self.image = pygame.transform.scale(self.image, (85, 60))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        delta_position_y = 3
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            delta_position_y = -4
        if 30 < self.rect.y < 630:
            self.rect.center = (self.rect.x, self.rect.y + delta_position_y)
        self.mask = pygame.mask.from_surface(self.image)
