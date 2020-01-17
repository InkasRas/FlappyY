import pygame
import sys
from random import randint, choice
from Objects.bird import Bird
from Objects.blocks import TopBlock, BottomBlock, Circle, ExtraSpeed, Ghost, FixWidth


class MainGame:  # Логика игры
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

    def terminate(self):  # Закрытие программы
        pygame.quit()
        sys.exit()

    def show_message(self, text, x, y, color, size):  # Функция для отображения сообщений
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        message_text = self.font.render(text, 1, color)
        message_rect = message_text.get_rect()
        message_rect.center = x, y
        self.screen.blit(message_text, (message_rect.center))

    def get_events(self):  # Функция для получения событий и их обработки
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
                    pygame.time.wait(700)
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_SPACE:
                    if 30 < self.bird_obj.rect.y < 630:
                        self.bird_obj.y -= 30
                    self.bird_obj.count += 3
                    self.bird_obj.change_image()
            if event.type == self.DRAW_CIRCLES:
                self.circles.clear()
                for i in range(randint(10, 30)):
                    self.circles.append(Circle(self.screen))
            if event.type == self.ON:
                self.ability_accept = False
                self.ability = None
                self.speed = None
                self.ghost = False
            if event.type == self.music_stopped:
                self.start_music()

    def start_game(self):  # Функция для запуска или перезапуска игры
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
        self.start_music()

    def update_all(self):  # Функция для обновления экрана
        self.all_sprites.update(self.score, self.speed)
        for circle in self.circles:
            circle.update(self.score)
        if (pygame.sprite.spritecollide(self.bird_obj, self.top_blocks_sprites, False,
                                        pygame.sprite.collide_mask) or pygame.sprite.spritecollide(
            self.bird_obj, self.bottom_blocks_sprites, False,
            pygame.sprite.collide_mask)) and not self.ghost:
            self.game_over()
        if self.ability is not None and not self.ability_accept:
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

    def create_new_blocks(self):  # Функия для создания новых препрятсвий и блоков со способностями
        h = randint(85, 440)
        self.tb = TopBlock(940, 0, h)
        self.top_blocks_sprites = pygame.sprite.Group()
        self.top_blocks_sprites.add(self.tb)
        self.all_sprites.add(self.tb)
        width = randint(100, 150)
        if self.ability is not None and self.ability_accept:
            if type(self.ability) == FixWidth:
                width = 180
        if randint(0, 100) >= 80 and not self.ability_accept:
            self.ability = choice([Ghost, ExtraSpeed, FixWidth])(970, h + width / 2 - 20)
            self.abilities = pygame.sprite.Group()
            self.abilities.add(self.ability)
            self.all_sprites.add(self.ability)
        self.bb = BottomBlock(940, h + width, self.screen_size[1] - h - width)
        self.bottom_blocks_sprites = pygame.sprite.Group()
        self.bottom_blocks_sprites.add(self.bb)
        self.all_sprites.add(self.bb)

    def pause(self):  # Функиця, запускающая паузу
        pause_status = True
        pause_image = pygame.image.load('Extra Files/Images/pause.png')
        pause_image = pygame.transform.scale(pause_image, (80, 60))
        pause_rect = pause_image.get_rect()
        pause_rect.x, pause_rect.y = self.screen_size[0] / 2 - 180, self.screen_size[1] / 4 + 20

        pygame.mixer.music.pause()
        while pause_status:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        250 > mouse[0] > 50 and 576 > mouse[1] > 500:
                    pause_status = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        850 > mouse[0] > 650 and 576 > mouse[1] > 500:
                    pause_status = False
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and pause_status:
                        pause_status = False
                    if event.key == pygame.K_BACKSPACE:
                        self.terminate()
            self.screen.blit(pause_image, pause_rect)
            self.show_message('Пауза', self.screen_size[0] / 2 - 90, self.screen_size[1] / 4 + 25,
                              (10, 10, 255), 80)
            if self.score // 50 % 2 != 1:
                self.show_message('Счет: ' + str(self.score), self.screen_size[0] / 2 - 65,
                                  self.screen_size[1] / 2 + 15, (0, 0, 0), 45)
            else:
                self.show_message('Счет: ' + str(self.score), self.screen_size[0] / 2 - 65,
                                  self.screen_size[1] / 2 + 15, (255, 255, 255), 45)
            if 250 > mouse[0] > 50 and 576 > mouse[1] > 500:
                pygame.draw.rect(self.screen, (127, 0, 255), (50, 500, 200, 76))
                self.show_message('Продолжить', 75, 530, (30, 30, 30), 26)
            else:
                pygame.draw.rect(self.screen, (102, 102, 0), (50, 500, 200, 76))
                self.show_message('Продолжить', 75, 530, (0, 0, 0), 26)

            if 850 > mouse[0] > 650 and 576 > mouse[1] > 500:
                pygame.draw.rect(self.screen, (127, 0, 255), (650, 500, 200, 76))
                self.show_message('Выйти из игры', 675, 530, (10, 10, 10), 26)
            else:
                pygame.draw.rect(self.screen, (159, 0, 0), (650, 500, 200, 76))
                self.show_message('Выйти из игры', 675, 530, (0, 0, 0), 26)

            pygame.display.flip()

    def start_music(self):  # Функция для запуска музыки
        self.music_stopped = pygame.USEREVENT + 1
        pygame.mixer.init()
        pygame.mixer.music.set_endevent()
        pygame.mixer.music.load('Extra Files/Music/1.mp3')
        for i in range(2, 9):
            pygame.mixer.music.queue(f'Extra Files/Music/{i}.mp3')
        pygame.mixer.music.play()

    def game_over(self):  # Функиця, запускающая меню после поражения игрока
        pygame.mixer.music.stop()
        game_over = True
        record = int(open('Extra Files/record.txt', 'r').readline())
        skull_image = pygame.image.load('Extra Files/Images/skull.png')
        skull_image = pygame.transform.scale(skull_image, (150, 150))
        skull_image_rect = skull_image.get_rect()
        skull_image_rect.x, skull_image_rect.y = self.screen_size[0] / 2 - 70, self.screen_size[
            1] / 4 - 120

        if record < self.score:
            print(self.score, file=open('Extra Files/record.txt', 'w'))
        while game_over:
            mouse = pygame.mouse.get_pos()
            if self.score // 50 % 2 == 1 and self.score != 0:
                self.screen.fill((0, 0, 0))
            else:
                self.screen.fill((255, 255, 255))
            self.clock.tick(self.FPS)
            self.screen.blit(skull_image, skull_image_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        250 > mouse[0] > 50 and 576 > mouse[1] > 500:
                    game_over = False
                    self.start_game()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        850 > mouse[0] > 650 and 576 > mouse[1] > 500:
                    game_over = False
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
            if self.score // 50 % 2 != 1:
                self.show_message('Счет: ' + str(self.score), self.screen_size[0] / 2 - 65,
                                  self.screen_size[1] / 2 + 15, (0, 0, 0), 45)
            else:
                self.show_message('Счет: ' + str(self.score), self.screen_size[0] / 2 - 65,
                                  self.screen_size[1] / 2 + 15, (255, 255, 255), 45)
            self.show_message('Рекорд: ' + str(record),
                              self.screen_size[0] / 2 - 65, self.screen_size[1] / 2 + 55,
                              (0, 100, 160), 45)

            if 250 > mouse[0] > 50 and 576 > mouse[1] > 500:
                pygame.draw.rect(self.screen, (127, 0, 255), (50, 500, 200, 76))
                self.show_message('Начать заново', 75, 530, (10, 10, 10), 26)
            else:
                pygame.draw.rect(self.screen, (0, 159, 0), (50, 500, 200, 76))
                self.show_message('Начать заново', 75, 530, (0, 0, 0), 26)

            if 850 > mouse[0] > 650 and 576 > mouse[1] > 500:
                pygame.draw.rect(self.screen, (127, 0, 255), (650, 500, 200, 76))
                self.show_message('Выйти из игры', 675, 530, (30, 30, 30), 26)
            else:
                pygame.draw.rect(self.screen, (159, 0, 0), (650, 500, 200, 76))
                self.show_message('Выйти из игры', 675, 530, (0, 0, 0), 26)

            pygame.display.flip()

    def start(self):  # Фукнция постоянно запускающая функции, которые должны работать постоянно
        while True:
            if self.score // 50 % 2 == 1 and self.score != 0:
                self.screen.fill((0, 0, 0))
                self.show_message('Счет: ' + str(self.score), 30, 30, (255, 255, 255), 30)

            else:
                self.screen.fill((255, 255, 255))
                self.show_message('Счет: ' + str(self.score), 30, 30, (0, 0, 0), 30)
            self.get_events()
            self.update_all()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
