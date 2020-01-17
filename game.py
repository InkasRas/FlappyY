import pygame
import sys
from random import randint, choice
from Objects.bird import Bird
from Objects.blocks import TopBlock, BottomBlock, Circle, ExtraSpeed, Ghost, FixWidth


class MainGame:
    def __init__(self, screen, clock, screen_size):
        self.FPS = 60
        self.screen = screen
        self.screen_size = screen_size
        self.clock = clock
        self.ability_accept = False
        self.score = 0
        self.speed = None
        self.ON = 31
        self.ability = None
        self.ghost = False
        self.DRAW_CIRCLES = 30
        self.circles = list()

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
                    pygame.display.flip()
                    if self.score // 50 % 2 == 1 and self.score != 0:
                        self.screen.fill((0, 0, 0))
                    else:
                        self.screen.fill((255, 255, 255))
                    self.update_all()
                    pygame.time.wait(1500)
                    print('STOP+')
                if event.key == pygame.K_SPACE:
                    if 30 < self.bird_obj.rect.y < 630:
                        self.bird_obj.y -= 30
            if event.type == self.DRAW_CIRCLES:
                self.circles.clear()
                for i in range(randint(10, 30)):
                    self.circles.append(Circle(self.screen))
            if event.type == self.ON:
                self.ability_accept = False
                self.ability = None
                self.speed = None
                self.ghost = False

    def start_game(self):
        pygame.time.set_timer(self.DRAW_CIRCLES, 2300)
        self.ability = None
        self.speed = None
        self.ghost = False
        self.ability_accept = False
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

        self.all_sprites.update(self.score, self.speed)
        for circle in self.circles:
            circle.update(self.score)
        if (pygame.sprite.spritecollide(self.bird_obj, self.top_blocks_sprites, False,
                                        pygame.sprite.collide_mask) or pygame.sprite.spritecollide(
            self.bird_obj, self.bottom_blocks_sprites, False,
            pygame.sprite.collide_mask)) and not self.ghost:
            self.game_over()
        if self.ability is not None:
            if pygame.sprite.spritecollide(self.bird_obj, self.abilities, False,
                                           pygame.sprite.collide_mask):
                self.all_sprites.remove(self.ability)
                self.ability_accept = True
                if type(self.ability) == ExtraSpeed:
                    self.speed = 6
                elif type(self.ability) == Ghost:
                    self.ghost = True
                self.ON = 31
                pygame.time.set_timer(self.ON, 10000)

        if self.bb.rect.x < self.screen_size[0] / 2 and self.tb.rect.x < self.screen_size[1] / 2:
            self.create_new_blocks()
            if self.ability is not None and self.ability_accept:
                if type(self.ability) == ExtraSpeed:
                    self.score += 3
            self.score += 1

    def create_new_blocks(self):
        h = randint(85, 440)
        self.tb = TopBlock(940, 0, h)
        self.top_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites.add(self.tb)
        self.all_sprites.add(self.tb)
        width = randint(100, 150)
        if self.ability is not None and self.ability_accept:
            if type(self.ability) == FixWidth:
                width = 180
        if randint(0, 100) >= 1 and not self.ability_accept:
            self.ability = choice([Ghost, ExtraSpeed, FixWidth])(940, h + width / 2 - 20)
            self.abilities = pygame.sprite.Group()
            self.abilities.add(self.ability)
            self.all_sprites.add(self.ability)
        self.bb = BottomBlock(940, h + width, self.screen_size[1] - h - width)
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
                        self.start_game()
                    if event.key == pygame.K_BACKSPACE:
                        self.terminate()
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
            if self.score // 50 % 2 == 1 and self.score != 0:
                self.screen.fill((0, 0, 0))
            else:
                self.screen.fill((255, 255, 255))
            self.get_events()
            self.update_all()
            self.show_message('Счет: ' + str(self.score), 30, 30, (0, 0, 0), 30)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
