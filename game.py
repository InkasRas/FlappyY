import pygame
import sys
from random import randint
from Objects.bird import Bird
from Objects.blocks import TopBlock, BottomBlock


class MainGame:
    def __init__(self, screen, clock, screen_size):
        self.FPS = 60
        self.screen = screen
        self.screen_size = screen_size
        self.clock = clock
        self.score = 0
        self.end_game = False
        self.speed = 10

    def terminate(self):
        pygame.quit()
        sys.exit()

    def show_message(self, text, x, y, color, size):
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        message_text = self.font.render(text, 1, color)
        message_rect = message_text.get_rect()
        message_rect.center = x / 2, y / 2
        self.screen.blit(message_text, (message_rect.center))

    def get_events(self):
        for event in pygame.event.get():
            self.clock.tick(self.FPS)
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.pause()

    def start_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.bottom_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites = pygame.sprite.Group()
        # self.bird = Bird()
        h = randint(85, 500)
        tb = TopBlock(650, 0, h)
        self.all_sprites.add(tb)
        self.top_blocks_sprites.add(tb)
        bb = BottomBlock(650, h + 80, self.screen_size[1] - h - 80)
        self.all_sprites.add(bb)
        self.top_blocks_sprites.add(bb)

    def pause(self):
        pause_status = True
        while pause_status:
            for event in pygame.event.get():
                self.clock.tick(self.FPS)
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause_status = False
            self.show_message('Пауза', self.screen_size[0] // 2, self.screen_size[1] // 2,
                              (10, 10, 255), 40)
            pygame.display.flip()

    def start(self):
        while True:
            self.start_game()
            self.get_events()
            self.show_message('Счет: ' + str(self.score), 30, 30, (0, 0, 0), 30)
            pygame.display.flip()

