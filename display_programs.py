import pygame
from utils.constants import *
from datetime import datetime
import pytz


class ImageDisplay:
    def __init__(self, screen, image_path_list, len_of_display=5):
        """
        :param screen: Pygame surface to update with image from program
        :param image_path_list: List of image paths for display
        :param len_of_display: How long to display each image in image path list, seconds
        """
        self.done = False
        self.screen = screen
        self.image_num = 0
        self.max_image_num = len(image_path_list) - 1
        self.image_path_list = image_path_list
        self.DISPLAY_TIME = len_of_display * 1000  # Convert to ms

        self.phase_time = pygame.time.get_ticks()
        self.image = pygame.image.load(image_path_list[self.image_num]).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.screen.blit(self.image, (0, 0))

        self.image_path_list = image_path_list

    def update(self):
        if pygame.time.get_ticks() - self.phase_time > self.DISPLAY_TIME:
            self.change_image()
        return self.done

    def change_image(self):
        self.phase_time = pygame.time.get_ticks()
        self.image_num += 1
        if self.image_num > self.max_image_num:
            self.done = True
        else:
            self.image = pygame.image.load(self.image_path_list[self.image_num])
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            self.image = self.image.convert()

            self.screen.blit(self.image, (0, 0))

    def start(self):
        self.done = False
        self.image_num = 0
        self.phase_time = pygame.time.get_ticks()
        self.image = pygame.image.load(self.image_path_list[self.image_num]).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.screen.blit(self.image, (0, 0))




class CalDisplay:
    def __init__(self, screen, event_times, events):
        self.done = False

        self.screen = screen
        self.event_times = event_times
        self.events = events

        # flags
        self.phase = 0  # keeps track of the phase of the display sequence
        self.phase_done = False
        self.timer_start = True

        # timers
        self.phase_time = pygame.time.get_ticks()

        # render text for the screen
        self.font_title = pygame.font.Font(r"VeraMono.ttf", 12)
        self.font_title.underline = True
        self.font = pygame.font.Font(r"VeraMono.ttf", 10)
        # create sprites for each event and time
        self.text_sprites = pygame.sprite.Group()
        self.title = self.text_sprite("Calendar", self.font_title, (WIDTH/2, 6), BLUE, center=True)
        self.text_sprites.add(self.title)

        # get height and space width of font
        space = self.font.size(' ')[0]
        font_height = self.font.size('A')[1]

        x = 0
        y = 18
        self.event_times = event_times
        for i in range(len(event_times)):
            # show the first 4 calendar events of the day
            time_sprite = self.text_sprite(self.event_times[i], self.font, (x, y), BLUE)
            self.text_sprites.add(time_sprite)
            x_size = time_sprite.rect.size[0]

            x += (x_size + space)
            event_sprite = self.text_sprite(self.events[i], self.font, (x, y), BLUE)
            self.text_sprites.add(event_sprite)

            if event_sprite.rect.size[0] + x > WIDTH:
                self.long_text = True

            # reset x,y positions
            x = 0
            y += font_height

            if i == 3:
                break

    def update(self):
        self.screen.fill(BLACK)

        if self.phase == 0:
            if pygame.time.get_ticks() - self.phase_time > 5000:
                self.phase = 1

        elif self.phase == 1:
            if self.check_done_moving():
                self.phase = 2
            self.text_sprites.update()

        elif self.phase == 2:
            if self.timer_start:
                self.phase_time = pygame.time.get_ticks()
                self.timer_start = False

            if pygame.time.get_ticks() - self.phase_time > 3000:
                self.done = True

        # draw to screen
        self.text_sprites.draw(self.screen)
        return self.done

    def check_done_moving(self):
        # assume done until otherwise
        done = True
        for sprite in self.text_sprites:
            if sprite.rect.right > WIDTH:
                done = False
                break
        return done

    class text_sprite(pygame.sprite.Sprite):
        def __init__(self, text, font, position, color, center=False):
            pygame.sprite.Sprite.__init__(self)
            self.text = text
            self.image = font.render(text, False, color)
            self.rect = self.image.get_rect()

            if center:
                self.rect.center = position
            else:
                self.rect.topleft = position

            if self.rect.right > WIDTH:
                self.needs_move = True

        def update(self):
            self.rect.move_ip(-2, 0)

    def start(self):
        self.done = False

        # flags
        self.phase = 0  # keeps track of the phase of the display sequence
        self.phase_done = False
        self.timer_start = True

        # timers
        self.phase_time = pygame.time.get_ticks()

        # render text for the screen
        self.font_title = pygame.font.Font(r"VeraMono.ttf", 12)
        self.font_title.underline = True
        self.font = pygame.font.Font(r"VeraMono.ttf", 10)
        # create sprites for each event and time
        self.text_sprites = pygame.sprite.Group()
        self.title = self.text_sprite("Calendar", self.font_title, (WIDTH/2, 6), BLUE, center=True)
        self.text_sprites.add(self.title)

        # get height and space width of font
        space = self.font.size(' ')[0]
        font_height = self.font.size('A')[1]

        x = 0
        y = 18

        for i in range(len(self.event_times)):
            # show the first 4 calendar events of the day
            time_sprite = self.text_sprite(self.event_times[i], self.font, (x, y), BLUE)
            self.text_sprites.add(time_sprite)
            x_size = time_sprite.rect.size[0]

            x += (x_size + space)
            event_sprite = self.text_sprite(self.events[i], self.font, (x, y), BLUE)
            self.text_sprites.add(event_sprite)

            if event_sprite.rect.size[0] + x > WIDTH:
                self.long_text = True

            # reset x,y positions
            x = 0
            y += font_height

            if i == 3:
                break

class TimeDisplay:
    def __init__(self, screen, temp_image, temp, stock_names, stock_prices, background_path=None, tz='US/Eastern'):
        self.done = False

        self.screen = screen
        # render all the text and add to the pygame sprites
        self.font_time = pygame.font.Font(r"VeraMono.ttf", 20)
        self.font_stocks = pygame.font.Font(r"VeraMono.ttf", 10)
        self.font_temp = pygame.font.Font(r"VeraMono.ttf", 14)
        self.sprites = pygame.sprite.Group()

        # timers
        self.phase_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.num_phases = len(stock_names)

        # time
        self.tz = pytz.timezone(tz)
        self.current_time = datetime.now(tz=self.tz).strftime("%H:%M")
        self.time_sprite = self.text_sprite(self.current_time, self.font_time, (WIDTH/2, HEIGHT/2), WHITE, center=True)
        self.sprites.add(self.time_sprite)

        # stocks
        self.stock_names = stock_names
        self.stock_prices = stock_prices
        self.disp_stock_num = 0
        self.stock_sprite = self.text_sprite(f"{self.stock_names[self.disp_stock_num]} {self.stock_prices[self.disp_stock_num]}", self.font_stocks, (WIDTH / 2, 8), WHITE, center=True)
        self.sprites.add(self.stock_sprite)

        # weather
        self.temp = str(temp)
        self.temp_sprite = self.text_sprite(self.temp + "F", self.font_temp, (WIDTH/4, HEIGHT*7/8), WHITE, center=True)
        self.sprites.add(self.temp_sprite)
        self.temp_image = temp_image
        self.temp_image_sprite = self.image_sprite(self.temp_image, (WIDTH*3/4, 54), center=True)
        self.sprites.add(self.temp_image_sprite)

        # background
        if background_path:
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.background = self.background.convert()
        else:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(BLACK)


    def change_stock(self):
        self.disp_stock_num += 1
        if self.disp_stock_num == self.num_phases:
            self.disp_stock_num = 0
        else:
            self.stock_sprite.kill()
            self.stock_sprite = self.text_sprite(f"{self.stock_names[self.disp_stock_num]} {self.stock_prices[self.disp_stock_num]}", self.font_stocks, (WIDTH / 2, 8), WHITE, center=True)
            self.sprites.add(self.stock_sprite)
            self.phase_time = pygame.time.get_ticks()

    def update(self):
        self.screen.blit(self.background, (0,0))
        now = datetime.now(tz=self.tz)
        self.current_time = now.strftime("%H:%M")
        self.time_sprite.update_text(self.current_time)

        if pygame.time.get_ticks() - self.phase_time > 5000:
            self.change_stock()

        if pygame.time.get_ticks() - self.start_time > 40000:
            self.done = True
            
        # draw to screen
        self.sprites.draw(self.screen)
        return self.done


    class text_sprite(pygame.sprite.Sprite):
        def __init__(self, text, font, position, color, center=False):
            # defaults to the top left
            pygame.sprite.Sprite.__init__(self)
            self.font = font
            self.text = text
            self.color = color
            self.position = position
            self.center = center

            self.image = font.render(text, False, color)
            self.rect = self.image.get_rect()

            if center:
                self.rect.center = position
            else:
                self.rect.topleft = position

        def update_text(self, text):
            self.text = text
            self.image = self.font.render(text, False, self.color)
            self.rect = self.image.get_rect()

            if self.center:
                self.rect.center = self.position
            else:
                self.rect.topleft = self.position

    class image_sprite(pygame.sprite.Sprite):
        def __init__(self, image, position, center=False):
            # defaults to the top left
            mode = image.mode
            size = image.size
            data = image.tobytes()

            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.fromstring(data, size, mode)
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.rect = self.image.get_rect()

            if center:
                self.rect.center = position
            else:
                self.rect.topleft = position

    def start(self):
        self.done = False

        # timers
        self.phase_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()


class SpotifyDisplay:
    def __init__(self, screen, image):
        self.screen = screen

        self.mode = None
        self.size = None
        self.data = None
        self.image = None

    def update(self, image):
        self.mode = image.mode
        self.size = image.size
        self.data = image.tobytes()

        self.image = pygame.image.fromstring(self.data, self.size, self.mode)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.screen.blit(self.image, (0, 0))


