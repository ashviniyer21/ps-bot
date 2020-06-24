from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import ast
import json
import requests, six
import lxml.html as lh
from pokemon import EnemyPokemon
from move import Move
from pokemon import Pokemon


url='https://pokemondb.net/pokedex/all'
page = requests.get(url)
text = page.text
index1 = text.find("<table")
index2 = text.find("</table>") + 8
s = text[index1:index2]
pokemons = list()
s = s[806:]
index = 0
while(s.find("<tr>") != -1):
    o_index = s.find("</tr>") + 5
    temp = s[:o_index]
    s = s[o_index:]
    new_index1 = temp.find("data-alt=\"") + 10
    new_index2 = temp.find(" icon\">")
    name = temp[new_index1: new_index2]
    new_index2 = temp.find("</a>") + 4
    temp = temp[new_index2:]
    types = list()
    while(temp.find("href=\"/type/") != -1):
        new_index1 = temp.find("href=\"/type/") + 12
        new_index2 = temp.find("</a>")
        new_type = temp[new_index1: new_index2]
        new_type = new_type[:int((len(new_type) - 2)/2)]
        temp = temp[new_index2 + 4:]
        types.append(new_type)
    new_index2 = temp.find("</td>")
    temp = temp[new_index2 + 4:]
    new_index2 = temp.find("</td>")
    temp = temp[new_index2 + 4:]
    stats = list()
    for i in range(6):
        new_index1 = temp.find("<td class=\"cell-num\">") + 21
        new_index2 = temp.find("</td>")
        stats.append(int(temp[new_index1: new_index2]))
        temp = temp[new_index2 + 4:]
    pokemon = EnemyPokemon(name, types, stats)
    pokemons.append(pokemon)
    #if(index < 20):
     #   pokemons[index].print()
    index = index + 1




enemy_pokemon = EnemyPokemon("HI", ["hi"], [0])
enemy_level = 100
url='http://pokemondb.net/move/all'
page = requests.get(url)
text = page.text
index1 = text.find("<table")
index2 = text.find("</table>") + 8
s = text[index1:index2]
moves = list()
s = s[796:]
index = 0
while(s.find("<tr>") != -1):
    o_index = s.find("</tr>") + 5
    temp = s[:o_index]
    s2 = temp
    test_index1 = temp.find("title=\"View details for ") + 24
    test_index2 = temp.find("</a>")
    name = temp[test_index1: test_index2]
    name = name[:int((len(name)-2)/2)]
    temp = temp[test_index2 + 4:]
    test_index1 = temp.find("href=\"/type/") + 12
    test_index2 = temp.find("</a>")
    move_type = temp[test_index1: test_index2]
    move_type = move_type[:int((len(move_type)-2)/2)]
    temp = temp[test_index2 + 4:]
    test_index1 = temp.find("data-sort-value=\"") + 17
    category = temp[test_index1: test_index1 + 3]
    if(category == "spe"):
        category = "special"
        temp = temp[test_index1 + 200:]
    elif(category == "sta"):
        temp = temp[test_index1 + 200:]
        category = "status"
    else:
        temp = temp[test_index1 + 205:]
        category = "physical"
    test_index1 = temp.find("<td class=\"cell-num\">") + 21
    test_index2 = temp.find("</td>")
    power = 0
    try:
        power = int(temp[test_index1:test_index2])
    except:
        pass
    temp = temp[test_index2 + 4:]
    accuracy = -1
    test_index1 = temp.find("<td class=\"cell-num\">") + 21
    test_index2 = temp.find("</td>")
    try:
        accuracy = int(temp[test_index1:test_index2])
    except:
        pass
    temp = temp[test_index2 + 4:]
    pp = -1
    test_index1 = temp.find("<td class=\"cell-num\">") + 21
    test_index2 = temp.find("</td>")
    try:
        pp = int(temp[test_index1:test_index2])
    except:
        pass
    test_index1 = temp.find("<td class=\"cell-long-text\"")
    temp = temp[test_index1:]
    test_index1 = temp.find("<td class=\"cell-long-text\"") + 27
    test_index2 = temp.find("</td>")
    effect = temp[test_index1: test_index2]
    effect = effect.lower()
    temp = temp[test_index2 + 4:]
    prob = 100
    test_index1 = temp.find("<td class=\"cell-num\">") + 21
    test_index2 = temp.find("</td>")
    try:
        prob = int(temp[test_index1:test_index2])
    except:
        pass
    status_opponent = "None"
    status_self = "None"
    stat_change_self = [0, 0, 0, 0, 0]
    stat_change_opponent = [0, 0, 0, 0, 0]
    if(effect.find("user") != -1):
        if(effect.find("paralyze") != -1):
            status_self = "Paralysis"
        elif(effect.find("sleep") != -1):
            status_self = "Sleep"
        elif(effect.find("poison") != -1):
            status_self = "Poison"
        elif(effect.find("burn") != -1):
            status_self = "Burn"
        elif(effect.find("freeze") != -1):
            status_self = "Frozen"
        elif(effect.find("confuse") != -1):
            status_self = "Confusion"
        raise_index = effect.find("raise")
        lower_index = effect.find("lower")
        if(effect.find("attack") > raise_index and effect.find("attack") != effect.find("special attack") + 8 and raise_index != -1):
            stat_change_self[0] = 1
        elif(effect.find("attack") > lower_index and effect.find("attack") != effect.find("special attack") + 8 and lower_index != -1):
            stat_change_self[0] = -1
        if(effect.find("defense") > raise_index and effect.find("defense") != effect.find("special defense") + 8 and raise_index != -1):
            stat_change_self[1] = 1
        elif(effect.find("defense") > lower_index and effect.find("defense") != effect.find("special defense") + 8 and lower_index != -1):
            stat_change_self[1] = -1
        if(effect.find("special attack") > raise_index and raise_index != -1):
            stat_change_self[2] = 1
        elif(effect.find("special attack") > lower_index and lower_index != -1):
            stat_change_self[2] = -1
        if(effect.find("special defense") > raise_index and raise_index != -1):
            stat_change_self[3] = 1
        elif(effect.find("special defense") > lower_index and lower_index != -1):
            stat_change_self[3] = -1
        if(effect.find("speed") > raise_index and raise_index != -1):
            stat_change_self[4] = 1
        elif(effect.find("speed") > lower_index and lower_index != -1):
            stat_change_self[4] = -1
        mult = 1
        if(effect.find("sharply") != -1):
            mult = 2
        elif(effect.find("drastically") != -1):
            mult = 3
        for i in range(5):
            stat_change_self[i] *= mult
    else:
        if(effect.find("paralyze") != -1):
            status_opponent = "Paralysis"
        elif(effect.find("sleep") != -1):
            status_opponent = "Sleep"
        elif(effect.find("poison") != -1):
            status_opponent = "Poison"
        elif(effect.find("burn") != -1):
            status_opponent = "Burn"
        elif(effect.find("freeze") != -1):
            status_opponent = "Frozen"
        elif(effect.find("confuse") != -1):
            status_opponent = "Confusion"
        raise_index = effect.find("raise")
        lower_index = effect.find("lower")
        if(effect.find("attack") > raise_index and effect.find("attack") != effect.find("special attack") + 8 and raise_index != -1):
            stat_change_opponent[0] = 1
        elif(effect.find("attack") > lower_index and effect.find("attack") != effect.find("special attack") + 8 and lower_index != -1):
            stat_change_opponent[0] = -1
        if(effect.find("defense") > raise_index and effect.find("defense") != effect.find("special defense") + 8  and raise_index != -1):
            stat_change_opponent[1] = 1
        elif(effect.find("defense") > lower_index and effect.find("defense") != effect.find("special defense") + 8 and lower_index != -1):
            stat_change_opponent[1] = -1
        if(effect.find("special attack") > raise_index and raise_index != -1):
            stat_change_opponent[2] = 1
        elif(effect.find("special attack") > lower_index and lower_index != -1):
            stat_change_opponent[2] = -1
        if(effect.find("special defense") > raise_index and raise_index != -1):
            stat_change_opponent[3] = 1
        elif(effect.find("special defense") > lower_index and lower_index != -1):
            stat_change_opponent[3] = -1
        if(effect.find("speed") > raise_index and raise_index != -1):
            stat_change_opponent[4] = 1
        elif(effect.find("speed") > lower_index and lower_index != -1):
            stat_change_opponent[4] = -1
        mult = 1
        if(effect.find("sharply") != -1):
            mult = 2
        elif(effect.find("drastically") != -1):
            mult = 3
        for i in range(5):
            stat_change_opponent[i] *= mult
    move = Move(name, move_type, category, power, accuracy, pp, effect, prob, status_self, status_opponent, stat_change_self, stat_change_opponent)
    moves.append(move)
    s = s[o_index:]
    index = index + 1
print("MOVES")
def get_move(name):
    if(isinstance(type(moves[0]), Move)):
        print("WORKS")
    else:
        print("NOT WORKS")
    for i in range(len(moves)):
        if(moves[i].name.lower().replace(" ", "").replace("-", "") == name.lower() or moves[i].name.lower().replace(" ", "").replace("-", "") == name[:len(name)-1].lower()):
            return moves[i]
    return moves[0]

def get_pokemon(name):
    for i in range(len(moves)):
        if(pokemons[i].name == name):
            return pokemons[i]
    return pokemons[0]

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
