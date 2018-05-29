from kivy.uix.button import Button


class Upgrade(Button):
    def __init__(self, name, price, text, **kwargs):
        super(Upgrade, self).__init__(**kwargs)
        self.name = name
        self.primary_price = price
        self.price = price
        self.img.source = self.load_img_src()
        self.info_label.markup = True
        self.name_label.text = name
        self.info_label.text = self.info_label.set_upgrade_text(self.price) + "\n" + str(text)

    def reset(self):
        self.price = self.primary_price
        self.load_text(self.get_text())

    def load_img_src(self):
        return "img/upgrades/" + self.name + ".png"


class Weapon(Upgrade):
    def __init__(self, number, damage, name, price, is_bought, **kwargs):
        super(Weapon, self).__init__(name, price, str(damage) + " dmg", **kwargs)
        self.number = number
        self.damage = damage
        self.disabled = is_bought
        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        game = self.parent.parent.parent.parent.parent
        if game.buy(self.damage, 0, self.price):
            self.disabled = True
            if game.player.weapon.damage < self.damage:
                game.player.change_weapon(self)


class Armor(Upgrade):
    def __init__(self, adds_per_second, name, price, is_bought, **kwargs):
        super(Armor, self).__init__(name, price, str(adds_per_second) + " /sec", **kwargs)
        self.adds_per_second = adds_per_second
        self.disabled = is_bought
        self.bind(on_press=self.on_click)

        self.font_size = 20

    def on_click(self, instance):
        if self.parent.parent.parent.parent.parent.buy(0, self.adds_per_second, self.price):
            self.disabled = True


class Potion(Upgrade):
    def __init__(self, adds_per_second, damage, name, price, count, **kwargs):
        super(Potion, self).__init__(name, price, str(adds_per_second) + "/sec " + str(damage) + " dmg", **kwargs)
        self.adds_per_second = adds_per_second
        self.damage = damage
        self.count = count
        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        if self.parent.parent.parent.parent.parent.buy(self.damage, self.adds_per_second, self.price):
            self.count += 1
            self.price *= self.count + 1
            self.load_text(self.get_text())


class Costume(Upgrade):
    def __init__(self, number, name, price, is_bought, **kwargs):
        super(Costume, self).__init__(name, price, "", **kwargs)
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
        self.is_bought = 1
        self.on_set(parent)

    def on_set(self, parent):
        parent.player.costume.disabled = False
        self.disabled = True

        parent.player.costume = self
        parent.player.load_img()

    def set_text(self):
        self.info_label.text = "SET"
