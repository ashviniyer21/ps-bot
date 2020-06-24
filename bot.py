from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import ast
import json
from pokemon import EnemyPokemon
from move import Move
from pokemon import Pokemon
from pokemon import get_all_pokemon
from pokemon import get_pokemon
from move import get_move

pokemons = get_all_pokemon()

enemy_pokemon = EnemyPokemon("HI", ["hi"], [0])
enemy_level = 100
print("MOVES")

def calc_type_matchup(move_type, pokemon_types):
    chart = dict()

    normal_chart = dict()
    normal_chart["strength"] = list()
    normal_chart["weakness"] =  ["rock", "steel"]
    normal_chart["immunity"] =  ["ghost"]
    chart["normal"] = normal_chart

    fire_chart = dict()
    fire_chart["strength"] = ["grass", "ice", "bug", "steel"]
    fire_chart["weakness"] = ["fire", "water", "rock", "dragon"]
    fire_chart["immunity"] = list()
    chart["fire"] = fire_chart

    water_chart = dict()
    water_chart["strength"] = ["fire", "ground", "rock"]
    water_chart["weakness"] = ["water", "grass", "dragon"]
    water_chart["immunity"]  = list()
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
        if(pkmn_type in the_chart["strength"]):
            mult *= 2.0
        elif(pkmn_type in the_chart["weakness"]):
            mult *= 0.5
        elif(pkmn_type in the_chart["immunity"]):
            return 0
    return mult

def calculate(my_pokemon, enemy_pokemon):
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
        if(temp_move.category == "physical"):
            atk = my_pokemon.attack
            def_min = 2 * enemy_pokemon.stats[2] * enemy_level
            def_min /= 100.0
            def_min += 5
            def_min *= 0.9
            def_max = (2 * enemy_pokemon.stats[2] + 31 + 63) * enemy_level
            def_max /= 100.0
            def_max += 5
            def_max *= 1.1
        elif(temp_move.category == "special"):
            atk = my_pokemon.special_attack
            def_min = 2 * enemy_pokemon.stats[4] * enemy_level
            def_min /= 100.0
            def_min += 5
            def_min *= 0.9
            def_max = (2 * enemy_pokemon.stats[4] + 31 + 63) * enemy_level
            def_max /= 100.0
            def_max += 5
            def_max *= 1.1
        if(temp_move.category != "status"):
            print(my_pokemon.level)
            min_damage = 2 + ((temp_move.power * atk/def_min * (2 + (2 * my_pokemon.level/5.0)))/50.0)
            max_damage = 2 + ((temp_move.power * atk/def_max * (2 + (2 * my_pokemon.level/5.0)))/50.0)
            stab = 1.0
            quick_testing_types = get_pokemon(my_pokemon.name).types
            if(temp_move.move_type in quick_testing_types):
                stab = 1.5
            min_damage *= calc_type_matchup(temp_move.move_type, enemy_pokemon.types) * stab * 0.85
            max_damage *= calc_type_matchup(temp_move.move_type, enemy_pokemon.types) * stab
        print("Damage: ", temp_move.name)
        print(max_damage)
        the_damage.append(max_damage)
    damage_indexes = list()
    new_the_damage = sorted(the_damage)
    for i in range(len(new_the_damage)):
        for j in range(len(the_damage)):
            if(new_the_damage[i] == the_damage[j] and not j in damage_indexes):
                damage_indexes.append(j)
    damage_indexes.reverse()
    return damage_indexes

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
already_finding = False
driver = webdriver.Chrome(desired_capabilities=d)
driver.get("https://play.pokemonshowdown.com/")
gameStart = False
initialize = False
isP1 = False
mapthing = dict()
temp_map = dict()
startPokemon = Pokemon("Blitzle", "L88", "F", ["1", "2", "3", "4"], "Motor Drive", "Choice Band", 1, 1, 1, 1, 1, 1, 1)
myPokemon = [startPokemon, startPokemon, startPokemon, startPokemon, startPokemon, startPokemon]
count = 0;
oppMon = ""
while(True):
    for entry in driver.get_log('browser'):
        temp_value = str(entry).replace("\\", "")
        print()
        value = dict()
        try:
            value = ast.literal_eval(temp_value)
        except:
            value = entry
        #print(temp_value)
        for x, y in value.items():
            if(len(str(y)) > 500):
                z = y[119:len(str(y))-1]
                try:
                    mapthing = json.loads(z)
                    print(mapthing['active'])
                    pkmn = mapthing['side']
                    #print(pkmn_string)
                    pkmn2 = pkmn['pokemon']
                    #for a, in pkmn2:
                     #   print(a)
                    counter = 0
                    for index in pkmn2:
                        name = index['details'].split(',')[0]
                        level = int(index['details'].split(',')[1][2:])
                        gender = " "
                        try:   
                            gender = index['details'].split(',')[2]
                        except:
                            gender = " "
                        moves2 = index['moves']
                        ability = index['ability']
                        item = index['item']
                        max_hp = 0
                        hp = 0
                        try:
                            max_hp = index['condition'].split('/')[1]
                            hp = index['condition'].split('/')[0]
                        except:
                            max_hp = 0
                            hp = 0
                        stats = index['stats']
                        atk = stats['atk']
                        defe = stats['def']
                        spa = stats['spa']
                        spd = stats['spd']
                        spe = stats['spe']
                        myPokemon[counter] = Pokemon(name, level, gender, moves2, ability, item, max_hp, hp, atk, defe, spa, spd, spe)
                        #myPokemon[counter].print()
                        print()
                        
                        counter = counter + 1
                    print()
                    print()
                    
                except Exception as e:
                    mapthing = dict()
                    print(e)
                
            if(str(y).find("|p1a: ") != -1 or str(y).find("|p2a: ") != -1):
                values = str(y).split("|")
                p1A = ""
                p2A = ""
                found1 = False
                found2 = False
                for value in values:
                    if(value.find("p1a: ") != -1 and found1 == False):
                        found1 = True
                        p1A = value[5:]
                    if(value.find("p2a: ") != -1 and found2 == False):
                        found2 = True
                        p2A = value[5:]
                if(not already_finding): 
                    isP1 = False
                    for pokemon in myPokemon:
                        if(p1A == pokemon.name):
                            isP1 = True
                            break
                    already_finding = True
                if(isP1):
                    oppMon = p2A
                    temp_test_string = str(y)[str(y).find("|p2a: "):]
                    if(temp_test_string.find(", L") > temp_test_string.find("|p2a: ")):
                        try:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 6])
                        except:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 5])
                        print("Enemy Level: ", enemy_level)
                else:
                    oppMon = p1A
                    temp_test_string = str(y)[str(y).find("|p1a: "):]
                    if(temp_test_string.find(", L") > temp_test_string.find("|p1a: ")):
                        try:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 6])
                        except:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 5])
                        print("Enemy Level: ", enemy_level)
                for the_pokemon in pokemons:
                    if(the_pokemon.name == oppMon or the_pokemon.name[:len(the_pokemon.name)-1] == oppMon):
                        enemy_pokemon = the_pokemon
                        break
                print(enemy_pokemon.name)
                print(enemy_pokemon.types)
                #moves[0].print()
                page_source = driver.page_source
                print(page_source)
                while(page_source.find("<div class=\"movemenu\"") == -1):
                    page_source = driver.page_source
                page_source = page_source[page_source.find("<div class=\"movemenu\""):]
                disabled_moves = list()
                while(page_source.find("<button") != -1):
                    if(page_source.find("disabled=\"disabled\"") != -1 and page_source.find("disabled=\"disabled\"") < page_source.find("</button>")):
                        disabled_moves.append(True)
                    else:
                        disabled_moves.append(False)
                    page_source = page_source[1:]
                    page_source = page_source[page_source.find("</button>") + 9:]
                #print(page_source)
                move_indexes = calculate(myPokemon[0], enemy_pokemon)
                move_index = move_indexes[0]
                move_decrement = 0
                for i in range(len(disabled_moves)):
                    if(disabled_moves[i] and move_index > i):
                        move_decrement += 1
                print("Moves: ", move_indexes)
                print(disabled_moves)
                for i in range(len(move_indexes)):
                    move_index = move_indexes[i]
                    print("TRAPPED IN LOOP")
                    if(disabled_moves[i] == False):
                        break
                print("Move before: ", move_index)
                move_index -= move_decrement
                print("Move after: ", move_index)
                while(True):
                  try: 
                    driver.find_elements_by_name('chooseMove')[move_index].click()
                    break
                  except:
                    pass
            print(x, y)
        if(str(entry).find("battle-gen8randombattle") != -1):
            gameStart = True
        if(str(entry).find("moves") != -1 and initialize == False):
            initialize = True
            print("HERE")
