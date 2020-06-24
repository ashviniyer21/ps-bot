class Move:
    def __init__(self, name, move_type, category, power, acc, pp, effect, prob, status_self, status_opponent, stats_self, stats_opponent):
        self.name = name
        self.move_type = move_type
        self.category = category
        self.power = power
        self.acc = acc
        self.pp = pp
        self.effect = effect
        self.prob = prob
        self.status_self = status_self
        self.status_opponent = status_opponent
        self.stats_self = stats_self
        self.stats_opponent = stats_opponent
    def print(self):
        print(self.name)
        print(self.move_type)
        print(self.category)
        print(self.power)
        print(self.acc)
        print(self.pp)
        print(self.effect)
        print(self.prob)
        print(self.status_self)
        print(self.status_opponent)
        print(self.stats_self)
        print(self.stats_opponent)
        print()
        print()
        print()
