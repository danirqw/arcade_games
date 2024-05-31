import arcade
import random
 # КОНСТАНТЫ , НОСТРОЙКИ
SCREEN_WIDTH = 1000 #  ШИРИНА ЭКРАНА
SCREEN_HEIGHT = 600 #  ШИРИНА ЭКРАНА
SCREEN_TITLE = "пинг-понг" 


BALL_SPEEDX = 4
BALL_SPEEDY = -4
BALL_IMG = "ping-pong/ball.png"
BALL_SIZE = 0.2

PADDLE_IMG = "ping-pong/paddle.png"
PADDLE_SIZE = 0.1
PADDLE_SPEED = 10
SPEED_UP = 0.1
FAILS = 2



class Ball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x # меняем кординату x
        self.center_y += self.change_y # меняем кординату y
        if self.right > SCREEN_WIDTH or self.left < 0: # если касаеться левой или правой стороны
            self.change_x =- self.change_x # меняет направдление
            self.color =(75, 75, 75)
            if self.change_x > 0: # если летит направа
                self.change_x += SPEED_UP
            else: #если летит налево
                self.change_x -= SPEED_UP
            if self.change_y > 0: # если летит направа
                self.change_y += SPEED_UP
            else: #если летит налево
                self.change_y -= SPEED_UP
                
        if self.top > SCREEN_HEIGHT or self.bottom < 0:
            self.change_y =- self.change_y
            self.color = (0, 235, 255)

class Paddle(arcade.Sprite):
    def update (self):
        self.center_x += self.change_x
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        
        


class GameWindow(arcade.Window):
    def __init__(self, width, height, title): # конструктор - вызывается при создании объекта
        super().__init__(width, height, title)
        self.ball = Ball(BALL_IMG,BALL_SIZE)
        self.paddle = Paddle(PADDLE_IMG, PADDLE_SIZE)
        self.count = 0
        self.fails = FAILS
        self.game = True
        
    def setup(self): # начальные кординаты
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT /2
        self.ball.change_x = BALL_SPEEDX
        self.ball.change_y = BALL_SPEEDY
        self.paddle.center_x = SCREEN_WIDTH / 2
        self.paddle.center_y = SCREEN_HEIGHT / 6
        

    def on_draw(self):
        arcade.start_render()  # начало отрисовки
        arcade.set_background_color((177, 215, 22))
        self.ball.draw()
        self.paddle.draw()
        arcade.draw_text(f"Счёт :{self.count}",
                         start_x=SCREEN_WIDTH -100,
                         start_y=SCREEN_HEIGHT -30,
                         color = arcade.color.BISTRE_BROWN,
                         font_size=16,
                         bold = True,
                         italic = True)
        arcade.draw_text(f"проигрыши: {self.fails}",
                         start_x=100,
                         start_y=SCREEN_HEIGHT -30,
                         color = arcade.color.BISTRE_BROWN,
                         font_size=16,
                         bold = True,
                         italic = True)
        if self.fails ==0:
            arcade.set_background_color((0, 0, 0))
            arcade.draw_text(f"Game over",
                            start_x=500,
                            start_y=300,
                            color = (255, 255,255),
                            font_size=36,
                            bold = True,
                            italic = True)
        if self.count ==20:
            arcade.set_background_color((255, 255, 255))
            arcade.draw_text(f"winnier:",
                            start_x=500,
                            start_y=300,
                            color = (0, 0,0),
                            font_size=36,
                            bold = True,
                            italic = True)        
        
    def on_update(self, delta_time: float): # смена кадров и игровая логика
        if self.game:
            self.ball.update()
            self.paddle.update()
            if arcade.check_for_collision(self.ball, self.paddle):
                self.ball.change_y = -self.ball.change_y
                self.ball.change_x = random.uniform(self.ball.change_x-5, self.ball.change_x+5) # (-5, 5)
                # while self.ball.change_x == 0:
                #      self.ball.change_x = random.uniform(-self.ball.change_x, self.ball.change_x+1) # (-5, 5)
                self.ball.bottom = self.paddle.top
                self.count += 1
            if self.ball.bottom < 0: # если мяч упал
                self.fails -=1 # отнимается попытки
                self.setup() # рестарт
            if self.fails == 0:
                self.game = False
            if self.count ==20:
                self.game=False
    # нажатие на клавише
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.paddle.change_x = PADDLE_SPEED
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.paddle.change_x = -PADDLE_SPEED
    def on_key_release(self, symbol: int, modifiers: int):
        self.paddle.change_x = 0
    
window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
window.setup() # вызывает метод setup
arcade.run()  # запускает цикл обработки событий