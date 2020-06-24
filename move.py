import requests
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

def get_all_moves():
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
    return moves
all_moves = get_all_moves()
def get_move(name):
    if(isinstance(type(all_moves[0]), Move)):
        print("WORKS")
    else:
        print("NOT WORKS")
    for i in range(len(all_moves)):
        if(all_moves[i].name.lower().replace(" ", "").replace("-", "") == name.lower() or all_moves[i].name.lower().replace(" ", "").replace("-", "") == name[:len(name)-1].lower()):
            return all_moves[i]
    return all_moves[0]
