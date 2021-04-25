import random
import json
with open("./deck.json","r") as f:
 deck = json.load(f)
    
def rand_card_generator(fall_off=0):
    rand_card = random.randint(0,(len(deck)-1)-fall_off)
    return deck[rand_card]

def playableChecker  (player_card,facedUp_card,rand_color = None):

    if player_card["color"] == facedUp_card["color"] or player_card["sign"] == facedUp_card["sign"] or player_card["color"] == rand_color or player_card["sign"] == "wild" or player_card["sign"] == "draw4": 
        return {"card":player_card,"playable":True}
  
def wildCard():
    colors = ["yellow", "red", "green", "blue"]
    return colors[random.randint(0,len(colors)-1)]

def uno_called(queue):
    for unit in queue.units:
        if len(unit.hand) == 1:
            unit.hand.append(rand_card_generator(fall_off=0))
            unit.hand.append(rand_card_generator(fall_off=0))
            print(queue.get_current_unit().name+" has called UNO on "+unit.name)
            print(unit.name+" has drawn 2 cards.")
            break       
       
class Queue:
    def __init__(self):
        self.units = []

    def add_unit(self,unit):
        if not(unit):
            return print("No unit was added!")
        
        return self.units.append(unit)

    def move_unit_back(self):
        self.units.append(self.units.pop(0))

    def remove_unit(self,index=0):
        self.units.pop(index)

    def get_current_unit(self):
        return self.units[0]
    
    def print_queue(self):
        if len(self.units)<1:
            return print("Under flow")
        return self.units

    def reverse_queue(self):
        self.units.reverse()

class Unit_Generator:
    def __init__(self,name,is_player= False):
        self.name=name
        self.hand=[]
        self.is_player = is_player
   
    def generate_new_hand(self, size =7):
        i = 0
        new_deck = [] 
        while i < size:
            new_deck.append(rand_card_generator())
            i+=1
        self.hand = new_deck

    def remove_card(self,card):
        self.hand.pop(self.hand.index(card))
    
    def draw_card(self):
        self.hand.append(rand_card_generator())

class Specials:
    def __init__(self,queue):
        self.draw_rate = 0
        self.queue = queue

    def forced_draw(self):
        drawed_hand = []
    
        while self.draw_rate > 0:
            drawed_hand.append(rand_card_generator())
            self.draw_rate-=1

        self.draw_rate = 0
        return drawed_hand

    def skip_unit(self):
        self.queue.move_unit_back()
  
    def reverse_turns(self):
        self.queue.reverse_queue()
    
    def change_color(self,color):
        wild_color = color
        return wild_color

draw_rate = 0
wild_color =  None
pile_top = rand_card_generator(2)

  
 
# queue = Queue() 
# queue.add_unit(Unit_Generator("Willy"))
# queue.get_current_unit().generate_new_hand()

# print(queue.get_current_unit().hand[0]["name"])

# print(pile_top["name"])
# print(queue.get_current_unit().hand)
# playableChecker(queue.get_current_unit().hand[0],queue.get_current_unit().hand[1],None)

 