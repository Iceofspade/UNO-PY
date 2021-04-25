import logic 
import random
import time
queue = logic.Queue()

AI_Names = ["Jacob","One time Mike","Tucker"]
print("Welcome to UNO in Python")

def start_game():
    player_name = str(input("Please input a name to start:  ")).lower()
    if player_name == "":
        return start_game()
    else:
        #player
        new_unit = logic.Unit_Generator(str(player_name),True)
        #AI
        new_ai_unit = logic.Unit_Generator(AI_Names[0])

        queue.add_unit(new_unit)
        queue.add_unit(new_ai_unit)

        for unit in queue.units:
            unit.generate_new_hand(7)

def Specials(card,color = None):
    if card["sign"] == "wild":
        logic.wild_color = color
        print("A wild was played new color is "+color)
    elif card["sign"] == "draw4":
        logic.wild_color = color
        logic.draw_rate+=4
        print("draw4 was played new color is "+color)
        return
    elif card["sign"] == "skip":
        queue.move_unit_back()
        print(queue.get_current_unit().name+" has been skipped")

    elif card["sign"] == "reverse":
        queue.reverse_queue()
        print("Game has been reverse")
    elif card["sign"] == "draw2":
        logic.draw_rate+=2
        print("draw2 was played")
        return
    if logic.draw_rate > 0:     
        print(queue.get_current_unit().name+" has drawn "+str(logic.draw_rate)+" cards")
        while logic.draw_rate > 0:
            queue.get_current_unit().hand.append(logic.rand_card_generator())
            logic.draw_rate-=1

        logic.wild_color = color
    
def color_queue():
    choice = str(input("Pick a color: ")).lower()
    if choice == "red" or choice == "yellow" or choice == "blue" or choice == "green":
       print("Color has been changed")
       return choice
    else:
        print(choice)
        color_queue()
        

def game_loop():
    print("Current faced up card is "+logic.pile_top["name"]+"\n")
    # get's list for playable cards
    playable_hand = []
    for card in queue.get_current_unit().hand:
        playable_card = logic.playableChecker(card,logic.pile_top,logic.wild_color)
        if playable_card != None:
            playable_hand.append(card)
    # Player actions
    if queue.get_current_unit().is_player == True:
        # Displays player's card names
        hand_names =[]
        for card in queue.get_current_unit().hand:
            hand_names.append(card["name"])
        # Display play's hand
        print("Your cards")
        print(hand_names)
        # Ask for input
        time.sleep(1.5)
        choice = str(input("Please choose a card or type 'draw' to draw a new card or type 'uno' to call uno on someone: ")).lower()
 
        for card in playable_hand:
            if card["name"] == choice:
                queue.get_current_unit().remove_card(card)
                logic.pile_top = card
                print("\n"+card["name"]+" was played\n")
                print(queue.get_current_unit().name+" has "+str(len(queue.get_current_unit().hand))+" cards left")

    # check to see if need to ask for a color
                if card["sign"] == "wild" or card["sign"] == "draw4": 
                    Specials(card,color_queue())
                else:
                    Specials(card)
                    queue.move_unit_back()
                break
    #Draw's a card        
        if choice == "draw" or choice == "d":
            print("A card was drawn")
            queue.get_current_unit().draw_card()
        elif choice == "uno":
            logic.uno_called(queue)
    # invalid input was given
        elif choice not in hand_names:
            print("\nThat cannot be played!\n")
          
    # action for AI turn
    elif  queue.get_current_unit().is_player == False :
        if len(playable_hand) > 0:
            time.sleep(1.5)
            # randon card picker
            ran_card = random.randint(0,len(playable_hand)-1) 
            # removes the card being played 
            queue.get_current_unit().remove_card(playable_hand[ran_card])
            print(queue.get_current_unit().name+" played "+playable_hand[ran_card]["name"])
            # sets playing card as new pile card
            logic.pile_top = playable_hand[ran_card]
            Specials(playable_hand[ran_card],logic.wildCard())
            if random.randint(0,10) > 5:
                logic.uno_called(queue)
            print(queue.get_current_unit().name+" has "+str(len(queue.get_current_unit().hand))+" cards left")
            queue.move_unit_back()

        else:
            time.sleep(1.5)
            queue.get_current_unit().draw_card()
            print(queue.get_current_unit().name+" drawn a card.")
   
    else:
        return print("Somthing went wrong...")
    
    
    # If any player has 0 cards then end the loop else keep looping
    for unit in queue.units:
        if len(unit.hand) == 0:
            print(unit.name+" has won!")
            break
        elif len(unit.hand) > 0:
            game_loop()
            break

start_game()
game_loop()