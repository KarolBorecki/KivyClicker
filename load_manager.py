import os

from kivy.app import App

from arena import Arena
from gui_elements import Monster, Player
from shop_loader import load_weapon, load_mixture, load_armor, load_costumes, weapon_names, armor_names, mixture_names, \
    costume_names
from windows import ShopWindow, ArenaWindow, WorkshopWindow


def load_arena():
    user_data_dir = App.get_running_app().user_data_dir + "/"
    arena_1_monsters = [Monster("enemy_1", 150, 1), Monster("enemy_4", 150, 1), Monster("enemy_2", 150, 1),
                        Monster("enemy_6", 150, 1), Monster("enemy_30", 150, 1), Monster("enemy_32", 150, 1)]

    arena_2_monsters = [Monster("enemy_10", 700, 2), Monster("enemy_11", 700, 2), Monster("enemy_12", 700, 2),
                        Monster("enemy_14", 700, 2), Monster("enemy_15", 700, 2), Monster("enemy_5", 700, 2),
                        Monster("enemy_28", 1000, 5, True)]

    arena_3_monsters = [Monster("enemy_7", 1300, 3), Monster("enemy_26", 1300, 3), Monster("enemy_8", 1300, 3),
                        Monster("enemy_22", 1300, 3), Monster("enemy_35", 1300, 3), Monster("enemy_9", 1350, 3)]

    arena_4_monsters = [Monster("enemy_24", 2000, 5), Monster("enemy_33", 2000, 5), Monster("enemy_13", 2000, 5),
                        Monster("enemy_33", 2000, 5), Monster("enemy_37", 2000, 5), Monster("enemy_39", 2500, 5),
                        Monster("enemy_3", 5000, 10, True)]

    arena_5_monsters = [Monster("enemy_25", 3700, 10), Monster("enemy_23", 3700, 10), Monster("enemy_27", 3700, 10),
                        Monster("enemy_36", 3700, 10), Monster("enemy_38", 3700, 10), Monster("enemy_34", 3700, 10)]

    arena_6_monsters = [Monster("enemy_16", 8000, 20), Monster("enemy_17", 8000, 20), Monster("enemy_18", 8000, 20),
                        Monster("enemy_19", 8000, 20), Monster("enemy_20", 8000, 20), Monster("enemy_21", 8000, 20),
                        Monster("enemy_29", 10000, 40, True)]

    arena_save_file = open(user_data_dir + "arena_save.txt", "r")
    arena_data = arena_save_file.readlines()
    arena_save_file.close()

    return [Arena(0, "Arena 1", 0, 5, 60, arena_1_monsters, True),
            Arena(1, "Arena 2", 10000, 20, 140, arena_2_monsters, bool(int(arena_data[1]))),
            Arena(2, "Arena 3", 50000, 90, 320, arena_3_monsters, bool(int(arena_data[2]))),
            Arena(3, "Arena 4", 100000, 170, 560, arena_4_monsters, bool(int(arena_data[3]))),
            Arena(4, "Arena 5", 500000, 300, 1000, arena_5_monsters, bool(int(arena_data[4]))),
            Arena(5, "Arena 6", 1000000, 560, 2000, arena_6_monsters, bool(int(arena_data[5])))]


def save_game(game):
    user_data_dir = App.get_running_app().user_data_dir + "/"

    save_file = open(user_data_dir + "game_info_save.txt", "w")

    save_file.write(str(game.money) + "\n")
    save_file.write(str(game.per_sec) + "\n")
    save_file.write(str(game.current_arena.number) + "\n")
    save_file.write(str(game.player.costume.number) + "\n")
    save_file.write(str(game.player.weapon.number) + "\n")

    save_file.close()

    weapon_save_file = open(user_data_dir + "weapon_save.txt", "w")
    for weapon in game.menu_windows[0].content:
        weapon_save_file.write(str(int(weapon.level)) + "\n")
    weapon_save_file.close()

    weapon_use_left_file = open(user_data_dir + "weapon_use_left.txt", "w")
    for weapon in game.menu_windows[0].content:
        weapon_use_left_file.write(str(int(weapon.use_left)) + "\n")
    weapon_use_left_file.close()

    armor_save_file = open(user_data_dir + "armor_save.txt", "w")
    for armor in game.menu_windows[1].content:
        armor_save_file.write(str(int(armor.is_bought)) + "\n")
    armor_save_file.close()

    potion_counts_file = open(user_data_dir + "potion_counts.txt", "w")
    for potion in game.menu_windows[2].content:
        potion_counts_file.write(str(potion.count) + "\n")
    potion_counts_file.close()

    arena_save_file = open(user_data_dir + "arena_save.txt", "w")
    for a in game.arena:
        arena_save_file.write(str(int(a.is_bought)) + "\n")
    arena_save_file.close()

    costume_save_file = open(user_data_dir + "costume_saves.txt", "w")
    for a in game.menu_windows[3].content:
        costume_save_file.write(str(int(a.is_bought)) + "\n")
    costume_save_file.close()


def load_game(game):
    user_data_dir = App.get_running_app().user_data_dir + "/"
    if not os.path.isfile(user_data_dir + "game_info_save.txt"):
        reset()

    save_file = open(user_data_dir + "game_info_save.txt", "r")
    data = save_file.readlines()
    print data
    print user_data_dir
    save_file.close()

    game.arena = load_arena()
    game.money = float(data[0])
    game.per_sec = float(data[1])
    game.current_arena = game.arena[int(data[2])]
    game.per_click = game.current_arena.per_click
    game.menu_windows = [ShopWindow("Weapon", load_weapon()), ShopWindow("Armor", load_armor()),
                         ShopWindow("Alchemy", load_mixture()), ShopWindow("Costumes", load_costumes()),
                         ArenaWindow(game)]
    costume = game.menu_windows[3].content[int(data[3])]
    weapon = game.menu_windows[0].content[int(data[4])]
    game.player = Player(costume, weapon)
    costume.on_set(game)
    weapon.on_set(game)
    game.menu_windows.append(WorkshopWindow(game))
    game.add_widget(game.player)
    game.background.source = game.current_arena.load_background_source()
    game.spawn_monster()


def reset():
    user_data_dir = App.get_running_app().user_data_dir + "/"
    save_file = open(user_data_dir + "game_info_save.txt", "a+")

    save_file.write(str(0) + "\n")
    save_file.write(str(0) + "\n")
    save_file.write(str(0) + "\n")
    save_file.write(str(0) + "\n")
    save_file.write(str(0) + "\n")

    save_file.close()

    i = 1
    weapon_save_file = open(user_data_dir + "weapon_save.txt", "a+")
    for weapon in weapon_names:
        weapon_save_file.write(str(int(i)) + "\n")
        i = 0
    weapon_save_file.close()

    weapon_save_file = open(user_data_dir + "weapon_use_left.txt", "a+")
    for weapon in weapon_names:
        weapon_save_file.write("800" + "\n")
    weapon_save_file.close()

    i = 0
    armor_save_file = open(user_data_dir + "armor_save.txt", "a+")
    for armor in armor_names:
        armor_save_file.write(str(int(i)) + "\n")
    armor_save_file.close()

    i = 0
    potion_counts_file = open(user_data_dir + "potion_counts.txt", "a+")
    for potion in mixture_names:
        potion_counts_file.write(str(i) + "\n")
    potion_counts_file.close()

    i = 1
    arena_save_file = open(user_data_dir + "arena_save.txt", "a+")
    for a in range(6):
        arena_save_file.write(str(int(i)) + "\n")
        i = 0
    arena_save_file.close()

    i = 1
    costume_save_file = open(user_data_dir + "costume_saves.txt", "a+")
    for a in costume_names:
        costume_save_file.write(str(int(i)) + "\n")
        i = 0
    costume_save_file.close()
