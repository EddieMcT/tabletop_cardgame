
import random
import json
import numpy as np
import pygame
import os
from globals import GlobalVariables

pygame.init()

# Screen dimensions
screen_width = 1800
screen_height = 1000#1200
global_vars = GlobalVariables()
#Define and create the screen and other global variables
global_vars.screen_width = screen_width
global_vars.screen_height = screen_height
global_vars.scene = []
global_vars.screen = pygame.display.set_mode((global_vars.screen_width, global_vars.screen_height))
global_vars.decklist = []#placeholder lists
global_vars.gm_deck = []
global_vars.battle_deck = []


from maputil import generate_minimap, Minimap #Function that generates three lists: nodes (descriptions of events at each location), map (similar to nodes, with a 1 if a node is present and 0 if absent), and connections (a list of arrays describing a sufficient and non-intersecting set of connections from each layer to the next), and the Minimap class that uses this
from gameutil import card, deck_icon #class that handles loading and scaling card art, and tracks ownership, position, tapping, moving, etc., once a card is added to the board
from gameutil import GameState #state machine class
from gameutil import create_dialog_surface, display_search_results, search_deck, draw_card #general dialogue box function to use for styling and misc functions for gameplay
from gameutil import shuffle_deck
from cardutil import select_cards, shortened_card_data, match, sample_deck #Select cards takes in dictionaries of requirements and outputs a list of cards that meet those from an input list. shortened_card_data is a json file with the cards to use in the game overall. match returns a bool indicating if a card matches a list
from aiutil import select_lands
from displayvars import titlefont
shuffle_deck(global_vars.decklist) #Persistent list of the cards in the player's deck. This will be updated over the course of a game, and used each battle to create a (volatile) battle list
shuffle_deck(global_vars.gm_deck) #Initial value of the gm deck, however this does not need to be stored persistently as it changes for each battle
global_vars.minimap = Minimap(5,15, world_name = "Place", special_steps = {0:5, 14:1})
global_vars.minimap_pos = -1
global_vars.search_results = None
global_vars.target_deck = None

#Sample code to create a random list
params = {"color":["R"], "set":["m10"], "cmc":[1,2,3,4,5]}
exclusive = {"color": False, "set": True}
blankparams = {"color": True, "subtypes": False}
negparams = {"card_type": ["Land", "Token", "Emblem"]}


global_vars.gm_deck=select_cards(shortened_card_data, 5, params, exclusive=exclusive,
                              negparams=negparams, blankparams=blankparams)


global_vars.decklist = []#sample_deck#placeholder list, now replaced by start nodes
global_vars.battle_deck = []

def start_new_battle(gm_list = global_vars.gm_deck):
    if gm_list is not None:
        global_vars.gm_deck = gm_list #This exists so that other lists might be passed in when the GM uses some other list for that battle.
        shuffle_deck(global_vars.gm_deck)
    global_vars.battle_deck = list(global_vars.decklist)  # Make a copy of the deck for the battle
    shuffle_deck(global_vars.battle_deck)
    if global_vars.landlist is not None:
        shuffle_deck(global_vars.landlist)
    if global_vars.gm_land is not None:
        shuffle_deck(global_vars.gm_land)

class InputBox:
    def __init__(self, x, y, w, h, prompt='', text='', max_length=None, valid_chars=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color(200, 200, 200)
        self.prompt = prompt
        self.text = text
        self.max_length = max_length
        self.valid_chars = valid_chars
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.prompt + self.text, True, self.color)
        self.done = False

        
    def handle_event(self, event=None):
        if event is None:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                new_char = event.unicode
                if self.valid_chars and new_char in self.valid_chars:
                    if self.max_length and len(self.text) < self.max_length:
                        self.text += new_char
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_char = str(event.button)
            if self.valid_chars and new_char in self.valid_chars:
                if self.max_length and len(self.text) < self.max_length:
                    self.text += new_char
            
            self.txt_surface = self.font.render(self.prompt + self.text, True, self.color)
        if len(self.text) == self.max_length:
            self.done = True
    def draw(self, screen):
        lines = self.prompt + self.text
        lines = [line for line in lines.split('\n')]  # split the text into lines
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, self.color)
            screen.blit(line_surface, (self.rect.x + 5, self.rect.y + 5 + i*self.font.get_height()))  # adjust y position based on line number
        pygame.draw.rect(screen, self.color, self.rect, 2)

game_state = GameState()

def construct_deck(i=15, node_details={}, card_list = shortened_card_data,boss=False, planar_reqs = None):
    if "fightparams" in node_details:
        params = node_details["fightparams"].copy()
    else:
        params = {}
    if "exclusive" in node_details:
        exclusive = node_details["exclusive"]
    else:
        exclusive = {}
    if "blankparams" in node_details:
        blankparams = node_details["blankparams"]
    else:
        blankparams = None
    if "negparams" in node_details:
        negparams = node_details["negparams"]
    else:
        negparams =  {}
    if not "rarity" in negparams:
        negparams["rarity"] = []
    if i < 5:
        params["cmc"] = [c for c in range(i*2)]
        negparams["rarity"].append("mythic")
    if i < 3:
        negparams["rarity"].append("rare")
    if i < 2:
        negparams["rarity"].append("uncommon")
    if planar_reqs is not None:
        params.update({"set" : planar_reqs})
    return(select_cards(card_list, i, params, exclusive=exclusive,negparams=negparams, blankparams=blankparams))

def update_minimap(event_queue = []):
    global global_vars

    if global_vars.minimap == None: #To be replaced with receiving input from the hub world
        global_vars.minimap = Minimap(5,10,world_name = "Place")
    while event_queue:
        event = event_queue.pop(0)
        if global_vars.dialog == None: #No dialogue box, handle input normally
            if event.type == pygame.KEYDOWN:#GM or debug input
                if event.key == pygame.K_b:
                    global_vars.scene = []
                    game_state.change_state("battle")
                    start_new_battle()

                if event.key == pygame.K_q:
                    global_vars.minimap_pos +=1
            if event.type == pygame.MOUSEBUTTONDOWN:#Player input
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #if text box isn't None, handle events there
                i, j, node_details = global_vars.minimap.handle_click(mouse_x, mouse_y, global_vars.minimap_pos)
                if event.button == 1 and i == (1+global_vars.minimap_pos):  # Left-click
                    print(node_details)#Move to selected node if possible
                    if not node_details is None: #TO DO check if the node is available to move to (ie has a connection to the current position
                        #create appropriate dialogue box, handle events there eventually resulting in below, possibly via some storyline stuff
                        global_vars.node_details = node_details['data']
                        global_vars.scene = []
                        global_vars.dialog == None
                        global_vars.minimap_pos = i
                        global_vars.minimap_lane = j
                        start_new_battle(global_vars.gm_deck)#Refresh and shuffle decks in case they're used in dialogue
                        game_state.change_state("event")
                    #This needs to , move the player to the selected node, show a pane with details, and include buttons for "test" (which will be handled later) or "battle, which constructs a GM deck based on that node's parameters and starts a battle
                elif event.button == 3:  # Right-click
                    #Create appropriate dialogue box describing what is known about location
                    print(node_details)  # Inspect selected node and show its description, needs to change to something with input box that exits to the same map screen
                elif event.button == 2:  # Middle-click, currently a debug tool, to be replaced with other functionality?
                    print(global_vars.decklist)
                    print(global_vars.battle_deck)
                    start_new_battle(global_vars.gm_deck)
            if event.type == pygame.MOUSEBUTTONUP:
                pass#No use planned yet
            if event.type == pygame.MOUSEMOTION:
                pass#No use planned yet
        else:#Handle input in minimap dialog
            dialog_input = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                dialog_input = event.button #1 = leftclick, 2 is middle, 3 is right
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:#yes, or go
                    dialog_input = 1
                if event.key == pygame.K_n:#no
                    dialog_input = 3
                if event.key == pygame.K_m:#maybe, or third option
                    dialog_input = 2
            if dialog_input == 3:#Leave the event description
                global_vars.dialog = None
            elif dialog_input == 1:#Go to the selected event
                print("Need to work on going to the selected event")
                

def draw_minimap():
    global_vars.minimap.draw(global_vars.screen, global_vars.minimap_pos, global_vars.minimap_lane)

def check_params():
    if "fightparams" in global_vars.node_details: #Note that planar requirements shouldn't normally be present at this stage
        params = global_vars.node_details["fightparams"]
    else:
        params = {}
    if "exclusive" in global_vars.node_details:
        exclusive = global_vars.node_details["exclusive"]
    else:
        exclusive = {}
    if "blankparams" in global_vars.node_details:
        blankparams = global_vars.node_details["blankparams"]
    else:
        blankparams = None
    if "negparams" in global_vars.node_details:
        negparams = global_vars.node_details["negparams"]
    else:
        negparams =  {}

    if "enemy_params" in global_vars.node_details:
        enemy_params = global_vars.node_details["enemy_params"]
        enemy_blanks = {k: True for k in enemy_params.keys()} #For the set of things we care about checking, don't allow blanks
    else:
        enemy_params = None
        enemy_blanks = None
    return(params, exclusive, blankparams, negparams, enemy_params, enemy_blanks)
def check_reqs(matchreq = True, enemyreq = True, reqs = []):
    available = True
    for req in reqs:#Go through requirements seeing if there's anything not met. If everything is met, the option is allowed
        if req == "match" and not matchreq: #Check if the matching requirement prohibits this option (ie is relevant and isn't met)
            available = False
        elif req == "enemy" and not enemyreq: #Check if enemy requirements prohibit option
            available = False
        elif len(req) >= 5 and req[:4] == "cost":
            if global_vars.currency < int(req[4:]):
                available = False
        elif len(req) >= 5 and req[:4] == "gift":
            if gift < int(req[4:]):
                available = False
        elif False: #Add other types of checks here, eg references to other storylines
            available = False
        elif "_" in req:#Finally, check for story based requirements that reference other storylines, eg you can't befriend the elves unless you attack the goblins
            #Story requirements are entered as storykey_c_n where n is the required story progression and c indicates the type of comparison to perform. 0 means that you need to have started the story and not made enemies (negative values are always used for hostilities)
            req_val = req.split('_')
            req = req_val[0]
            if req in  global_vars.storylines:#Check if the relevant storyline has been started
                val =  global_vars.storylines[req]
            else:#If the story hasn't been started, treat it as a 0 as that means the player's able to encounter it in a neutral state but hasn't changed anything about it (needed eg for boss checks)
                global_vars.storylines[req] = 0
                val = 0
            if req_val[1] == "g" and val < int(req_val[2]):#Check if the story fails the test of being greater than/equal (ie if it's less, it fails)
                available = False
            elif req_val[1] == "l" and val > int(req_val[2]):#Check if the story fails the test of being less than/equal (ie if it's more, it fails)
                available = False
            elif req_val[1] == "e" and val != int(req_val[2]):#Check if the story fails the test of being equal (ie if it's different, it fails)
                available = False
    return (available)

def check_matches():
    matchreq = False
    enemyreq = True
    params, exclusive, blankparams, negparams, enemy_params, enemy_blanks = check_params()

    for card in global_vars.scene:
        if match(card.card_data, params, exclusive, negparams=negparams, blankparams=blankparams):
            matchreq = True #Any matches mean the player meets this requirement
        if enemy_params is not None:
            if match(card.card_data, enemy_params, {}, negparams=None, blankparams=enemy_blanks):
                enemyreq = False #Check if any match this, if so the requirement isn't met
    return(matchreq, enemyreq)

def update_event(event_queue = []):
    global global_vars
    if 'storykey' in global_vars.node_details:
        key = global_vars.node_details['storykey']
        if key in global_vars.storylines:#If storyline is tracked, read its current progress
            story = global_vars.storylines[key]
        if key in global_vars.gifts:#If storyline is tracked, read its current progress
            gifts = global_vars.gifts[key]
        else:#If storyline isn't yet tracked, start it at 0
            global_vars.storylines[key] = 0
            global_vars.gifts[key] = 0
            gifts = 0
            story = 0
    else: #If storyline doesn't have progression, it's always 0
        story = 0
    stagedata = global_vars.node_details['stages'][story]
    if 'card_disp' in stagedata and stagedata['card_disp'] > 0:
        while len(global_vars.scene) < stagedata['card_disp'] and len(global_vars.battle_deck):#Draw and show the appropriate number of cards
            draw_card(global_vars.battle_deck, "main")
    if len(global_vars.scene) >0 and  global_vars.dialog == None: #Just once, reposition the cards (doesn't need to happen every time)
        for i in range(len(global_vars.scene)):
            global_vars.scene[i].x = global_vars.scene[i].artwork.get_width() // 4  + (i+1) * global_vars.screen_width // (len(global_vars.scene)+2) 
            global_vars.scene[i].y = global_vars.screen_height // 2
    if global_vars.dialog == None:
        if 'text' in stagedata:
            dialog = stagedata['text']
        else:
            dialog = ""
            
        #Evaluate options, if any, and then add them to dialogue separated by linebreaks
        if 'options' in stagedata:
            if "req_keys" in stagedata:
                matchreq, enemyreq = check_matches()
            else:
                matchreq = True
                enemyreq = True
            
            for n, option in enumerate(stagedata['options']):
                available = True
                
               
                if "req_keys" in stagedata and n < len(stagedata["req_keys"])  and len(stagedata["req_keys"][n]):
                    #If there are requirements, check what they are and if they're met
                    #Go through requirements seeing if there's anything not met. If it is met, the option is described
                    available = check_reqs(matchreq = matchreq, enemyreq = enemyreq, reqs = stagedata["req_keys"][n])
                if available:
                    dialog += "\n" + option #Currently this just determines whether or not the options show up, but doesn't change whether they can be accessed (allows GM override, but also allows cheating)
            
        global_vars.dialog = InputBox(
            x=global_vars.screen_width // 8,
            y=global_vars.screen_height // 4, 
            w = global_vars.screen_width*3 // 4,
            h = global_vars.screen_height // 4,
            prompt=dialog, text='', max_length=1, valid_chars='12345') #max length and allowed characters may need to be adjusted for expanded options
    
    while event_queue:
        event = event_queue.pop(0)
        global_vars.dialog.handle_event(event)
    if global_vars.dialog.done: #Handle the resolution of an event and prepare for the battle step
        if "bossreward" in stagedata:
            matchreq, enemyreq = check_matches() #Recheck these before clearing the scene, in case they're used for boss requirements
        global_vars.scene = []
        if ("plnswlker" in  global_vars.node_details) and  global_vars.node_details["plnswlker"]: #What's this second check for, is it actually used?
            planar_reqs= None
        else:
            planar_reqs = global_vars.minimap.sets
        try:
            choicenum = int(global_vars.dialog.text) - 1
        except:
            choicenum = 0
        choicenum = min(choicenum, len(stagedata["method"])-1)
        if "req_keys" in stagedata:
            for req in stagedata["req_keys"][choicenum]: #Some requirements have consequences when they're chosen, such as reducing money or resetting a quest tracker
                if len(req) >= 5 and req[:4] == "gift":#Check if the gifts were used for the chosen story option and then reset to 0
                    global_vars.gifts[key] = 0 #Untested, should find the right thing?
                elif len(req) >= 5 and req[:4] == "cost":
                    print(global_vars.currency)
                    global_vars.currency += -int(req[4:]) #Not currently working???
                    print(global_vars.currency)
                    print(req)
        choice = stagedata["method"][choicenum]
        if "diff" in stagedata: #Diff means that the difficulty is specified, and will no longer depend on the position on the map
            numcards = int(stagedata["diff"][choicenum%max(len(stagedata["diff"]),1)])
        else:
            numcards = int(global_vars.minimap_pos+5)
        global_vars.gm_deck = construct_deck(numcards, global_vars.node_details, shortened_card_data, planar_reqs = planar_reqs) #Add planar requirements here (skip for planeswalkers)
        if len(choice) >= 2 and choice[:2] == "m_":
            global_vars.gm_deck = list(global_vars.decklist)
            choice = choice[2:]    
        if choice == "battle":
            global_vars.trade = False
            global_vars.landlist = select_lands(global_vars.decklist)
            global_vars.gm_land = select_lands(global_vars.gm_deck)
            
        elif choice == "puzzle":
            global_vars.trade = False
            global_vars.landlist = select_lands(global_vars.decklist)
            global_vars.gm_land = None
            global_vars.gm_deck = list(global_vars.gm_deck[:3]) #construct_deck(3, global_vars.node_details, shortened_card_data, planar_reqs = planar_reqs)
        elif choice == "trade" or choice == "summon":
            if choice == "summon":
                global_vars.gm_deck = construct_deck(numcards, global_vars.node_details, global_vars.banished, planar_reqs = None)
            global_vars.trade = True
            global_vars.landlist = None
            global_vars.gm_land = None
        elif choice == "reward" or choice == "aether" or choice == "rest":
            global_vars.trade = False
            global_vars.landlist = None
            global_vars.gm_land = None
            global_vars.gm_deck = None
            if choice == "aether":
                global_vars.currency += 5
            elif choice == "rest":
                global_vars.health = 20
        start_new_battle(global_vars.gm_deck)#Refresh and shuffle decks in case they're used in dialogue
        #Create a deck_icon item for each deck
        global_vars.scene.append(deck_icon(250, 0, global_vars.gm_deck, origin = 0))
        global_vars.scene.append(deck_icon(350, 0, global_vars.gm_land, origin = 1))
        global_vars.scene.append(deck_icon(250, global_vars.screen_height - 100,  global_vars.decklist,owner= "main", origin = 2))
        global_vars.scene.append(deck_icon(350, global_vars.screen_height - 100, global_vars.landlist, owner= "main", origin = 3))
        if choice == "battle": #Create counters and life totals
            global_vars.combat = True
            global_vars.scene.append(deck_icon(250, global_vars.screen_height//2 - 50,  None,owner= "main", origin = 2, countergen = True))#The counter generator of this battle
            for _ in range(2): #Number of players, currently always 2
                global_vars.scene[4].create_counter(2)
                global_vars.scene[-1].x = 250
                global_vars.scene[-1].y = 100
                global_vars.scene[-1].value = 5
                global_vars.scene[-1].origin = 3
                global_vars.scene[-1].refresh_artwork()
                global_vars.scene[-1].owner = "opponent"#Use these as system ones, ie undraggable, so they keep their spot at the start of the list
            global_vars.scene[6].value = int(global_vars.health) #Number 6 is the player's health, note that this should be global
            global_vars.scene[6].y = global_vars.screen_height - 300
            global_vars.scene[6].refresh_artwork()
        else:
            global_vars.combat = False
        if 'storykey' in global_vars.node_details:#If storyline is tracked, update its current progress
            if "new_stage" in stagedata:#new_stage can be left blank if the stage should stay the same
                global_vars.storylines[key] = int(stagedata["new_stage"][choicenum%max(len(stagedata["new_stage"]),1)])#Modulo so that a single newstage option is enough for all
        if "reward" in stagedata:
            for card in stagedata["reward"][choicenum%max(len(stagedata["reward"]),1)]:#Modulo so that rewards don't have to be repeated if it's the same in all cases
                draw_card(deck=None, player="opponent", card_data = card, origin=0) #Rewards aren't really drawn from the deck, but in case they're ever sent back that's their origin
        if "bossreward" in stagedata:
            for n, reward in enumerate(stagedata['bossreward'][choicenum%max(len(stagedata["bossreward"]),0)]):
                print(n)
                print(reward)
                if "bossreq" in stagedata:
                    #If there are requirements, check what they are and if they're met
                    reqs = stagedata["bossreq"][choicenum%max(len(stagedata["bossreward"]),0)][n%max(len(stagedata["bossreq"]),0)]
                    print(reqs)
                    available = check_reqs(matchreq = matchreq, enemyreq = enemyreq, reqs = reqs)#Go through requirements seeing if there's anything not met. If it is met, the option is described
                else:
                    available = True
                if available:
                    for card in reward:
                        draw_card(deck=None, player="opponent", card_data = card, origin=0)
        game_state.change_state("battle")#Every event type is resolved using a battle, even if it isn't a fight
def draw_event():
    global_vars.dialog.draw(global_vars.screen)
    for item in global_vars.scene: 
        item.draw()

def update_battle(event_queue = []):
    while event_queue:
        event = event_queue.pop(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # Main player draws
                draw_card(global_vars.battle_deck, "main")
            if event.key == pygame.K_g:  # Opponent (GM) draws
                draw_card(global_vars.gm_deck, "opponent")
            if event.key == pygame.K_l:  # Main player draws
                draw_card(global_vars.landlist, "main")
            if event.key == pygame.K_k:  # Opponent (GM) draws
                draw_card(global_vars.gm_land, "opponent")
            if event.key == pygame.K_e:
                print("Main player's turn ends")#Placeholder for possible turn handling
            if event.key == pygame.K_s:
                global_vars.search_results = None
                game_state.ministate = 0
                game_state.change_state("search")
            if event.key == pygame.K_h:
                shuffle_deck(global_vars.battle_deck)
            if event.key == pygame.K_m: #End the battle
                global_vars.scene = []
                game_state.change_state("minimap")
            if event.key == pygame.K_w: #End the battle with victory and appropriate rewards
                for item in global_vars.scene:
                    if item.tapped and item.origin == 0: #Card(s) won from opponent 
                        global_vars.decklist.append(item.card_data)
                    elif item.tapped and item.origin == 2 and global_vars.trade:
                        #Currently doing match check here, to be moved to card item to give value within trade?
                        if "fightparams" in global_vars.node_details or "negparams" in global_vars.node_details:
                            params, exclusive, blankparams, negparams, enemy_params, enemy_blanks = check_params()
                            if match(item.card_data, params, exclusive, negparams=negparams, blankparams=blankparams):
                                global_vars.currency += 1
                                if 'storykey' in global_vars.node_details:
                                    key = global_vars.node_details['storykey']
                                    global_vars.gifts[key] += 1
                        global_vars.banished.append(item.card_data)
                        global_vars.decklist.remove(item.card_data)
                if global_vars.combat:
                    global_vars.health = min( global_vars.scene[6].value, global_vars.health)
                        
                global_vars.scene = []
                game_state.change_state("minimap")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                for item in global_vars.scene:
                    item.handle_mouse_down(pygame.mouse.get_pos())
            elif event.button == 3:  # Right-click
                for item in global_vars.scene:
                    item.handle_right_click(pygame.mouse.get_pos(), trade = global_vars.trade)
            elif event.button == 2:  # Middle-click
                for item in global_vars.scene:
                    item.handle_middle_click(pygame.mouse.get_pos())
                
            elif event.button == 4:  # Scroll up
                for item in global_vars.scene:
                    item.handle_scroll_up(pygame.mouse.get_pos())
            elif event.button == 5:  # Scroll down
                for item in global_vars.scene:
                    item.handle_scroll_down(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            for item in global_vars.scene:
                item.handle_mouse_up(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEMOTION:
            for item in global_vars.scene:
                item.handle_mouse_motion(pygame.mouse.get_pos())
    # Update card positions, needs to be outside of event loop in order to stack cards
    dragging_cards = [card for card in global_vars.scene if card.dragging] #This refers to cards, but the same logic will be used for counters, tokens, etc.
    for i, dragged_card in enumerate(dragging_cards):
        dragged_card.dragging_index = i
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dragged_card.x = min(max(mouse_x - dragged_card.width // 2,5 - dragged_card.width),global_vars.screen_width -5) #Apply horizontal movement, keeping within 5 pixels of being hidden
        dragged_card.y = min(max(mouse_y - dragged_card.height // 2 + i * (max(50 - 3*len(dragging_cards),5)),5 - dragged_card.height),global_vars.screen_height -5)  # Apply vertical offset
        # Move the dragged card to the end of the scene list
        global_vars.scene.remove(dragged_card)
        global_vars.scene.append(dragged_card)
    if global_vars.trade:
        gmcards = [card for card in global_vars.scene if card.owner == "opponent"]
        #Display cards in the store appropriately
def draw_battle():
    for item in global_vars.scene: #Battle is handled using the list of objects in scene, each of which should have a draw function of its own
        item.draw()
    if global_vars.trade:
        titlefont.render_to(global_vars.screen, (200,200), str(global_vars.currency), fgcolor=(150,128,100), bgcolor=None)

        

def update_search(event_queue = []):
    global global_vars

    if not hasattr(global_vars, "player_gm_input"):
        global_vars.player_gm_input = InputBox(
            x=global_vars.screen_width // 4,
            y=global_vars.screen_height // 4,
            w=300,
            h=50,
            prompt="Enter 0 for Player or 1 for GM: ",
            max_length=1,
            valid_chars="01"
        )

    if not hasattr(global_vars, "num_cards_input"):
        global_vars.num_cards_input = InputBox(
            x=global_vars.screen_width // 4,
            y=global_vars.screen_height // 4 + 50,
            w=300,
            h=50,
            prompt="Enter the number of cards to reveal (0 for all): ",
            max_length=2,
            valid_chars="0123456789"
        )
    
    player_gm_text = None
    
    if global_vars.player_gm_input.done:
        global_vars.player_or_gm = int(global_vars.player_gm_input.text or 0)
    if global_vars.num_cards_input.done:
        global_vars.num_cards = int(global_vars.num_cards_input.text or 0)
    num_cards_text = None
    while event_queue:  # Process events until the queue is empty
        event = event_queue.pop(0)  # Get the first event in the queue
        
        if global_vars.player_gm_input.done and global_vars.num_cards_input.done:
            global_vars.search_done = True
            global_vars.target_deck = global_vars.battle_deck if global_vars.player_or_gm == 0 else global_vars.gm_deck
            global_vars.search_results = search_deck(global_vars.target_deck, "main" if global_vars.player_or_gm == 0 else "opponent", num_cards=global_vars.num_cards)
        elif global_vars.player_gm_input.done:
            global_vars.num_cards_input.handle_event(event)
        else:
            global_vars.player_gm_input.handle_event(event)

    if game_state.ministate: #Leave once search is complete, and reset search variables for next time
        global_vars.search_results = None
        global_vars.search_done = False
        global_vars.player_gm_input.done = False
        global_vars.num_cards_input.done = False
        game_state.change_state("battle")

def draw_search():
    a = False
    global_vars.screen.blit(game_state.previous_screen, (0, 0))
    dark = pygame.Surface((global_vars.screen.get_width(), global_vars.screen.get_height()), flags=pygame.SRCALPHA)
    dark.fill((50, 50, 50, 0))
    global_vars.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    if not global_vars.player_gm_input.done:
        global_vars.player_gm_input.draw(global_vars.screen)
    elif not global_vars.num_cards_input.done:
        global_vars.num_cards_input.draw(global_vars.screen)
    elif global_vars.search_results != None: #perform and display the search
        #Note that display_search_results is an exception to the usual flow for event handling, and does pause the rest of the game while it runs
        a = display_search_results(global_vars.search_results, global_vars.target_deck, "main" if global_vars.player_or_gm == 0 else "opponent", game_state.previous_screen)
        if a:
            game_state.ministate = 1 #if search is done
            global_vars.search_results = None
            global_vars.search_done = False
            global_vars.player_gm_input.done = False
            global_vars.num_cards_input.done = False
        else:
            game_state.ministate = 0

def update_search_input():
    pass

def draw_search_input():
    pass
game_state.add_state("minimap", update_minimap, draw_minimap)
game_state.add_state("event", update_event, draw_event)
game_state.add_state("battle", update_battle, draw_battle)
game_state.add_state("minimap", update_minimap, draw_minimap)
game_state.add_state("search", update_search, draw_search)
game_state.add_state("search_input", update_search_input, draw_search_input)

game_state.change_state("minimap")

pygame.display.set_caption("Inscryption-inspired Game")

# Main game loop
running = True
show_search_dialog = False
Clock = pygame.time.Clock()
Clock.tick()
while running:
    Clock.tick(60) #Limit the frame rate
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game_state.event_queue.append(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # Update game state
    
    game_state.update()
    
    # Draw game elements
    global_vars.screen.fill((0, 0, 0))  # Clear the screen (fill with black), is this redundant with game_state?
    game_state.draw()

    # Draw other elements here

    pygame.display.flip()  # Update the display
pygame.quit()
