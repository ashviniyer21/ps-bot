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
def get_all_moves2():
    url='http://play.pokemonshowdown.com/data/moves.js'
    page = requests.get(url)
    text = page.text[24:]
    text = text[:len(text)-1]
    counter = 0
    while(text.find("accuracy:") != -1):
        index1 = text.find("accuracy:")
        text = text[index1:]
        index1 = text.find("accuracy:") + 9
        index2 = text.find(",")
        accuracy = -1
        try:
            accuracy = int(text[index1: index2])
        except:
            pass
        text = text[index2 + 1:]
        index1 = text.find("basePower:") + 10
        index2 = text.find(",")
        power = 0
        try:
            power = int(text[index1: index2])
        except:
            pass
        text = text[index2 + 1:]
        index1 = text.find("category:\"") + 10
        index2 = text.find("\",")
        category = text[index1: index2]
        index1 = text.find("shortDesc:")
        text = text[index1:]
        index1 = text.find("shortDesc:\"") + 11
        index2 = text.find("\",")
        description = text[index1: index2]
        index1 = text.find("name:\"")
        text = text[index1:]
        index1 = text.find("name:\"") + 6
        index2 = text.find("\",")
        name = text[index1: index2]
        index1 = text.find("priority:")
        text = text[index1:]
        index1 = text.find("priority:") + 9
        index2 = text.find(",")
        priority = int(text[index1: index2])
        boosts = [0, 0, 0, 0, 0]
        if(text.find(",boosts:") < text.find(",type:\"") and text.find(",boosts:") < text.find("secondary:") and text.find(",boosts:") != -1):
            index1 = text.find(",boosts:") + 1
            text = text[index1:]
            index1 = text.find("boosts:{") + 8
            index2 = text.find("}")
            boosts_text = text[index1: index2].split(",")
            for boost_text in boosts_text:
                boost_values = boost_text.split(":")
                if(boost_values[0] == "atk"):
                    boosts[0] = int(boost_values[1])
                elif(boost_values[0] == "def"):
                    boosts[1] = int(boost_values[1])
                elif(boost_values[0] == "spa"):
                    boosts[2] = int(boost_values[1])
                elif(boost_values[0] == "spd"):
                    boosts[3] = int(boost_values[1])
                elif(boost_values[0] == "spe"):
                    boosts[4] = int(boost_values[1])
        num_hit = 1
        if(text.find("multihit:") < text.find(",type:\"") and text.find("multihit:") != -1):
            index1 = text.find("multihit:")
            text = text[index1:]
            index1 = text.find("multihit:") + 9
            index2 = text.find(",")
            num_hit = int(text[index1:index2])
        if(text.find("status:") < text.find(",type:\"") and text.find("status:") != -1):
            index1 = text.find("status:")
            text = text[index1:]
            index1 = text.find("status:") + 7
            index2 = text.find(",")
            status = text[index1:index2]
        index2 = text.find("},")
        index1 = text.find(",type:\"") + 1
        text = text[index1:]
        index1 = text.find("type:\"") + 6
        index2 = text.find("\",")
        move_type = text[index1:index2].lower()
        if(counter < 20):
            print(accuracy)
            print(power)
            print(category)
            print(description)
            print(name)
            print(priority)
            print(boosts)
            print(secondary_text)
            print(move_type)
            print()
        counter += 1

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
    for i in range(len(all_moves)):
        if(all_moves[i].name.lower().replace(" ", "").replace("-", "") == name.lower() or all_moves[i].name.lower().replace(" ", "").replace("-", "") == name[:len(name)-1].lower()):
            return all_moves[i]
    return all_moves[0]
get_all_moves2()
