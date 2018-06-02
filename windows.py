from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

from arena import Arena
from gui_elements import MoneyLabel


class ShopContent(ScrollView):
    def __init__(self, elements, **kwargs):
        ScrollView.__init__(self, **kwargs)

        for element in elements:
            self.scrolling_area.add_widget(element)


class PopupWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

    def on_open(self):
        pass


class ShopWindow(PopupWindow):
    def __init__(self, header, content, **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.content = content
        self.header.text = header

        self.window_scheme.add_widget(ShopContent(self.content))

    def reset(self):
        for upgrade in self.content:
            upgrade.reset()


class ArenaWindow(PopupWindow):
    current_arena = Arena

    def __init__(self, parent, **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.current_arena_number = parent.current_arena.number
        self.refresh(parent)

    def change_arena(self, direction):
        self.parent.switch_sound.play()
        self.current_arena_number += direction
        self.refresh(self.parent)

    def buy(self):
        if self.parent.buy(self.current_arena.per_click, 0, self.current_arena.price):
            self.current_arena.is_bought = True
            self.set_area()

    def set_area(self):
        self.parent.current_arena = self.current_arena
        self.parent.background.source = self.current_arena.load_background_source()
        self.parent.remove_widget(self.parent.current_monster)
        self.parent.spawn_monster()
        self.parent.arena_change_sound.play()
        self.parent.open_window(4)
        self.refresh(self.parent)

    def on_set_click(self):
        if not self.current_arena.is_bought:
            self.buy()
        else:
            self.set_area()

    def refresh(self, parent):
        self.current_arena = parent.arena[self.current_arena_number]
        self.header.text = self.current_arena.name

        self.set_buy_button(parent)
        self.load_info_label_text()
        self.set_switch_buttons(parent)

    def set_buy_button(self, parent):
        money_label = MoneyLabel()
        if self.current_arena.is_bought and self.current_arena.number == parent.current_arena.number:
            self.buy_btn.disabled = True
            self.buy_btn.text = "Set"
        if not self.current_arena.number == parent.current_arena.number and self.current_arena.is_bought:
            self.buy_btn.disabled = False
            self.buy_btn.text = "Set"
        if not self.current_arena.is_bought:
            self.buy_btn.disabled = False
            self.buy_btn.text = money_label.set_text(self.current_arena.price)
            self.arena_img.source = "img/arena/icons/na.png"
        else:
            self.arena_img.source = self.current_arena.load_ico_source()

    def set_switch_buttons(self, parent):
        if self.current_arena_number == 0:
            self.previous_btn.disabled = True
        else:
            self.previous_btn.disabled = False

        if self.current_arena_number == len(parent.arena) - 1:
            self.next_btn.disabled = True
        else:
            self.next_btn.disabled = False

    def load_info_label_text(self):
        self.info_label.text = "per click: " + str(self.current_arena.per_click) + "$\n\nKill bonus: " + str(
            self.current_arena.kill_bonus) + "$"


class WorkshopWindow(PopupWindow):
    def __init__(self, game, **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.game = game
        self.load_info_labels_text()

        self.costume_card.btn1.text = "?"
        self.costume_card.btn2.text = "?"

        self.weapon_card.btn1.text = "?"
        self.weapon_card.btn2.text = "Repair"
        self.weapon_card.btn2.bind(on_press=self.repair)

    def repair(self, instance):
        self.game.player.weapon.repair(self.game)
        self.load_info_labels_text()

    def on_open(self):
        self.load_info_labels_text()

    def load_info_labels_text(self):
        self.costume_card.card_header.text = "Costume"
        self.costume_card.info_label.text = "Health: ?\nStrength: ?\nLevel: ?"
        self.costume_card.img.source = self.game.player.player_img.source

        self.weapon_card.card_header.text = "Sword"
        self.weapon_card.info_label.text = "Damage: " + str(self.game.player.weapon.damage) + "\nUse left: " + str(
            self.game.player.weapon.use_left) + "\nLevel: ?"
        self.weapon_card.img.source = self.game.player.weapon_img.source
