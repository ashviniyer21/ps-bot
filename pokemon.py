import requests
class EnemyPokemon:
    def __init__(self, name, types, stats):
        self.name = name
        self.types = types
        self.stats = stats
    def print(self):
        print("Name: ", self.name)
        print("Types: ", self.types)
        print("Stats: ", self.stats)

class Pokemon:
    def __init__(self, name, level, gender, moves, ability, item, max_hp, hp, attack, defense, special_attack, special_defense, speed):
        self.name = name
        self.level = level
        self.gender = gender
        self.moves = moves
        self.ability = ability
        self.item = item
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed;
    def set_hp(self, hp):
        self.hp = hp
    def print(self):
        print("Name: ", self.name)
        print("Level: ", self.level)
        print("Gender: ", self.gender)
        print("Moves: ", self.moves)
        print("Ability: ", self.ability)
        print("Item: ", self.item)
        print("HP: ", self.hp, "/", self.max_hp)
        print("Attack: ", self.attack)
        print("Defense: ", self.defense)
        print("SPA: ", self.special_attack)
        print("SPD: ", self.special_defense)
        print("SPEED: ", self.speed)
def get_all_pokemon():
    pokemons = list()
    url='http://play.pokemonshowdown.com/data/pokedex.js'
    page = requests.get(url)
    text = page.text
    text = text[24:len(text)-1]
    counter = 0
    while(text.find("name:\"") != -1):
        index1 = text.find("name:\"")
        text = text[index1:]
        index1 = text.find("name:\"") + 6
        index2 = text.find("\",")
        name = text[index1:index2]
        index1 = text.find("types:")
        text = text[index1:]
        index1 = text.find("types:") + 7
        index2 = text.find("\"],") + 1
        type_string = text[index1: index2]
        type_string = type_string.replace("\"", "")
        types = type_string.split(",")
        for i in range(len(types)):
            types[i] = types[i].lower()
        index1 = text.find("baseStats:")
        text = text[index1 + 10:]
        index2 = text.find("},") + 1
        stats_string = text[:index2]
        stats_string = stats_string[1: len(stats_string)-1]
        stats_temp = stats_string.split(",")
        stats = list()
        for stat in stats_temp:
            stats.append(int(stat[stat.find(":") + 1:]))
        pokemons.append(EnemyPokemon(name, types, stats))
    return pokemons
all_pokemon = get_all_pokemon()
def get_pokemon(name):
    for i in range(len(all_pokemon)):
        if(all_pokemon[i].name == name):
            return all_pokemon[i]
    return all_pokemon[0]
get_pokemon("charmander").print()
