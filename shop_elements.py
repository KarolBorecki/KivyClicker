from kivy.uix.button import Button


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
        self.info_label.text = self.get_text()

    def get_text(self):
        return ""


class Weapon(Upgrade):
    def __init__(self, number, damage, name, price, use_left, is_bought, **kwargs):
        self.number = number
        self.damage = damage
        self.use_left = use_left
        self.is_bought = is_bought

        self.repair_price = int(price / 4)

        super(Weapon, self).__init__(name, price, **kwargs)

        if is_bought:
            self.set_text()

        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        parent = self.parent.parent.parent.parent.parent
        if not self.is_bought:
            if parent.buy(0, 0, self.price):
                self.on_buy(parent)
        else:
            self.on_set(parent)

    def get_text(self):
        return str(self.damage) + "dmg"

    def on_buy(self, parent):
        self.set_text()
        self.on_set(parent)
        self.is_bought = True

    def on_set(self, parent):
        parent.player.weapon.disabled = False
        self.disabled = True

        parent.player.change_weapon(self)
        if self.is_bought == 1:
            parent.weapon_change_sound.play()

    def set_text(self):
        self.buy_label.text = "SET"

    def repair(self, game):
        if game.buy(0, 0, self.repair_price):
            self.use_left = 800


class Armor(Upgrade):
    def __init__(self, adds_per_second, name, price, is_bought, **kwargs):
        self.adds_per_second = adds_per_second
        self.disabled = is_bought

        super(Armor, self).__init__(name, price, **kwargs)

        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        if self.parent.parent.parent.parent.parent.buy(0, self.adds_per_second, self.price):
            self.disabled = True

    def get_text(self):
        return str(self.adds_per_second) + "/sec"


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
