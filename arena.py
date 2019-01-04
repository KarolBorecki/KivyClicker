class Arena:
    def __init__(self, number, name, price, per_click, kill_bonus, opponents, is_bought=False):
        self.number = number
        self.name = name
        self.price = price
        self.per_click = per_click
        self.kill_bonus = kill_bonus
        self.monsters = opponents
        self.is_bought = is_bought

    def load_ico_source(self):
        return "img/arena/icons/" + str(self.name) + ".png"

    def load_background_source(self):
        return "img/arena/" + str(self.name) + ".png"
