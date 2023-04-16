import random
import json
import numpy as np
import pygame
import os
from globals import GlobalVariables

global_vars = GlobalVariables()

def draw_card(deck, player, card_data = None):
    if len(deck) > 0:
        if card_data == None:
            card_data = deck.pop(0)
        setcode = card_data["set"][0]#These variables always exist as lists, but only one should be present for name and set
        name = card_data["name"][0]#Only name and set are needed to find artwork
        if player == "main":
            cardx = 10  # Lower left
            cardy = global_vars.screen_height - 100
        elif player == "opponent":
            cardx = 10  # Upper left
            cardy = 10
        global_vars.scene.append(card(setcode, name, cardx, cardy, owner=player, card_data=card_data))
        
class card():#Object that is present and rendered in a scene
    def __init__(self, setcode, name, x, y,owner, card_data,scale=0.5):
        image_path = os.path.join("C:\\", "Users", "eddie", "Documents", "D&D", "Codes", "images", f"{setcode} {name}.jpg")
        original_artwork = pygame.image.load(image_path)
        width, height = original_artwork.get_size()
        new_size = (int(width * scale), int(height * scale))
        self.artwork = pygame.transform.scale(original_artwork, new_size)
        self.x = x
        self.y = y
        self.width, self.height = new_size
        self.dragging = False
        self.tapped = False
        self.dragging_index = 0
        self.owner = owner  # "main" or "opponent"
        self.setcode = setcode
        self.name = name
        self.card_data=card_data
    
    def handle_mouse_down(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            self.dragging = True

    def handle_mouse_up(self, pos):
        self.dragging = False

    def handle_mouse_motion(self, pos):
        if self.dragging:
            self.x = pos[0] - self.artwork.get_width() // 2
            self.y = pos[1] - self.artwork.get_height() // 2
    
    def handle_right_click(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            self.tapped = not self.tapped
            self.artwork = pygame.transform.rotate(self.artwork, -90 if self.tapped else 90)
    def draw(self):
        global_vars.screen.blit(self.artwork, (self.x, self.y))
    
    def handle_middle_click(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            # Send the card back to the top of the appropriate library
            if self.owner == "main":
                global_vars.battle_deck.insert(0,(self.card_data))
            elif self.owner == "opponent":
                global_vars.gm_deck.insert(0,(self.card_data))
            global_vars.scene.remove(self)  # Remove the card from the scene

def shuffle_deck(deck):
    random.shuffle(deck)
    
class GameState:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.event_queue = [] 
        self.ministate1 = 0 #Variable for tracking minor updates to states, has different meaning in different contexts

    def add_state(self, name, update_fn, draw_fn):
        self.states[name] = {"update": update_fn, "draw": draw_fn}

    def change_state(self, name):
        if self.current_state != name:
            self.previous_screen = global_vars.screen.copy()
        self.current_state = name
        self.states[self.current_state]["update"](event_queue = [])#States frequently need to run at least once before they will render properly (eg creating variables that the draw function needs)
    def update(self):
        if self.current_state:
            self.states[self.current_state]["update"](event_queue = self.event_queue)

    def draw(self):
        if self.current_state:
            self.states[self.current_state]["draw"]()
def create_dialog_surface(width, height, alpha=0.4):
    dialog_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    dialog_surface.fill((128,100,80, 50))
    return dialog_surface
def display_search_results(search_results, deck, player, previous_screen):
    dialog_width = global_vars.screen_width // 2
    dialog_height = global_vars.screen_height // 2
    result_list_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
    dialog_surface = create_dialog_surface(dialog_width, dialog_height)
    
    font = pygame.font.Font(None, 36)
    gap = 50

    selected_actions = {idx: "None" for idx in range(len(search_results))}
    current_idx = 0
    selection_done = False

    def redraw_result_list_surface():
        result_list_surface.fill((0, 0, 0,0))
        result_list_surface.set_colorkey((0, 0, 0))
        for idx, card in enumerate(search_results):
            text_color = (255, 255, 100) if idx == current_idx else (200, 175, 175)
            text_surface = font.render(f"{card[1]} ({card[0]}) - {selected_actions[idx]}", True, text_color)
            result_list_surface.blit(text_surface, (10, 10 + idx * gap))

    while not selection_done:
        global_vars.screen.blit(previous_screen, (0,0))
        dark = pygame.Surface((global_vars.screen.get_width(), global_vars.screen.get_height()), flags=pygame.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        global_vars.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        redraw_result_list_surface()
        dialog_surface.blit(result_list_surface, (0, 0))
        
        global_vars.screen.blit(dialog_surface, (global_vars.screen_width // 4, global_vars.screen_height // 4), special_flags=pygame.BLEND_RGBA_MAX)
        pygame.display.flip()
        dialog_surface = create_dialog_surface(dialog_width, dialog_height)  # Clear the dialog_surface for the next frame


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #Add in option to use num + to increase search size
                if event.key == pygame.K_UP:
                    current_idx = max(0, current_idx - 1)
                elif event.key == pygame.K_DOWN:
                    current_idx = min(len(search_results) - 1, current_idx + 1)
                elif event.key == pygame.K_KP1:
                    selected_actions[current_idx] = "draw"
                elif event.key == pygame.K_KP2:
                    selected_actions[current_idx] = "send_to_top"
                elif event.key == pygame.K_KP3:
                    selected_actions[current_idx] = "send_to_bottom"
                elif event.key == pygame.K_KP_PLUS: #Increase number of cards revealed
                    global_vars.num_cards += 1
                    global_vars.search_results = search_deck(global_vars.target_deck, "main" if global_vars.player_or_gm == 0 else "opponent", num_cards=global_vars.num_cards)
                    search_results = global_vars.search_results
                elif event.key == pygame.K_KP_ENTER:
                    # Confirm selections and exit
                    selection_done = True
                elif event.key == pygame.K_ESCAPE:
                    # Cancel card selection and close the search results
                    selected_actions = {idx: "None" for idx in range(len(search_results))}
                    selection_done = True
    to_remove = []
    to_add = []
    for idx, action in selected_actions.items():
        if action != "None":
            card = search_results[idx]
            if action == "draw":
                draw_card(deck, player, setcode=card[0], name=card[1])
                to_remove.append(card)
            elif action == "send_to_top":
                to_remove.append(card)
                to_add.append(card)
            elif action == "send_to_bottom":
                to_remove.append(card)
                deck.append(card)
    
    for card in to_remove:
        deck.remove(card)
    
    for card in to_add:
        deck.insert(0, card)
    return(selection_done)
def search_deck(deck, player, num_cards=0, search_term=None):
    if search_term:
        search_results = [card for card in deck if search_term.lower() in card[1].lower() or search_term.lower() in card[0].lower()]
    elif num_cards > 0:
        search_results = deck[:num_cards]
    else:
        search_results = deck
    return(search_results)
    
