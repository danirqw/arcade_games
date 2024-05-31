import arcade
import random
import time
SCREEN_WIDTH = 1200 #  ШИРИНА ЭКРАНА
SCREEN_HEIGHT = 800 #  ШИРИНА ЭКРАНА
SCREEN_TITLE = "звёздные война" 
BG_IMG = "star_wars/textures/bg.jpg"
HERO_IMG ="star_wars/textures/hero.png"
LASER_IMG = "star_wars/textures/las.png"
ENEMW_LASER_IMG =  "star_wars/textures/laser.webp"
ENEMY_LASER_SIZE = 0.2
HERO_SIZE = 0.4
LASER_SIZE = 0.3
LASER_SPEED = 20
LASER_SOUND = "star_wars/sounds/laser_sound.mp3"
ENEMY_IMG = "star_wars/textures/enemy.png"
ENEMY_SIZE = 0.15
ENEMY_SPEED = 2
ENEMY_COUNT = 50
ENEMY_DIST = 100
PROGRESS_HEIGHT = 20


class EnemyLaser(arcade.Sprite):
    def __init__(self,enemy): # вызываеться, когда появляеться спрайт
        super().__init__(ENEMW_LASER_IMG, ENEMY_LASER_SIZE)
        self.enemy = enemy # сам враг
        self.center_x = self.enemy.center_x
        self.top = self.enemy.bottom
        self.change_y = LASER_SPEED / 2
        # self.sound = arcade.load_sound(LASER_SOUND)
    def update(self):
        self.center_y -= self.change_y
        if self.top < 0:
            self.kill()
class Laser(arcade.Sprite):
    def __init__(self): # вызываеться, когда появляеться спрайт
        super().__init__(LASER_IMG, LASER_SIZE)
        self.center_x = window.hero.center_x
        self.bottom = window.hero.top
        self.change_y = LASER_SPEED
        self .angle = 90
        self.sound = arcade.load_sound(LASER_SOUND)
    def update(self):
        self.center_y += self.change_y
        if self.bottom > SCREEN_HEIGHT:
            self.kill()
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(ENEMY_IMG, ENEMY_SIZE)
        self.center_x = random.randint(self.width/2, SCREEN_WIDTH - self.width/2)
        self.change_y = ENEMY_SPEED
        self.last_update = time.time() # старт
        self.fuse = random.uniform(2,4)
    def update(self):
        self.chexk_time = time.time()
        if self.chexk_time - self.last_update > self.fuse and self.center_y < SCREEN_HEIGHT:
            self.last_update = time.time() # старт
            laser = EnemyLaser(self)
            window.enemy_lasers.append(laser) #  добавляем в спрайт лист
        self.center_y -= self.change_y
        if self.top < 0 :
            self.kill()
class Hero(arcade.Sprite):
        def update(self):
            self.center_x += self.change_x
            if self.right > SCREEN_WIDTH:
                self.right = SCREEN_WIDTH
            if self.left < 0:
                self.left = 0
class GameWindow(arcade.Window):
    def __init__(self, width, height, title): # конструктор - вызывается при создании объекта
        super().__init__(width, height, title, center_window = True)    
        self.bg = arcade.load_texture(BG_IMG)
        self.hero = Hero(HERO_IMG, HERO_SIZE)
        self.lasers = arcade.SpriteList() #  список спрайтов 
        self.enemies = arcade.SpriteList() #  список врагов
        self.enemy_lasers = arcade.SpriteList() 
        self.lost = False
    def setup(self): # начальные кординаты
        self.hero.center_x = SCREEN_WIDTH/2
        self.hero.center_y = SCREEN_HEIGHT/12
        for i in range (ENEMY_COUNT): # ПОВТОРЯТЬ 50 РАЗ
            enemy = Enemy()
            enemy.center_y = SCREEN_HEIGHT + i * ENEMY_DIST
            self.enemies.append(enemy)
    def on_draw(self):
        arcade.start_render()  # начало отрисовки
        arcade.draw_texture_rectangle(center_x=SCREEN_WIDTH/2,
                                      center_y=SCREEN_HEIGHT/2,
                                      width=SCREEN_WIDTH,
                                      height=SCREEN_HEIGHT,
                                      texture=self.bg)
        self.hero.draw()
        self.lasers.draw()
        self.enemies.draw()
        self.enemy_lasers.draw()
        arcade.draw_rectangle_filled(center_x=30 +int(ENEMY_COUNT*2.45),
                                      center_y=PROGRESS_HEIGHT/2,
                                      width=ENEMY_COUNT *5.1,
                                      height = PROGRESS_HEIGHT,
                                      color = (78,110,129))
        for i in range(len(self.enemies)):
            arcade.draw_rectangle_filled(center_x=30 + i *5,
                                         center_y=PROGRESS_HEIGHT/2,
                                         width= 5,
                                         height=PROGRESS_HEIGHT,
                                         color =(255,3,3))
            
        arcade.draw_rectangle_outline(center_x=30 +int(ENEMY_COUNT*2.45),
                                      center_y=PROGRESS_HEIGHT/2,
                                      width=ENEMY_COUNT *5.1,
                                      height = PROGRESS_HEIGHT,
                                      color = (249,219,187),
                                      border_width =5 )
        arcade.draw_text(text="Enemis left",
                         start_x= ENEMY_COUNT * 5.2 +30,
                         start_y= PROGRESS_HEIGHT/2-5,
                         color=(249,200,187),
                         font_name = "Kenney Blocks")
            
            
    def on_update(self, delta_time: float): # смена кадров и игровая логика
        if self.lost ==False:
            self.hero.update()
            self.lasers.update()
            self.enemies.update()
            self.enemy_lasers.update()
            for laser in self.lasers:# для уаждого лазера в списке  
                hit_list = arcade.check_for_collision_with_list(laser, self.enemies)
                if len(hit_list) > 0: # когда список пустой
                    laser.kill()  
                    for enemy in hit_list:
                        enemy.kill()
            hit_list = arcade.check_for_collision_with_list(self.hero, self.enemies) + arcade.check_for_collision_with_list(self.hero, self.enemy_lasers)
            if len(hit_list) > 0:
                self.lost = True
                arcade.pause(2)
                self.close()
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol ==arcade.key.ESCAPE:
            self.close()
    def on_key_release(self, symbol: int, modifiers: int):
        pass
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.lost ==False:
            self.hero.center_x = x
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.lost ==False:
            if button == arcade.MOUSE_BUTTON_LEFT:
                laser = Laser() # создаём спрайт
                self.lasers.append(laser) # добавляемспрайт в спрайт лист
                arcade.play_sound(laser.sound, volume = 1)

window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
window.setup() # вызывает метод setup
arcade.run()  # запускает цикл обработки событий