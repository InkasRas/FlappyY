import pygame


class Bird(pygame.sprite.Sprite):  # Класс для объекта-птицы
    def __init__(self, x, y):
        super().__init__()
        self.count = 0
        self.images = [pygame.image.load('Extra Files/Images/' + str(i) + '.png') for i in
                       range(1, 5)]
        self.image = None
        self.change_image()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x = x
        self.y = y

    def change_image(self):
        self.image = self.images[self.count % 4]
        self.image = pygame.transform.scale(self.image, (85, 60))

    def update(self, score, speed=None):  # Обновления состояние птицы
        self.y += 3 + score // 20 * 0.4 if speed is None else 3.5
        if 30 < self.y < 630:
            self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
