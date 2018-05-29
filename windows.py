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
            self.refresh(self.parent)

    def on_set_click(self):
        if not self.current_arena.is_bought:
            self.buy()
        else:
            self.parent.current_arena = self.current_arena
            self.parent.background.source = self.current_arena.load_background_source()
            self.parent.remove_widget(self.parent.current_monster)
            self.parent.spawn_monster()
            self.parent.arena_change_sound.play()
            self.parent.open_window(4)
            self.refresh(self.parent)

    def refresh(self, parent):
        money_label = MoneyLabel()
        self.current_arena = parent.arena[self.current_arena_number]
        self.header.text = self.current_arena.name

        if self.current_arena.is_bought and self.current_arena.number == parent.current_arena.number:
            self.buy_btn.disabled = True
            self.buy_btn.text = "Set"
        if not self.current_arena.number == parent.current_arena.number and self.current_arena.is_bought:
            self.buy_btn.disabled = False
            self.buy_btn.text = "Set"
        if not self.current_arena.is_bought:
            self.buy_btn.disabled = False
            self.buy_btn.text = money_label.set_upgrade_text(self.current_arena.price)
            self.arena_img.source = "img/arena/icons/na.png"
        else:
            self.arena_img.source = self.current_arena.load_ico_source()

        self.info_label.text = "per click: " + str(self.current_arena.per_click) + "$\n\nKill bonus: " + str(
            self.current_arena.kill_bonus) + "$"

        if self.current_arena_number == 0:
            self.previous_btn.disabled = True
        else:
            self.previous_btn.disabled = False

        if self.current_arena_number == len(parent.arena) - 1:
            self.next_btn.disabled = True
        else:
            self.next_btn.disabled = False
