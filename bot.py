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
from calculations import calculate
from calculations import calculate_random
import time
pokemons = get_all_pokemon()

console_debug = False

general_debug = True

random_move = False

enemy_pokemon = EnemyPokemon("HI", ["hi"], [0])
enemy_level = 100
print("STARTING")

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
already_finding = False
driver = webdriver.Chrome(desired_capabilities=d)
driver.get("https://play.pokemonshowdown.com/")
gameStart = False
initialize = False
isP1 = False
move_index = 0
mapthing = dict()
temp_map = dict()
startPokemon = Pokemon("Blitzle", "L88", "F", ["1", "2", "3", "4"], "Motor Drive", "Choice Band", 1, 1, 1, 1, 1, 1, 1)
myPokemon = [startPokemon, startPokemon, startPokemon, startPokemon, startPokemon, startPokemon]
count = 0;
oppMon = ""
should_skip = True
can_start = False
one_mon_temp = ""
two_mon_temp = ""
start_len = -1
while(True):
    time.sleep(10)
    for entry in driver.get_log('browser'):
        temp_value = str(entry).replace("\\", "")
        value = dict()
        try:
            value = ast.literal_eval(temp_value)
        except:
            value = entry
        for x, y in value.items():
            if(len(str(y)) > 500):
                z = y[119:len(str(y))-1]
                try:
                    mapthing = json.loads(z)
                    pkmn = mapthing['side']
                    pkmn2 = pkmn['pokemon']
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
                        counter = counter + 1
                        can_start = True
                except Exception as e:
                    mapthing = dict()
                    print(e)
                
            if(str(y).find("|p1a: ") != -1 or str(y).find("|p2a: ") != -1):
                values = str(y).split("|")
                print(values)
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
                for value in range(len(values)):
                    if(values[value].find("switch") != -1 and value + 2 < len(values)):
                        if(values[value + 1].find("p1a: ") != -1):
                            one_mon_temp = values[value+2].split(",")[0]
                        elif(values[value + 1].find("p2a: ") != -1):
                            two_mon_temp = values[value+2].split(",")[0]
                print("P1: ", one_mon_temp, " P2: ", two_mon_temp)
                if(isP1):
                    oppMon = two_mon_temp
                    temp_test_string = str(y)[str(y).find("|p2a: "):]
                    if(temp_test_string.find(", L") > temp_test_string.find("|p2a: ")):
                        try:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 6])
                        except:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 5])
                        if(general_debug): print("Enemy Level: ", enemy_level)
                else:
                    oppMon = one_mon_temp
                    temp_test_string = str(y)[str(y).find("|p1a: "):]
                    if(temp_test_string.find(", L") > temp_test_string.find("|p1a: ")):
                        try:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 6])
                        except:
                            enemy_level = int(temp_test_string[temp_test_string.find(", L") + 3: temp_test_string.find(", L") + 5])
                        if(general_debug): print("Enemy Level: ", enemy_level)
                for the_pokemon in pokemons:
                    if(the_pokemon.name == oppMon or the_pokemon.name[:len(the_pokemon.name)-1] == oppMon):
                        enemy_pokemon = the_pokemon
                        break
                if(general_debug): print(enemy_pokemon.name)
                if(general_debug): print(enemy_pokemon.types)
                page_source = driver.page_source
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
                if(start_len == -1):
                    start_len = len(disabled_moves)
                if(not random_move): move_indexes = calculate(myPokemon[0], enemy_pokemon, enemy_level)
                else: move_indexes = calculate_random()
                move_index = move_indexes[0]
                for i in range(len(move_indexes)):
                    move_index = move_indexes[i]
                    if(disabled_moves[move_index] == False):
                        break
                move_decrement = 0
                for i in range(len(disabled_moves)):
                    if(disabled_moves[i] and move_index > i):
                        move_decrement += 1
                if(general_debug): print("Moves: ", move_indexes)
                if(general_debug): print(disabled_moves)
                if(general_debug): print("Move before: ", move_index)
                move_index -= move_decrement
                if(general_debug): print("Move after: ", move_index)
                if(len(disabled_moves) != start_len):
                    move_index = 0
            if(console_debug): print(x, y)
    if(can_start):
        if(should_skip):
            should_skip = False
        else:
            should_skip = True
            while(True):
                try: 
                    driver.find_elements_by_name('chooseMove')[move_index].click()
                    break
                except:
                    pass
