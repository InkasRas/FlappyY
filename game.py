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
        self.DRAW_CIRCLES = 30
        self.draw_circles_timer = pygame.time.set_timer(self.DRAW_CIRCLES, 900)

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
                if event.key == pygame.K_SPACE:
                    if 30 < self.bird_obj.rect.y < 630:
                        self.bird_obj.y -= 30
            if event.type == self.DRAW_CIRCLES:
                for i in range(randint(10, 30)):
                    pygame.draw.circle(self.screen,
                                       (randint(0, 255), randint(0, 255), randint(0, 255)),
                                       (randint(10, 890), randint(10, 640)), randint(10, 60))

    def start_game(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.bottom_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites = pygame.sprite.Group()
        self.bird_obj = Bird(self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.all_sprites.add(self.bird_obj)
        h = randint(85, 350)
        self.tb = TopBlock(950, 0, h)
        self.all_sprites.add(self.tb)
        self.top_blocks_sprites.add(self.tb)
        random_width = randint(110, 140)
        self.bb = BottomBlock(950, h + random_width, self.screen_size[1] - h - random_width)
        self.all_sprites.add(self.bb)
        self.top_blocks_sprites.add(self.bb)

    def update_all(self):
        self.all_sprites.update(self.score)
        if pygame.sprite.spritecollide(self.bird_obj, self.top_blocks_sprites, False,
                                       pygame.sprite.collide_mask) or pygame.sprite.spritecollide(
            self.bird_obj, self.bottom_blocks_sprites, False,
            pygame.sprite.collide_mask):
            self.game_over()

        if self.bb.rect.x < self.screen_size[0] / 2 and self.tb.rect.x < self.screen_size[1] / 2:
            self.create_new_blocks()
            self.score += 1

    def create_new_blocks(self):
        h = randint(85, 440)
        self.tb = TopBlock(940, 0, h)
        self.top_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites.add(self.tb)
        self.all_sprites.add(self.tb)
        random_width = randint(100, 150)
        self.bb = BottomBlock(940, h + random_width, self.screen_size[1] - h - random_width)
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
            self.show_message('Пауза', self.screen_size[0] / 2 - 80, self.screen_size[1] / 2,
                              (10, 10, 255), 80)
            pygame.display.flip()

    def game_over(self):
        print('Game Over')
        game_over = True
        while game_over:
            self.screen.fill((255, 255, 255))
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
            self.show_message('ИГРА ОКОНЧЕНА', self.screen_size[0] / 2 - 225,
                              self.screen_size[1] / 2 - 100,
                              (201, 0, 0),
                              70)
            self.show_message('Счет: ' + str(self.score), self.screen_size[0] / 2 - 50,
                              self.screen_size[1] / 2 + 20, (0, 0, 0), 45)

            pygame.display.flip()

            # mouse = pygame.mouse.get_pos()
            # if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
            #     pygame.draw.rect(self.screen, (10, 255, 40), (150, 450, 100, 50))
            # else:
            #     pygame.draw.rect(self.screen, (0, 255, 0), (150, 450, 100, 50))

    def start(self):
        while True:
            self.screen.fill((255, 255, 255))
            self.get_events()
            self.update_all()
            self.show_message('Счет: ' + str(self.score), 30, 30, (0, 0, 0), 30)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
