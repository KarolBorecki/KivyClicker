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
        self.info_label.text = self.info_label.set_upgrade_text(self.price) + "\n[size=18]" + str(text) + "[/size]"

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

    def get_text(self):
        return str(self.damage) + " dmg"


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

    def get_text(self):
        return str(self.adds_per_second) + " /sec"


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

    def get_text(self):
        return str(self.adds_per_second) + " /sec " + str(self.damage) + " dmg"
