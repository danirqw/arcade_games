import arcade

SCREEN_WIDTH = 700 #  ШИРИНА ЭКРАНА
SCREEN_HEIGHT = 500 #  ШИРИНА ЭКРАНА
SCREEN_TITLE = "гонки" 

class GameWindow(arcade.Window):
    def __init__(self, width, height, title): # конструктор - вызывается при создании объекта
        super().__init__(width, height, title)    
        
    def setup(self): # начальные кординаты
         pass
    
    def on_draw(self):
        arcade.start_render()  # начало отрисовки
    
    def on_update(self, delta_time: float): # смена кадров и игровая логика
        pass
    
    def on_key_press(self, symbol: int, modifiers: int):
        pass
    def on_key_release(self, symbol: int, modifiers: int):
        pass

window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
window.setup() # вызывает метод setup
arcade.run()  # запускает цикл обработки событий