from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class GameManager(FloatLayout):
    player = ObjectProperty(None)
    menu = ObjectProperty(None)

    money = NumericProperty()
    per_click = NumericProperty()
    per_sec = NumericProperty()

    arena = []
    menu_windows = []

    current_menu_window = None
    current_arena = None
    current_monster = None
    next_monster_index = 0

    is_active = True

    def __init__(self, **kwargs):
        super(GameManager, self).__init__(**kwargs)

    def add_per_second(self, dt):
        self.money += self.per_sec
        if self.per_sec > 0:
            self.game_status()

    def on_touch_down(self, touch):
        if self.is_active:
            self.player.attack(self.current_monster)
            self.money += self.per_click
            self.game_status()
        super(GameManager, self).on_touch_down(touch)

    def spawn_monster(self):
        monster = self.current_arena.monsters[self.next_monster_index]
        self.next_monster_index += 1
        if self.next_monster_index >= len(self.current_arena.monsters):
            self.next_monster_index = 0
        if monster.is_boss:
            print("BOSS FIGHT")

        self.current_monster = monster
        self.add_widget(monster)

    def on_kill(self):
        self.money += self.current_arena.kill_bonus + self.current_monster.kill_bonus

    def open_window(self, menu_option):
        self.is_active = False
        if self.current_menu_window is not None:
            self.remove_widget(self.menu_windows[self.current_menu_window])
        self.add_widget(self.menu_windows[menu_option])
        self.current_menu_window = menu_option

    def close_window(self):
        self.remove_widget(self.menu_windows[self.current_menu_window])
        self.current_menu_window = None
        self.is_active = True

    def buy(self, per_click, per_second, price):
        if self.money >= price:
            self.per_click += per_click
            self.per_sec += per_second
            self.money -= price
            return True
        return False

    def game_status(self):
        print(["Money: " + str(self.money), " Per click: " + str(self.per_click), " Per sec: " + str(self.per_sec),
                "Current Arena: " + str(self.current_arena.name), "Current Monster: " + str(self.current_monster.name)])
