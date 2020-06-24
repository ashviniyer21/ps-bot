class EnemyPokemon:
    def __init__(self, name, types, stats):
        self.name = name
        self.types = types
        self.stats = stats
    def print(self):
        print("Name: ", self.name)
        print("Types: ", self.types)
        print("Stats: ", self.stats)
