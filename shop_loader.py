from shop_elements import Weapon, Armor, Potion, Costume

weapon_names = ["Wooden sword", "Iron dagger", "Rusty sword", "Iron sword", "Long iron sword",
                "Golden sword", "Iron hammer", "Heavy iron sword", "Long iron hammer",
                "Iron chopper", "Silver sword", "Long silver sword", "Iron-heart sword", "golden-heart sword",
                "stacked silver sword", "grassy-heart sword", "Ruby sword", "Stacked sword", "Obsidian sword"]
weapon_prices = [0, 200, 500, 800, 1000, 1500, 2000, 4000, 8000, 10000, 20000, 50000, 100000, 150000,
                 300000, 800000, 2000000, 5000000, 10000000, 15000000]
weapon_damage = [1, 3, 5, 7, 10, 13, 10, 13, 15, 20, 24, 30, 40, 51, 63,
                 70, 80, 90, 97, 100]

armor_names = ["Light iron helmet", "Light golden helmet", "Light diamond helmet",
               "Light iron boots", "Light golden boots", "Light diamond boots",
               "Light iron pants", "Light golden pants", "Light diamond pants",
               "Light iron breastplate", "Light golden breastplate", "Light diamond breastplate",
               "Heavy iron helmet", "Heavy golden helmet", "Heavy diamond helmet",
               "Heavy iron boots", "Heavy golden boots", "Heavy diamond boots",
               "Heavy iron pants", "Heavy golden pants", "Heavy diamond pants",
               "Heavy iron breastplate", "Heavy golden breastplate", "Heavy diamond breastplate"]

armor_prices = [100, 500, 1000,
                1600, 2000, 3000,
                4000, 8000, 16000,
                20000, 40000, 100000,
                200000, 300000, 900000,
                2000000, 8000000, 15000000,
                200000000, 50000000, 100000000,
                300000000, 700000000, 1000000000]
armor_per_seconds = [0.3, 1, 1.5,
                     3, 4.7, 7.3,
                     10, 13.1, 15,
                     20.3, 24.1, 30.6,
                     40.6, 51.2, 63.4,
                     70.5, 80.6, 90.1,
                     97.2, 100.2, 109.3,
                     110.2, 112.4, 115.3]

mixture_names = ["Small health mixture", "Small mana mixture", "Small protect mixture", "Small strength mixture",
                 "Big health mixture", "Big mana mixture", "Big protect mixture", "Big strength mixture"]
mixture_prices = [1500, 3000, 5000, 10000,
                  40000, 90000, 100000, 200000]
mixture_damage = [0, 0.5, 0.5, 1,
                  0, 1, 1, 2]
mixture_per_seconds = [0.3, 1, 1.5, 3,
                       4.7, 7.3, 10, 13.1]

costume_names = ["Default", "Yellow"]

costume_prices = [0, 20]


def read_counts_from_file(file_name):
    counts_file = open(file_name, "r")
    counts = []
    for line in counts_file.readlines():
        counts.append(line.strip())
    counts_file.close()

    return counts


def load_weapon():
    names = weapon_names
    prices = weapon_prices
    damage = weapon_damage
    counts = read_counts_from_file("saves/weapon_save.txt")

    weapon = []
    i = 0
    while i < len(names):
        weapon.append(Weapon(i, int(damage[i]), str(names[i]), float(prices[i]), int(counts[i])))
        i += 1

    return weapon


def load_armor():
    names = armor_names
    prices = armor_prices
    per_seconds = armor_per_seconds
    counts = read_counts_from_file("saves/armor_save.txt")

    armor = []
    i = 0
    while i < len(names):
        armor.append(Armor(float(per_seconds[i]), str(names[i]), float(prices[i]), int(counts[i])))
        i += 1

    return armor


def load_potion():
    names = mixture_names
    prices = mixture_prices
    damage = mixture_damage
    per_seconds = mixture_per_seconds
    counts = read_counts_from_file("saves/potion_counts.txt")

    potion = []
    i = 0
    while i < len(names):
        potion.append(Potion(float(per_seconds[i]), int(damage[i]), str(names[i]),
                             float(prices[i]) * (int(counts[i]) + 1), int(counts[i])))
        i += 1
    return potion


def load_costumes():
    names = costume_names
    prices = costume_prices
    counts = read_counts_from_file("saves/costume_saves.txt")

    costumes = []

    i = 0
    while i < len(names):
        costumes.append(Costume(str(names[i]), float(prices[i]), int(counts[i])))
        i += 1

    return costumes
