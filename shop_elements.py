from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color


class Upgrade(Button):
    def __init__(self, name, price, **kwargs):
        super(Upgrade, self).__init__(**kwargs)
        self.name = name
        self.primary_price = price
        self.price = price
        self.img.source = self.load_img_src()
        self.info_label.markup = True
        self.name_label.text = name
        self.load_label_text()

    def reset(self):
        self.price = self.primary_price
        self.load_text(self.get_text())

    def load_img_src(self):
        return "img/upgrades/" + self.name + ".png"

    def load_label_text(self):
        self.buy_label.text = self.buy_label.set_text(self.price)
        self.load_info_label_text()

    def load_info_label_text(self):
        self.info_label.text = self.get_text()

    def get_text(self):
        return ""

    def on_add(self, caller=None):
        pass


class Weapon(Upgrade):
    def __init__(self, number, damage, name, price, use_left, level, **kwargs):
        self.number = number
        self.damage = damage
        self.use_left = use_left
        self.level = level

        super(Weapon, self).__init__(name, price, **kwargs)

        self.repair_price = self.calculate_repair_price()
        self.upgrade_price = self.calculate_upgrade_price()

        self.check_level(level)
        self.bind(on_press=self.on_click)

    def repair(self, game):
        if game.buy(0, 0, self.repair_price):
            self.use_left = 800

    def upgrade(self, game):
        if game.buy(0, 0, self.upgrade_price):
            self.level += 1
            self.repair_price = self.calculate_repair_price()
            self.upgrade_price = self.calculate_upgrade_price()
            self.check_level(self.level)

    def check_level(self, level):
        if level > 0:
            self.set_text()
            i = level
            while i > 1:
                self.damage = round(self.damage * 1.2, 1)
                i -= 1
            self.load_info_label_text()

    def on_click(self, instance):
        parent = self.parent.parent.parent.parent.parent
        if not self.level > 0:
            if parent.buy(0, 0, self.price):
                self.on_buy(parent)
        else:
            self.on_set(parent)

    def on_buy(self, parent):
        self.level += 1
        self.set_text()
        self.on_set(parent)

    def on_set(self, parent):
        parent.player.weapon.disabled = False
        self.disabled = True

        parent.player.change_weapon(self)
        if self.level > 0:
            parent.weapon_change_sound.play()

    def calculate_repair_price(self):
        return int(self.price * (self.level + 1) / 2)

    def calculate_upgrade_price(self):
        return int(self.price * self.level * (self.level + 1))

    def set_text(self):
        self.buy_label.text = "SET"

    def get_text(self):
        return str(self.damage) + "dmg"


class Armor(Upgrade):
    def __init__(self, adds_per_second, name, price, is_bought, **kwargs):
        self.adds_per_second = adds_per_second
        self.is_bought = is_bought

        super(Armor, self).__init__(name, price, **kwargs)

        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        parent = self.parent.parent.parent.parent.parent
        if not self.is_bought and parent.buy(0, self.adds_per_second, self.price):
            self.is_bought = 1
            self.on_add(self.parent.parent.parent.parent.shop_content)

    def get_text(self):
        return str(self.adds_per_second) + "/sec"

    def on_add(self, caller=None):
        if self.is_bought > 0:
            print("DELETING" + str(caller))
            caller.scrolling_area.remove_widget(self)


class Mixture(Upgrade):
    def __init__(self, adds_per_second, damage, name, price, count, **kwargs):
        self.adds_per_second = adds_per_second
        self.damage = damage
        self.count = count

        super(Mixture, self).__init__(name, price, **kwargs)

        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        if self.parent.parent.parent.parent.parent.buy(self.damage, self.adds_per_second, self.price):
            self.count += 1
            self.price *= self.count
            self.load_label_text()

    def get_text(self):
        return str(self.adds_per_second) + "/sec\n" + str(self.damage) + " dmg"


class Costume(Upgrade):
    def __init__(self, number, name, price, is_bought, **kwargs):
        super(Costume, self).__init__(name, price, **kwargs)
        self.number = number
        self.is_bought = is_bought
        self.bind(on_press=self.on_click)

        if is_bought:
            self.set_text()

    def on_click(self, instance):
        parent = self.parent.parent.parent.parent.parent
        if not self.is_bought:
            if parent.buy(0, 0, self.price):
                self.on_buy(parent)
        else:
            self.on_set(parent)

    def on_buy(self, parent):
        self.set_text()
        self.on_set(parent)
        self.is_bought = 1

    def on_set(self, parent):
        parent.player.costume.disabled = False
        self.disabled = True

        parent.player.costume = self
        parent.player.load_img()
        if self.is_bought == 1:
            parent.costume_change_sound.play()

    def set_text(self):
        self.info_label.text = "SET"
