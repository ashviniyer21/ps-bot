import requests
class Move:
    def __init__(self, name, move_type, category, power, acc, target, status, stats, priority, num_hit):
        self.name = name
        self.move_type = move_type
        self.category = category
        self.power = power
        self.acc = acc
        self.target = target
        self.status = status
        self.stats = stats
        self.priority = priority
        self.num_hit = num_hit
    def print(self):
        print(self.name)
        print(self.move_type)
        print(self.category)
        print(self.power)
        print(self.acc)
        print(self.target)
        print(self.status)
        print(self.stats)
        print(self.priority)
        print(self.num_hit)
        print()
        print()
        print()
def get_all_moves():
    url='http://play.pokemonshowdown.com/data/moves.js'
    page = requests.get(url)
    text = page.text[24:]
    text = text[:len(text)-1]
    counter = 0
    moves = list()
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
        if(text.find("multihit:") < text.find(",type:\"") and text.find("multihit:") != -1 and text.find("multihit:") < text.find("secondary:")):
            index1 = text.find("multihit:")
            text = text[index1:]
            index1 = text.find("multihit:") + 9
            index2 = text.find(",")
            try:
                num_hit = int(text[index1:index2])
            except:
                num_hit = 3
        status = "none"
        if(text.find("status:") < text.find(",type:\"") and text.find("status:") != -1 and text.find("status:") < text.find("secondary:")):
            index1 = text.find("status:")
            text = text[index1:]
            index1 = text.find("status:") + 7
            index2 = text.find(",")
            status = text[index1:index2]
        index2 = text.find("},")
        index1 = text.find("target:\"")
        text = text[index1:]
        index1 = text.find("target:\"") + 8
        index2 = text.find("\",")
        target = text[index1:index2]
        index1 = text.find(",type:\"") + 1
        text = text[index1:]
        index1 = text.find("type:\"") + 6
        index2 = text.find("\",")
        move_type = text[index1:index2].lower()
        #if(counter < 20):
         #   print(accuracy)
          #  print(power)
           # print(category)
            #print(description)
            #print(name)
            #print(priority)
            #print(boosts)
            #print(secondary_text)
            #print(move_type)
            #print(status)
            #print()
        counter += 1
        moves.append(Move(name, move_type, category, power, accuracy, target, status, boosts, priority, num_hit))
    return moves
all_moves = get_all_moves()
def get_move(name):
    name = name.replace(" ", "")
    for i in range(len(all_moves)):
        if(all_moves[i].name.lower().replace(" ", "").replace("-", "") == name.lower() or all_moves[i].name.lower().replace(" ", "").replace("-", "") == name[:len(name)-1].lower()):
            return all_moves[i]
    return all_moves[0]
get_move("Thunder Wave").print()
