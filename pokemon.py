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
    url='https://pokemondb.net/pokedex/all'
    page = requests.get(url)
    text = page.text
    index1 = text.find("<table")
    index2 = text.find("</table>") + 8
    s = text[index1:index2]
    pokemons = list()
    s = s[806:]
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
    return pokemons
all_pokemon = get_all_pokemon()
def get_pokemon(name):
    for i in range(len(all_pokemon)):
        if(all_pokemon[i].name == name):
            return all_pokemon[i]
    return all_pokemon[0]
