from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from game_manager import GameManager
from load_manager import save_game, load_game

Window.size = (540, 960)
Builder.load_file('graphic.kv')


class ClickerApp(App):
    game = GameManager()

    def build(self):
        load_game(self.game)
        return self.game

    def on_stop(self):
        save_game(self.game)


app = ClickerApp()

if __name__ == '__main__':
    app.run()
