from kivy.uix.label import Label

from arena import Arena
from gui_elements import Monster, Player
from shop_loader import load_weapon, load_potion, load_armor
from windows import ShopWindow, ArenaWindow


def load_arena():
    arena_1_monsters = [Monster("enemy_1", 500, 10), Monster("enemy_4", 500, 10), Monster("enemy_2", 1000, 20),
                        Monster("enemy_6", 1000, 20), Monster("enemy_30", 1000, 20), Monster("enemy_32", 1000, 20)]

    arena_2_monsters = [Monster("enemy_10", 500, 10), Monster("enemy_11", 500, 10), Monster("enemy_12", 1000, 20),
                        Monster("enemy_14", 1000, 20), Monster("enemy_15", 1000, 20), Monster("enemy_5", 1000, 20),
                        Monster("enemy_28", 1000, 20, True)]

    arena_3_monsters = [Monster("enemy_7", 500, 10), Monster("enemy_26", 500, 10), Monster("enemy_8", 1000, 20),
                        Monster("enemy_22", 1000, 20), Monster("enemy_35", 1000, 20), Monster("enemy_9", 1000, 20)]

    arena_4_monsters = [Monster("enemy_24", 500, 10), Monster("enemy_33", 500, 10), Monster("enemy_13", 1000, 20),
                        Monster("enemy_33", 1000, 20), Monster("enemy_37", 1000, 20), Monster("enemy_39", 1000, 20),
                        Monster("enemy_3", 1000, 20, True)]

    arena_5_monsters = [Monster("enemy_25", 500, 10), Monster("enemy_23", 500, 10), Monster("enemy_27", 1000, 20),
                        Monster("enemy_36", 1000, 20), Monster("enemy_38", 1000, 20), Monster("enemy_34", 1000, 20)]

    arena_6_monsters = [Monster("enemy_16", 500, 10), Monster("enemy_17", 500, 10), Monster("enemy_18", 1000, 20),
                        Monster("enemy_19", 1000, 20), Monster("enemy_20", 1000, 20), Monster("enemy_21", 1000, 20),
                        Monster("enemy_29", 1000, 20, True)]

    arena_save_file = open("saves/arena_save.txt", "r")
    arena_data = arena_save_file.readlines()
    arena_save_file.close()

    return [Arena(0, "Arena 1", 0, 1, 5, arena_1_monsters, True),
            Arena(1, "Arena 2", 100000, 3, 8, arena_2_monsters, bool(int(arena_data[1]))),
            Arena(2, "Arena 3", 500000, 7, 12, arena_3_monsters, bool(int(arena_data[2]))),
            Arena(3, "Arena 4", 1000000, 8, 15, arena_4_monsters, bool(int(arena_data[3]))),
            Arena(4, "Arena 5", 1000000, 8, 15, arena_5_monsters, bool(int(arena_data[4]))),
            Arena(5, "Arena 6", 1000000, 8, 15, arena_6_monsters, bool(int(arena_data[5])))]


def save_game(game):
    save_file = open("saves/game_info_save.txt", "w")

    save_file.write(str(game.money) + "\n")
    save_file.write(str(game.per_sec) + "\n")
    save_file.write(str(game.current_arena.number) + "\n")
    save_file.write(str(game.player.source) + "\n")
    save_file.write(str(game.player.weapon.number) + "\n")

    save_file.close()

    weapon_save_file = open("saves/weapon_save.txt", "w")
    for weapon in game.menu_windows[0].content:
        weapon_save_file.write(str(int(weapon.disabled)) + "\n")
    weapon_save_file.close()

    armor_save_file = open("saves/armor_save.txt", "w")
    for armor in game.menu_windows[1].content:
        armor_save_file.write(str(int(armor.disabled)) + "\n")
    armor_save_file.close()

    potion_counts_file = open("saves/potion_counts.txt", "w")
    for potion in game.menu_windows[2].content:
        potion_counts_file.write(str(potion.count) + "\n")
    potion_counts_file.close()

    arena_save_file = open("saves/arena_save.txt", "w")
    for a in game.arena:
        arena_save_file.write(str(int(a.is_bought)) + "\n")
    arena_save_file.close()


def load_game(game):
    save_file = open("saves/game_info_save.txt", "r")
    data = save_file.readlines()
    save_file.close()
    game.arena = load_arena()
    game.money = float(data[0])
    game.per_sec = float(data[1])
    game.current_arena = game.arena[int(data[2])]
    game.per_click = game.current_arena.per_click
    game.menu_windows = [ShopWindow("Weapon", load_weapon()), ShopWindow("Armor", load_armor()),
                         ShopWindow("Alchemy", load_potion()), ShopWindow("Costumes", []),
                         ArenaWindow(game)]
    game.menu_windows[3].add_widget(Label(text="Coming soon", font_size=40, pos_hint={'center_x': .5, 'center_y': .5}))
    game.player = Player(data[3].split()[0], game.menu_windows[0].content[int(data[4])])
    game.add_widget(game.player)
    game.background.source = game.current_arena.load_background_source()
    game.spawn_monster()
