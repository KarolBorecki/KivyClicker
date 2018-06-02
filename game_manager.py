from random import randint

from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, ObjectProperty, Clock
from kivy.uix.floatlayout import FloatLayout

from gui_elements import DisappearingLabel


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

    attack_sound = SoundLoader.load('sounds/player_attack.wav')
    buy_sound = SoundLoader.load('sounds/buy.wav')
    window_open_sound = SoundLoader.load('sounds/window_open.wav')
    switch_sound = SoundLoader.load('sounds/switch.wav')
    failed_buy_sound = SoundLoader.load('sounds/failed_buy.wav')
    arena_change_sound = SoundLoader.load('sounds/arena_change.wav')
    costume_change_sound = SoundLoader.load('sounds/costume_change.wav')
    weapon_change_sound = SoundLoader.load('sounds/weapon_change.wav')

    def __init__(self, **kwargs):
        super(GameManager, self).__init__(**kwargs)
        Clock.schedule_interval(self.add_per_second, 1.0)

    def add_money(self, amount):
        if self.is_active:
            label_pos = {"center_x": randint(20, 80) / 100, "center_y": randint(20, 80) / 100}
            self.add_widget(DisappearingLabel("+" + str(amount) + "$", pos_hint=label_pos, font_size=30, duration=0.5))
        self.money += amount

    def add_per_second(self, dt):
        self.add_money(self.per_sec)

    def on_touch_down(self, touch):
        if self.is_active:
            if self.player.weapon.use_left > 0:
                self.player.attack(self.current_monster)
            else:
                self.add_widget(DisappearingLabel("Your broke a weapon!", duration=1))
            self.attack_sound.play()
            self.add_money(self.per_click)
        super(GameManager, self).on_touch_down(touch)

    def spawn_monster(self):
        monster = self.current_arena.monsters[self.next_monster_index]
        self.next_monster_index += 1

        if self.next_monster_index >= len(self.current_arena.monsters):
            self.next_monster_index = 0

        if monster.is_boss:
            self.add_widget(DisappearingLabel("BOSS FIGHT", font_size=50, duration=2))

        self.current_monster = monster

        self.remove_widget(self.player)
        self.add_widget(monster)
        self.add_widget(self.player)

    def on_kill(self):
        self.money += self.current_arena.kill_bonus + self.current_monster.kill_bonus

    def open_window(self, menu_option):
        self.attack_sound.stop()
        self.window_open_sound.play()

        if self.current_menu_window is not None:
            self.remove_widget(self.menu_windows[self.current_menu_window])
        window = self.menu_windows[menu_option]
        self.add_widget(window)
        window.on_open()
        self.current_menu_window = menu_option
        self.is_active = False

    def close_window(self):
        self.remove_widget(self.menu_windows[self.current_menu_window])
        self.current_menu_window = None
        self.is_active = True

    def buy(self, per_click, per_second, price):
        if self.money >= price:
            self.buy_sound.play()
            self.per_click += per_click
            self.per_sec += per_second
            self.money -= price
            return True
        self.add_widget(DisappearingLabel(text="You don't have enough money!", duration=1))
        self.failed_buy_sound.play()
        return False

    def game_status(self):
        print(["Money: " + str(self.money), " Per click: " + str(self.per_click), " Per sec: " + str(self.per_sec),
               "Current Arena: " + str(self.current_arena.name), "Current Monster: " + str(self.current_monster.name)])
