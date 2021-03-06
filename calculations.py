from move import get_move
from pokemon import get_pokemon
import random


def calc_type_matchup(move_type, pokemon_types):
    chart = dict()

    normal_chart = dict()
    normal_chart["strength"] = list()
    normal_chart["weakness"] = ["rock", "steel"]
    normal_chart["immunity"] = ["ghost"]
    chart["normal"] = normal_chart

    fire_chart = dict()
    fire_chart["strength"] = ["grass", "ice", "bug", "steel"]
    fire_chart["weakness"] = ["fire", "water", "rock", "dragon"]
    fire_chart["immunity"] = list()
    chart["fire"] = fire_chart

    water_chart = dict()
    water_chart["strength"] = ["fire", "ground", "rock"]
    water_chart["weakness"] = ["water", "grass", "dragon"]
    water_chart["immunity"] = list()
    chart["water"] = water_chart

    electric_chart = dict()
    electric_chart["strength"] = ["water", "flying"]
    electric_chart["weakness"] = ["electric", "grass", "dragon"]
    electric_chart["immunity"] = ["ground"]
    chart["electric"] = electric_chart

    grass_chart = dict()
    grass_chart["strength"] = ["water", "ground", "rock"]
    grass_chart["weakness"] = ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"]
    grass_chart["immunity"] = list()
    chart["grass"] = grass_chart

    ice_chart = dict()
    ice_chart["strength"] = ["grass", "ground", "flying", "dragon"]
    ice_chart["weakness"] = ["fire", "water", "ice", "steel"]
    ice_chart["immunity"] = list()
    chart["ice"] = ice_chart

    fighting_chart = dict()
    fighting_chart["strength"] = ["normal", "ice", "rock", "dark", "steel"]
    fighting_chart["weakness"] = ["poison", "flying", "psychic", "bug", "fairy"]
    fighting_chart["immunity"] = ["ghost"]
    chart["fighting"] = fighting_chart

    poison_chart = dict()
    poison_chart["strength"] = ["grass", "fairy"]
    poison_chart["weakness"] = ["poison", "ground", "rock", "ghost"]
    poison_chart["immunity"] = ["steel"]
    chart["poison"] = poison_chart

    ground_chart = dict()
    ground_chart["strength"] = ["fire", "electric", "poison", "rock", "steel"]
    ground_chart["weakness"] = ["grass", "bug"]
    ground_chart["immunity"] = ["flying"]
    chart["ground"] = ground_chart

    flying_chart = dict()
    flying_chart["strength"] = ["grass", "fighting", "bug"]
    flying_chart["weakness"] = ["electric", "rock", "steel"]
    flying_chart["immunity"] = list()
    chart["flying"] = flying_chart

    psychic_chart = dict()
    psychic_chart["strength"] = ["fighting", "poison"]
    psychic_chart["weakness"] = ["psychic", "steel"]
    psychic_chart["immunity"] = ["dark"]
    chart["psychic"] = psychic_chart

    bug_chart = dict()
    bug_chart["strength"] = ["grass", "psychic", "dark"]
    bug_chart["weakness"] = ["fire", "fighting", "poison", "flying", "rock", "steel", "fairy"]
    bug_chart["immunity"] = []
    chart["bug"] = bug_chart

    rock_chart = dict()
    rock_chart["strength"] = ["fire", "ice", "flying", "bug"]
    rock_chart["weakness"] = ["ground", "fighting", "steel"]
    rock_chart["immunity"] = []
    chart["rock"] = rock_chart

    ghost_chart = dict()
    ghost_chart["strength"] = ["psychic", "ghost"]
    ghost_chart["weakness"] = ["dark"]
    ghost_chart["immunity"] = ["normal"]
    chart["ghost"] = ghost_chart

    dragon_chart = dict()
    dragon_chart["strength"] = ["dragon"]
    dragon_chart["weakness"] = ["steel"]
    dragon_chart["immunity"] = ["fairy"]
    chart["dragon"] = dragon_chart

    dark_chart = dict()
    dark_chart["strength"] = ["psychic", "ghost"]
    dark_chart["weakness"] = ["fighting", "dark", "fairy"]
    dark_chart["immunity"] = []
    chart["dark"] = dark_chart

    steel_chart = dict()
    steel_chart["strength"] = ["steel", "rock", "fairy"]
    steel_chart["weakness"] = ["fire", "water", "electric", "steel"]
    steel_chart["immunity"] = []
    chart["steel"] = steel_chart

    fairy_chart = dict()
    fairy_chart["strength"] = ["fighting", "dragon", "dark"]
    fairy_chart["weakness"] = ["fire", "poison", "steel"]
    fairy_chart["immunity"] = []
    chart["fairy"] = fairy_chart

    mult = 1.0
    the_chart = chart[move_type]
    for pkmn_type in pokemon_types:
        if (pkmn_type in the_chart["strength"]):
            mult *= 2.0
        elif (pkmn_type in the_chart["weakness"]):
            mult *= 0.5
        elif (pkmn_type in the_chart["immunity"]):
            return 0
    return mult


def basic_calculate(my_pokemon, enemy_pokemon, enemy_level):
    best = 0
    the_damage = list()
    index = 0
    top_damage = 0
    for the_move in my_pokemon.moves:
        temp_move = get_move(the_move)
        atk = 0.0
        def_min = 0.0
        def_max = 0.0
        min_damage = 0.0
        max_damage = 0.0
        if (temp_move.category == "Physical"):
            atk = my_pokemon.attack
            def_min = int((2 * enemy_pokemon.stats[2] + 31 + 85 / 4.0) * enemy_level)
            def_min /= 100.0
            def_min += 5
            def_max = int((2 * enemy_pokemon.stats[2] + 31 + 85 / 4.0) * enemy_level)
            def_max /= 100.0
            def_max += 5
        elif (temp_move.category == "Special"):
            atk = my_pokemon.special_attack
            def_min = int((2 * enemy_pokemon.stats[4] + 31 + 85 / 4.0) * enemy_level)
            def_min /= 100.0
            def_min += 5
            def_max = int((2 * enemy_pokemon.stats[4] + 31 + 85 / 4.0) * enemy_level)
            def_max /= 100.0
            def_max += 5
        if (temp_move.category != "Status"):
            used_level = 0
            try:
                used_level = int(my_pokemon.level)
            except:
                used_level = 100
            min_damage = 2 + ((temp_move.power * atk / def_max * (2 + (2 * used_level / 5.0))) / 50.0)
            max_damage = 2 + ((temp_move.power * atk / def_min * (2 + (2 * used_level / 5.0))) / 50.0)
            stab = 1.0
            quick_testing_types = get_pokemon(my_pokemon.name).types
            if (temp_move.move_type in quick_testing_types):
                stab = 1.5
            min_damage *= calc_type_matchup(temp_move.move_type, enemy_pokemon.types) * stab * 0.85 * temp_move.num_hit
            max_damage *= calc_type_matchup(temp_move.move_type, enemy_pokemon.types) * stab * temp_move.num_hit
        hp_min = (((2 * enemy_pokemon.stats[0] + 31 + (85 / 4.0)) * enemy_level) / 100.0) + enemy_level + 10
        hp_max = (((2 * enemy_pokemon.stats[0] + 31 + (85 / 4.0)) * enemy_level) / 100.0) + enemy_level + 10
        min_damage /= hp_max
        min_damage *= 1000
        min_damage = round(min_damage) / 10.0
        max_damage /= hp_min
        max_damage *= 1000
        max_damage = round(max_damage) / 10.0
        print("Damage: ", temp_move.name)
        print("Min: ", min_damage, " Max: ", max_damage)
        the_damage.append((min_damage + max_damage) / 2.0)
    damage_indexes = list()
    new_the_damage = sorted(the_damage)
    for i in range(len(new_the_damage)):
        for j in range(len(the_damage)):
            if (new_the_damage[i] == the_damage[j] and not j in damage_indexes):
                damage_indexes.append(j)
    damage_indexes.reverse()
    return damage_indexes


def advance_calculate(my_pokemon, enemy_pokemon, enemy_level, self_boosts, opp_boosts, enemy_hp):
    damage_values = list()
    for move in my_pokemon.moves:
        actual_move = get_move(move)
        damage1 = 0
        damage2 = 0
        level = 100
        try:
            level = int(enemy_level)
        except:
            pass
        if (actual_move.category != "Status"):
            attack = 0
            defense = 0
            if (actual_move.category == "Physical"):
                attack = my_pokemon.attack
                if (my_pokemon.item.lower() == "choice band"):
                    attack *= 1.5
                if (self_boosts[0] > 0):
                    attack *= 1 + 0.5 * self_boosts[0]
                elif (self_boosts[0] < 0):
                    attack *= 2.0 / (2.0 - self_boosts[0])
                defense = round((2 * enemy_pokemon.stats[2] + 31 + 85 / 4.0) * level)
                if (opp_boosts[1] > 0):
                    defense *= 1 + 0.5 * opp_boosts[1]
                elif (opp_boosts[1] < 0):
                    defense *= 2.0 / (2.0 - opp_boosts[1])
            elif (actual_move.category == "Special"):
                attack = my_pokemon.special_attack
                if (self_boosts[2] > 0):
                    attack *= 1 + 0.5 * self_boosts[2]
                elif (self_boosts[2] < 0):
                    attack *= 2.0 / (2.0 - self_boosts[2])
                if (my_pokemon.item.lower() == "choice specs"):
                    attack *= 1.5
                defense = round((2 * enemy_pokemon.stats[4] + 31 + 85 / 4.0) * level)
                if (opp_boosts[3] > 0):
                    defense *= 1 + 0.5 * opp_boosts[3]
                elif (opp_boosts[3] < 0):
                    defense *= 2.0 / (2.0 - opp_boosts[3])
            defense /= 100.0
            defense += 5
            stab = 1
            if (actual_move.move_type in get_pokemon(my_pokemon.name).types):
                stab = 1.5
            damage_reg = 2 + ((actual_move.power * attack / defense * (2 + (2 * level / 5.0))) / 50.0)
            damage_reg *= calc_type_matchup(actual_move.move_type, enemy_pokemon.types) * stab * actual_move.num_hit
            if (my_pokemon.item.lower() == "life orb"):
                damage_reg *= 1.3
            hp = round((((2 * enemy_pokemon.stats[0] + 31 + (85 / 4.0)) * level) / 100.0) + level + 10)
            damage1 = damage_reg * 0.85
            damage1 /= hp
            damage1 *= 1000.0
            damage1 = round(damage1)
            damage1 /= 10.0
            damage2 = damage_reg
            damage2 /= hp
            damage2 *= 1000.0
            damage2 = round(damage2)
            damage2 /= 10.0
        print(move)
        print("Damage1: ", damage1, " Damage2: ", damage2)
        damage_values.append(damage1)
    # print(damage_values)
    priority_indexes = list()
    move_indexes = list()
    for i in range(4):
        priority_indexes.append(0)
        if(damage_values[i] > enemy_hp):
            priority_indexes[i] = 10
        elif(damage_values[i] > enemy_hp / 2):
            priority_indexes[i] = 8
        elif(damage_values[i] > enemy_hp / 3):
            priority_indexes[i] = 6
        elif (damage_values[i] > enemy_hp / 4):
            priority_indexes[i] = 4
        elif (damage_values[i] > enemy_hp / 5):
            priority_indexes[i] = 2
        actual_move = get_move(my_pokemon.moves[i])
        if(actual_move.priority > 0):
            priority_indexes[i] += 1
    for i in range(4):
        temp_index = max(priority_indexes)
        for j in range(4):
            if(priority_indexes[j] == temp_index and not j in move_indexes):
                move_indexes.append(j)
                priority_indexes[j] = 0
                break
    return move_indexes

def calculate_random():
    damage_indexes = list([0, 1, 2, 3])
    random.shuffle(damage_indexes)
    return damage_indexes
