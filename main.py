
import random
import json
import numpy as np
import pygame
import os
from globals import GlobalVariables

pygame.init()

# Screen dimensions
screen_width = 1800
screen_height = 900
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
from gameutil import card #class that handles loading and scaling card art, and tracks ownership, position, tapping, moving, etc., once a card is added to the board
from gameutil import GameState #state machine class
from gameutil import create_dialog_surface, display_search_results, search_deck, draw_card #general dialogue box function to use for styling and misc functions for gameplay
from gameutil import shuffle_deck
from cardutil import select_cards, shortened_card_data, match, sample_deck #Select cards takes in dictionaries of requirements and outputs a list of cards that meet those from an input list. shortened_card_data is a json file with the cards to use in the game overall. match returns a bool indicating if a card matches a list

shuffle_deck(global_vars.decklist) #Persistent list of the cards in the player's deck. This will be updated over the course of a game, and used each battle to create a (volatile) battle list
shuffle_deck(global_vars.gm_deck) #Initial value of the gm deck, however this does not need to be stored persistently as it changes for each battle
global_vars.minimap = Minimap(5,10, world_name = "Place")
global_vars.minimap_pos = 0
global_vars.search_results = None
global_vars.target_deck = None

#Sample code to create a random list
colors = ["W", "U", "B", "R", "G", []]  # Include an empty list for colorless cards
params = {"color":["R"], "set":["m10"], "cmc":[1,2,3,4,5]}
exclusive = {"name": True, "color": True, "set": True, "subtypes": True}
blankparams = {"color": True, "subtypes": False}
negparams = {"card_type": ["Land", "Token"]}

# Expected output: A deck containing an equal number of cards from each color and colorless cards, with no artifacts.
global_vars.gm_deck=select_cards(shortened_card_data, 5, params, exclusive=exclusive,
                              negparams=negparams, blankparams=blankparams)


global_vars.decklist = sample_deck#placeholder lists
global_vars.battle_deck = []

def start_new_battle(gm_list = global_vars.gm_deck):
    global_vars.gm_deck = gm_list #This exists so that other lists might be passed in when the GM uses some other list for that battle.
    global_vars.battle_deck = list(global_vars.decklist)  # Make a copy of the deck for the battle
    shuffle_deck(global_vars.gm_deck)
    shuffle_deck(global_vars.battle_deck)
    draw_card(global_vars.battle_deck, "main", )
    draw_card(global_vars.battle_deck, "main")
    draw_card(global_vars.gm_deck, "opponent")

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
            self.txt_surface = self.font.render(self.prompt + self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

game_state = GameState()

def construct_deck(i, node_details, card_list = shortened_card_data,boss=False):
    if "fightparams" in node_details:
        params = node_details["fightparams"]
    else:
        params = {}
    if "exclusive" in node_details:
        exclusive = node_details["exclusive"]
    else:
        exclusive = None
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
    return(select_cards(shortened_card_data, i*2, params, exclusive=exclusive,negparams=negparams, blankparams=blankparams))

def update_minimap(event_queue = []):
    if global_vars.minimap == None:
        global_vars.minimap = Minimap(5,10,world_name = "Place")
    while event_queue:
        event = event_queue.pop(0)
        if event.type == pygame.KEYDOWN:#GM or debug input
            if event.key == pygame.K_b:
                global_vars.scene = []
                game_state.change_state("battle")
                start_new_battle()

            if event.key == pygame.K_q:
                global_vars.minimap_pos +=1
        if event.type == pygame.MOUSEBUTTONDOWN:#Player input
            mouse_x, mouse_y = pygame.mouse.get_pos()
            i, j, node_details = global_vars.minimap.handle_click(mouse_x, mouse_y, global_vars.minimap_pos)
            if event.button == 1:  # Left-click
                print(node_details)#Move to selected node if possible
                if True: #TO DO check if the node is available to move to (ie is exactly one step ahead, and has a connection to the current position
                    global_vars.gm_deck = construct_deck(i, node_details, shortened_card_data)
                    global_vars.scene = []
                    game_state.change_state("battle")
                    start_new_battle(global_vars.gm_deck)
                #This needs to , move the player to the selected node, show a pane with details, and include buttons for "test" (which will be handled later) or "battle, which constructs a GM deck based on that node's parameters and starts a battle
            elif event.button == 3:  # Right-click
                print(node_details)  # Inspect selected node and show its description, needs to change to something with input box that exits to the same map screen
            elif event.button == 2:  # Middle-click
                pass#No use planned yet
        if event.type == pygame.MOUSEBUTTONUP:
            pass#No use planned yet
        if event.type == pygame.MOUSEMOTION:
            pass#No use planned yet


def draw_minimap():
    global_vars.minimap.draw(global_vars.screen, global_vars.minimap_pos)

def update_event(event = None):
    pass

def draw_event():
    pass

def update_battle(event_queue = []):
    while event_queue:
        event = event_queue.pop(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # Main player draws
                draw_card(global_vars.battle_deck, "main")
            if event.key == pygame.K_g:  # Opponent (GM) draws
                draw_card(global_vars.gm_deck, "opponent")
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                for item in global_vars.scene:
                    item.handle_mouse_down(pygame.mouse.get_pos())
            elif event.button == 3:  # Right-click
                for item in global_vars.scene:
                    item.handle_right_click(pygame.mouse.get_pos())
            elif event.button == 2:  # Middle-click
                for item in global_vars.scene:
                    item.handle_middle_click(pygame.mouse.get_pos())
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
        dragged_card.x = mouse_x - dragged_card.width / 2
        dragged_card.y = mouse_y - dragged_card.height / 2 + i * (50 - 2*len(dragging_cards))  # Apply vertical offset
        # Move the dragged card to the end of the scene list
        global_vars.scene.remove(dragged_card)
        global_vars.scene.append(dragged_card)
    
def draw_battle():
    for item in global_vars.scene: #Battle is handled using the list of objects in scene, each of which should have a draw function of its own
        item.draw()

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
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game_state.event_queue.append(event)
    # Update game state
    
    game_state.update()
    
    # Draw game elements
    global_vars.screen.fill((0, 0, 0))  # Clear the screen (fill with black), is this redundant with game_state?
    game_state.draw()

    # Draw other elements here

    pygame.display.flip()  # Update the display

pygame.quit()
