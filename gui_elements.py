from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Player(FloatLayout):
    angle = NumericProperty(90)

    attack_sound = SoundLoader.load('sounds/player_attack.wav')

    def __init__(self, costume, weapon, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.costume = costume
        self.weapon = weapon
        self.weapon_img.source = self.weapon.load_img_src()
        self.load_img()

    def attack(self, monster):
        self.attack_sound.play()
        self.parent.add_widget(DisappearingImage("img/effects/dust.gif", {'center_x': .5, 'center_y': .5}, (.6, .6)))
        anim = Animation(angle=0, duration=0.05) + Animation(angle=90, duration=0.1)
        anim.start(self)
        monster.get_dmg(self.weapon.damage)

    def change_weapon(self, weapon):
        self.weapon = weapon
        self.weapon_img.source = weapon.load_img_src()

    @staticmethod
    def on_angle(item, angle):
        if angle == 360:
            item.angle = 0

    def load_img(self):
        self.player_img.source = self.costume.load_img_src()


class Monster(Image):
    death_sound = SoundLoader.load('sounds/monster_death.wav')

    def __init__(self, name, health, kill_bonus, is_boss=False, **kwargs):
        super(Monster, self).__init__(**kwargs)
        self.name = name
        self.primary_health = health
        self.health = health
        self.kill_bonus = kill_bonus
        self.is_boss = is_boss
        self.source = self.load_src()

        if is_boss:
            self.size_hint_y = .3

    def get_dmg(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = self.primary_health
            self.dead()

    def dead(self):
        self.death_sound.play()
        self.parent.spawn_monster()
        self.parent.on_kill()
        self.parent.remove_widget(self)

    def load_src(self):
        return "img/enemies/" + str(self.name) + ".png"


class MenuButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)


class DisappearingImage(Image):
    def __init__(self, src, pos=None, size=None, duration=0.4, **kwargs):
        super(DisappearingImage, self).__init__(**kwargs)
        self.source = src
        self.pos_hint = pos
        self.size_hint = size
        Clock.schedule_once(self.destroy, duration)

    def destroy(self, dt):
        self.parent.remove_widget(self)


class DisappearingLabel(Label):
    def __init__(self, text, pos=None, duration=0.4, **kwargs):
        super(DisappearingLabel, self).__init__(**kwargs)

        if pos is None:
            pos = {'center_x': .5}

        self.text = text
        self.font_size = font_size
        self.pos_hint = pos
        self.center_y = Window.height / 2 * -1 + 100
        anim = Animation(y=Window.height / 2 * -1 + 200, duration=duration)
        anim.start(self)
        Clock.schedule_once(self.destroy, duration)

    def destroy(self, dt):
        self.parent.remove_widget(self)


class MoneyLabel(Label):
    def __init__(self, **kwargs):
        super(MoneyLabel, self).__init__(**kwargs)

    @staticmethod
    def set_text(price, round_places=1):
        round_places = round_places
        if price >= 1000000000:
            return str(round(price / 1000000000, round_places)) + "mld$"

        elif price >= 1000000:
            return str(round(price/1000000, round_places)) + "mln$"

        elif price >= 1000:
            return str(round(price/1000, round_places)) + "tys$"

        else:
            return str(round(price, round_places)) + "$"

    @staticmethod
    def set_upgrade_text(price):
        if price >= 1000000000:
            return str(int(price / 1000000000)) + "mld"

        elif price >= 1000000:
            return str(int(price / 1000000)) + "mln"

        elif price >= 1000:
            return str(int(price / 1000)) + "tys"

        else:
            return str(int(price))
