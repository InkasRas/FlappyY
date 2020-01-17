import pygame
import sys
from game import MainGame


class Menu:  # Класс для главного меню
    def __init__(self, screen, screen_size, clock):
        self.screen = screen
        self.FPS = 60
        self.screen_size = screen_size
        self.clock = clock

    def show_message(self, text, x, y, color, size):  # Функция для отображения сообщений
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        message_text = self.font.render(text, 1, color)
        message_rect = message_text.get_rect()
        message_rect.center = x, y
        self.screen.blit(message_text, (message_rect.center))

    def terminate(self):  # Закрытие программы
        pygame.quit()
        sys.exit()

    def menu(self):  # Работа и отображение меню
        menu_status = True
        bird_image = pygame.image.load('Extra Files/Images/1.png')
        bird_image = pygame.transform.scale(bird_image, (150, 125))
        bird_rect = bird_image.get_rect()
        bird_rect.x, bird_rect.y = self.screen_size[0] / 2 - 75, 15
        while menu_status:
            mouse = pygame.mouse.get_pos()
            self.screen.blit(bird_image, bird_rect)
            for event in pygame.event.get():
                self.clock.tick(self.FPS)
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_size[0] / 2 + 100 > mouse[0] > self.screen_size[0] / 2 - 100 and \
                            375 > mouse[1] > 300:
                        game = MainGame(self.screen, self.clock, self.screen_size)
                        while True:
                            game.start_game()
                            game.start()
                    if self.screen_size[0] / 2 + 100 > mouse[0] > self.screen_size[0] / 2 - 100 and \
                            475 > mouse[1] > 400:
                        self.terminate()
            self.show_message(f'Рекорд: {open("Extra Files/record.txt").readline()}',
                              self.screen_size[0] - 200, 50, (200, 200, 200), 30)
            self.show_message('FlappyY', self.screen_size[0] / 2 - 145, 175, (255, 255, 255), 90)

            if self.screen_size[0] / 2 + 100 > mouse[0] > self.screen_size[0] / 2 - 100 and \
                    375 > mouse[1] > 300:
                pygame.draw.rect(self.screen, (25, 0, 51),
                                 (self.screen_size[0] / 2 - 100, 300, 200, 75))
                self.show_message('Начать игру', self.screen_size[0] / 2 - 75, 330,
                                  (153, 0, 0), 25)
            else:
                pygame.draw.rect(self.screen, (64, 64, 64),
                                 (self.screen_size[0] / 2 - 100, 300, 200, 75))
                self.show_message('Начать игру', self.screen_size[0] / 2 - 75, 330,
                                  (255, 255, 255), 25)

            if self.screen_size[0] / 2 + 100 > mouse[0] > self.screen_size[0] / 2 - 100 and \
                    475 > mouse[1] > 400:
                pygame.draw.rect(self.screen, (25, 0, 51),
                                 (self.screen_size[0] / 2 - 100, 400, 200, 75))
                self.show_message('Выйти из игры', self.screen_size[0] / 2 - 75, 430,
                                  (153, 0, 0), 25)
            else:
                pygame.draw.rect(self.screen, (64, 64, 64),
                                 (self.screen_size[0] / 2 - 100, 400, 200, 75))
                self.show_message('Выйти из игры', self.screen_size[0] / 2 - 75, 430,
                                  (255, 255, 255), 25)

            self.show_message('Developed by Smirnov Ivan', 15, self.screen_size[1] - 20,
                              (128, 128, 128), 25)

            pygame.display.flip()
