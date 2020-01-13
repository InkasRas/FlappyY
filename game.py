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
        self.last = pygame.time.get_ticks()
        self.end_game = False

    def terminate(self):
        pygame.quit()
        sys.exit()

    def show_message(self, text, x, y, color, size):
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        message_text = self.font.render(text, 1, color)
        message_rect = message_text.get_rect()
        message_rect.center = x, y
        self.screen.blit(message_text, (message_rect.center))

    def get_events(self):
        for event in pygame.event.get():
            self.clock.tick(self.FPS)
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause()
                    print('STOP+')

    def start_game(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.bottom_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites = pygame.sprite.Group()
        self.bird_obj = Bird(self.screen_size[0] / 2, screen_size[1] / 2)
        self.all_sprites.add(self.bird_obj)
        h = randint(85, 500)
        self.tb = TopBlock(750, 0, h)
        self.all_sprites.add(self.tb)
        self.top_blocks_sprites.add(self.tb)
        random_width = randint(100, 150)
        self.bb = BottomBlock(750, h + random_width, self.screen_size[1] - h - random_width)
        self.all_sprites.add(self.bb)
        self.top_blocks_sprites.add(self.bb)

    def update_all(self):
        self.all_sprites.update()
        if pygame.sprite.spritecollide(self.bird_obj, self.top_blocks_sprites, False,
                                       pygame.sprite.collide_mask) or pygame.sprite.spritecollide(
            self.bird_obj, self.bottom_blocks_sprites, False,
            pygame.sprite.collide_mask):
            self.game_over()

        if self.bb.rect.x < screen_size[0] / 2 and self.tb.rect.x < screen_size[1] / 2:
            self.create_new_blocks()
            self.score += 1

    def create_new_blocks(self):
        h = randint(85, 500)
        self.tb = TopBlock(740, 0, h)
        self.top_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites.add(self.tb)
        self.all_sprites.add(self.tb)
        random_width = randint(100, 150)
        self.bb = BottomBlock(740, h + random_width, self.screen_size[1] - h - random_width)
        self.bottom_blocks_sprites = pygame.sprite.Group()
        self.bottom_blocks_sprites.add(self.bb)
        self.all_sprites.add(self.bb)

    def pause(self):
        print('PAUSE START')
        pause_status = True
        while pause_status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and pause_status:
                        pause_status = False
                        print('STOP')
            self.show_message('Пауза', self.screen_size[0] / 2, (self.screen_size[1] - 300) / 2,
                              (10, 10, 255), 40)
            pygame.display.flip()

    def game_over(self):
        print('Game Over')
        game_over = True
        while game_over:
            self.show_message('ИГРА ОКОНЧЕНА', self.screen_size[0], self.screen_size[1], (100, 0, 0),
                              70)
            mouse = pygame.mouse.get_pos()
            if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
                pygame.draw.rect(self.screen, (10, 255, 40), (150, 450, 100, 50))
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), (150, 450, 100, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
            pygame.display.flip()

    def start(self):
        while True:
            self.get_events()
            self.update_all()
            self.all_sprites.draw(self.screen)
            self.show_message('Счет: ' + str(self.score), 30, 30, (0, 0, 0), 30)
            pygame.display.flip()


pygame.init()
screen_size = width, height = (900, 650)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
pygame.display.set_caption('FlappyY')

game = MainGame(screen, clock, screen_size)
while True:
    game.start_game()
    game.start()
