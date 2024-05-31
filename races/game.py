import random
import arcade
import time

SCREEN_WIDTH = 1000 #  ШИРИНА ЭКРАНА
SCREEN_HEIGHT = 700 #  ВЫСОТА ЭКРАНА
SCREEN_TITLE = "гонки" 
BG_IMG = "races/images/road.jpg" # название текстуры
LOST_IMG ="races/images/Game over.png"
HERO_IMG = "races/images/hero.png"
HERO_SIZE = 0.13
HERO_SPEED = 10
STOP_1 = "races/images/stop1.png"
STOP_2 = "races/images/stop2.png"

STOP_1SIZE = 0.1
STOP1_SPEED = 8

STOP_2SIZE = 1
STOP2_SPEED = 8

LEFT_SUBURB = -25
RIGHT_SUBURB = SCREEN_WIDTH
HERO_ANGLE = -90

class Hero(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        if self.right > RIGHT_SUBURB:
            self.right = RIGHT_SUBURB
        if self.left < LEFT_SUBURB :
            self.left = LEFT_SUBURB
    
        
class Stop(arcade.Sprite):
    def update(self):
        self.center_y-= self.change_y
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT
            self.center_x = random.randint(LEFT_SUBURB,RIGHT_SUBURB)
            
    

class GameWindow(arcade.Window):
    def __init__(self, width, height, title): # конструктор - вызывается при создании объекта
        super().__init__(width, height, title)
        self.bg = arcade.load_texture(BG_IMG)   # сама текстура
        self.hero = Hero(HERO_IMG, HERO_SIZE)
        self.stop1 = Stop(STOP_1, STOP_1SIZE)
        self.stop2 = Stop(STOP_2, STOP_2SIZE)
        self.lost = False
        self.win = False
        self.lost_bg = arcade.load_texture(LOST_IMG)
        self.start = time.time()
        
        
    def setup(self): # начальные кординаты
        self.hero.center_x = SCREEN_WIDTH/4
        self.hero.center_y = SCREEN_HEIGHT/5
        self.hero.angle = HERO_ANGLE
        self.stop1.center_x = random.randint(LEFT_SUBURB,RIGHT_SUBURB)
        self.stop1.center_y = SCREEN_HEIGHT - 10
        self.stop1.change_y = STOP1_SPEED
        
        self.stop2.center_x = random.randint(LEFT_SUBURB,RIGHT_SUBURB)
        self.stop2.center_y = SCREEN_HEIGHT - 100
        self.stop2.change_y = STOP2_SPEED
    
    def on_draw(self):
        arcade.draw_texture_rectangle(center_x=SCREEN_WIDTH/2,
                                      center_y=SCREEN_HEIGHT/2,
                                      width=SCREEN_WIDTH,
                                      height=SCREEN_HEIGHT,
                                      texture=self.bg)
        self.hero.draw()
        self.stop1.draw()
        self.stop2.draw()
        if self.lost:
            arcade.draw_texture_rectangle(center_x=SCREEN_WIDTH/2,
                                      center_y=SCREEN_HEIGHT/2,
                                      width=SCREEN_WIDTH/2,
                                      height=SCREEN_HEIGHT/2,
                                      texture=self.lost_bg)
        if self.score/60 == 1:
             arcade.draw_text(f"winnier",
                            start_x=500,
                            start_y=300,
                            color = (0, 0,0),
                            font_size=36,
                            bold = True,
                            italic = True)
        
    
    def on_update(self, delta_time: float): # смена кадров и игровая логика
        if not self.lost and not self.win:
            self.hero.update()
            self.stop1.update()
            self.stop2.update()
            while arcade.check_for_collision(self.stop1,self.stop2):
                self.stop1.center_x = random.randint(LEFT_SUBURB,RIGHT_SUBURB)
            if arcade.check_for_collision(self.stop1, self.hero):
                self.lost = True
            if arcade.check_for_collision(self.stop2, self.hero):
                self.lost = True
            self.end = time.time()
            self.score =int(self.end - self.start)
        if self.score/60 == 1:
            self.win == True
        
        
    
    # нажатие клавиши
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.hero.change_x = HERO_SPEED
            self.hero.angle = HERO_ANGLE-25
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.hero.change_x = -HERO_SPEED
            self.hero.angle = HERO_ANGLE+25
    # отжатие клавиши
    def on_key_release(self, symbol: int, modifiers: int):
        self.hero.change_x = 0
        self.hero.angle = HERO_ANGLE
        

window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
window.setup() # вызывает метод setup
arcade.run()  # запускает цикл обработки событий    
    