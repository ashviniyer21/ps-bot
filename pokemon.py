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
