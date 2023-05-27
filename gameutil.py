import random
import json
import numpy as np
import pygame
import os
from globals import GlobalVariables
from displayvars import titlefont
global_vars = GlobalVariables()

def draw_card(deck, player, card_data = None, origin = 0, scale = 0.5):
    if card_data is not None or len(deck) > 0:
        if card_data == None:
            card_data = deck.pop(0)
        setcode = card_data["set"][0]#These variables always exist as lists, but only one should be present for name and set
        name = card_data["name"][0]#Only name and set are needed to find artwork
        if player == "main":
            cardx = 10  # Lower left
            cardy = global_vars.screen_height - 100
        elif player == "opponent" or origin==0:
            cardx = 10  # Upper left
            cardy = -50
        else: #Placeholder for additional players later
            cardx = global_vars.screen_width - 100  # Lower right
            cardy = global_vars.screen_height - 100
        global_vars.scene.append(card(setcode, name, cardx, cardy, owner=player, card_data=card_data, origin= origin, scale = scale))
        
class card():#Object that is present and rendered in a scene
    def __init__(self, setcode, name, x, y,owner, card_data,scale=0.5, origin = 0):
        name = name.replace("/","-")#To handle dual cards
        image_path = os.path.join("C:\\", "Users", "eddie", "Documents", "D&D", "Codes", "images", f"{setcode} {name}.jpg")
        original_artwork = pygame.image.load(image_path)
        width, height = original_artwork.get_size()
        new_size = (int(width * scale), int(height * scale))
        self.artwork = pygame.transform.scale(original_artwork, new_size)
        self.original_artwork = original_artwork
        self.scale = scale
        self.x = x
        self.y = y
        self.width, self.height = new_size
        self.dragging = False
        self.tapped = False
        self.dragging_index = 0
        self.owner = owner  # "main" or "opponent"
        self.origin = origin #To replace the owner tag, the index of which deck object it's connected to, 0=opponent deck, 1=opponent land, 2=playerdeck, 3=playerland
        if False and owner == "main":
            self.origin=2 #To be removed once origin system fully implemented
        self.setcode = setcode
        self.name = name
        self.card_data=card_data
    
    def handle_mouse_down(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            self.dragging = True

    def handle_mouse_up(self, pos):
        self.dragging = False

    def handle_mouse_motion(self, pos):
        if False and self.dragging: #This is handled in the main loop instead so as to include offsets
            self.x = pos[0] - self.artwork.get_width() // 2
            self.y = pos[1] - self.artwork.get_height() // 2
    
    def handle_right_click(self, pos, trade = False):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            if trade:
                if self.origin == 2:#Player's deck
                    value = 1
                elif self.card_data['rarity'][0] == 'mythic':
                    value = 7
                elif self.card_data['rarity'][0] == 'rare':
                    value = 5
                elif self.card_data['rarity'][0] == 'uncommon':
                    value = 3
                else:
                    value = 1
                
                if self.origin == 0 and not self.tapped:
                    purchase = True
                elif self.origin == 2 and self.tapped:
                    purchase = True
                else:
                    purchase = False
                if purchase: #Try to pay for the new item
                    if global_vars.currency >= value:
                        global_vars.currency -= value
                        success = True
                    else:
                        success = False
                else:
                    global_vars.currency += value
                    success = True
            else: #Not trading, no need for money checks
                success = True
            if success:
                self.tapped = not self.tapped
                self.artwork = pygame.transform.rotate(self.artwork, -90 if self.tapped else 90)
                
                self.x = min(max(self.x - (self.artwork.get_width()- self.artwork.get_height()) // 2,5 - self.artwork.get_width()),global_vars.screen_width -5) #Keep the center constant, keeping within 5 pixels of being hidden
                self.y = min(max(self.y - (self.artwork.get_height()- self.artwork.get_width()) // 2,5 - self.artwork.get_height()),global_vars.screen_height -5) 
                
    def draw(self):
        global_vars.screen.blit(self.artwork, (self.x, self.y))
    
    def handle_middle_click(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            # Send the card back to the top of the appropriate library
            global_vars.scene[self.origin].deck.insert(0,(self.card_data))
            global_vars.scene.remove(self)  # Remove the card from the scene
    
    def handle_scroll_up(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            orig = list((self.artwork.get_width(), self.artwork.get_height()))
            self.scale -= 0.25
            self.scale = max(self.scale, 0.25)
            original_artwork = self.original_artwork 
            width, height = original_artwork.get_size()
            new_size = (int(width * self.scale), int(height * self.scale))
            self.width, self.height = new_size #For the sake of dragging
            self.artwork = pygame.transform.scale(original_artwork, new_size)
            self.artwork = pygame.transform.rotate(self.artwork, -90 if self.tapped else 0)
            orig[0] -= self.artwork.get_width()
            orig[1] -= self.artwork.get_height()
            self.x += orig[0]//2
            self.y += orig[1]//2
    def handle_scroll_down(self, pos):
        if self.x <= pos[0] <= self.x + self.artwork.get_width() and self.y <= pos[1] <= self.y + self.artwork.get_height():
            orig = list((self.artwork.get_width(), self.artwork.get_height()))
            self.scale += 0.25
            self.scale = min(self.scale, 2)
            original_artwork = self.original_artwork 
            width, height = original_artwork.get_size()
            new_size = (int(width * self.scale), int(height * self.scale))
            self.width, self.height = new_size #For the sake of dragging
            self.artwork = pygame.transform.scale(original_artwork, new_size)
            self.artwork = pygame.transform.rotate(self.artwork, -90 if self.tapped else 0)
            orig[0] -= self.artwork.get_width()
            orig[1] -= self.artwork.get_height()
            self.x += orig[0]//2
            self.y += orig[1]//2
def shuffle_deck(deck):#Just some error catching around the built in function, could be removed if I were more careful?
    if deck is not None:
        if len(deck):
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
                    global_vars.search_results = search_deck(global_vars.target_deck, "main" if global_vars.player_or_gm == 0 else "opponent", num_cards=global_vars.num_cards)#Needs fixing to be in line with new deck_icon object
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
    
class deck_icon():#Object that is present and rendered in a scene, representing a deck and can be interacted with
    def __init__(self, x, y,deck, owner="opponent",size = 100, origin=0, countergen = False):
        self.x = x
        self.y = y
        self.size = size
        self.owner=owner
        self.tapped = False
        self.countergen = countergen
        self.dragging = False #These can't be dragged, but are in the scene so will  be checked
        self.origin = origin #self referential, this should be the deck's own index in the scene, which cards will use to be transferred back to the right place later
        if deck is None:
            self.deck = []
            self.card_num = 0
        else:
            self.deck = list(deck) #Note that this needs to be a global variable, probably? 
            self.card_num = len(deck)
        #Otherwise this more or less replaces the global deck lists (also not a bad option, maybe do that deliberately with copy()?) Note that if this happens, the cards and many other functions will need to change which decklist things are sent to
    def create_counter(self, size):
        global_vars.scene.append(counter(250, 300, scale=size, owner=self.owner))
    def handle_mouse_down(self, pos): #Draw a card
        if self.x <= pos[0] <= self.x + self.size and self.y <= pos[1] <= self.y + self.size:
            if self.countergen:
                self.create_counter(0.5) #Create a counter
            else:
                if len(self.deck):
                    draw_card(self.deck, self.owner, origin = self.origin, scale = 0.25)
                    print(self.origin)
                    print(len(self.deck))
                    self.card_num -=1

    def handle_mouse_up(self, pos):
        pass

    def handle_mouse_motion(self, pos):
        pass
    
    def handle_right_click(self, pos, *args, **kwargs): #shuffle
        if self.x <= pos[0] <= self.x + self.size and self.y <= pos[1] <= self.y + self.size:
            if self.countergen:
                self.create_counter(1) #Create a counter
            else:
                shuffle_deck(self.deck)
    def draw(self):
        pygame.draw.rect(global_vars.screen, (18, 15, 15), pygame.Rect(self.x, self.y, self.size, self.size))
        pygame.draw.rect(global_vars.screen, (180, 180, 150), pygame.Rect(self.x, self.y, self.size, self.size), 5)
        titlefont.render_to(global_vars.screen, (self.x + self.size//10 , self.y+ self.size//10), str(self.card_num), fgcolor=(180,150,100), bgcolor=(18, 15, 15))
    
    def handle_middle_click(self, pos):
        if self.x <= pos[0] <= self.x + self.size and self.y <= pos[1] <= self.y + self.size:
            if self.countergen:
                self.create_counter(2) #Create a counter
            else:
                self.card_num = len(self.deck) #recalculate in case it's wrong, since they could get out of sync
    
    def handle_scroll_up(self, pos):
        pass #placeholder function for scrolling
    def handle_scroll_down(self, pos):
        pass #placeholder function for scrolling
    
class counter():#Object that is present and rendered in a scene, currently made as a variant of cards, could be made into a type of card?
    def __init__(self, x, y,owner = "opponent", scale=0.5, origin = 0):
        self.scale = scale
        self.x = x
        self.y = y
        self.width = self.height = 100*self.scale #Currently don't need both, but could make different shapes later
        self.dragging = False
        self.tapped = False
        self.dragging_index = 0
        self.owner = owner  # Unnecessary, reused to track dragability (ie system owned counters aren't moveable, and so won't be adjusted in the scene ordering)
        self.mode = 0 #Type of counter
        self.origin = origin #Probably not needed in normal sense, so it's being used to track the desired colour
        self.colours = [(250,250,230),#White
                        (20,50,250),#Blue
                        (0,0,0),#Black
                        (200,30,20),#Red
                        (10,200,30),#Green
                        (80,0,150),#Violet
                        (120,120,120),#Grey
                       ]
        self.value = 0
        self.refresh_artwork()
    
    def refresh_artwork(self):
        text_surface = pygame.Surface((100, 100))
        bg = self.colours[self.origin]
        text_surface.fill(bg)
        if self.mode == 0:
            text = self.value #Just a number
        elif self.mode == 1:
            text = f"+{self.value}/+{self.value}" #+1 counters
        elif self.mode == 2:
            text = f"{self.value}/{self.value}" #For tokens
        elif self.mode == 2:
            text = f"-{self.value}/-{self.value}" #-1 counters
        text_size = titlefont.get_rect(str(self.value)).size# Calculate the position to center the text in the surface
        text_x = 50 - text_size[0] // 2
        text_y = 50 - text_size[1] // 2
        titlefont.render_to(text_surface, (text_x, text_y), str(self.value), fgcolor=(50,40,15), bgcolor=bg)
        self.text_surface = pygame.transform.scale(text_surface, (int(self.scale*100), int(self.scale*100)))
    
    def handle_mouse_down(self, pos):#Only allow dragging for non-system counters, eg those created during the battle and not tracking important data
        if self.owner == "main" and self.x <= pos[0] <= self.x + 100*self.scale and self.y <= pos[1] <= self.y + 100*self.scale:
            self.dragging = True

    def handle_mouse_up(self, pos):
        self.dragging = False

    def handle_mouse_motion(self, pos):
        if self.dragging:
            self.x = pos[0] - self.width // 2
            self.y = pos[1] - self.height // 2
    
    def handle_right_click(self, pos, trade = False):
        if self.x <= pos[0] <= self.x + 100*self.scale and self.y <= pos[1] <= self.y + 100*self.scale:
            self.refresh_artwork()#Currently no real use for this
    def draw(self):
        global_vars.screen.blit(self.text_surface, (self.x, self.y))
    
    def handle_middle_click(self, pos):
        if self.x <= pos[0] <= self.x + 100*self.scale and self.y <= pos[1] <= self.y + 100*self.scale:
            self.origin = (self.origin+1)%len(self.colours) #misusing the origin here to track the colour
            self.refresh_artwork()
    
    def handle_scroll_up(self, pos):
        if self.x <= pos[0] <= self.x + 100*self.scale and self.y <= pos[1] <= self.y + 100*self.scale:
            self.value += 1
            self.refresh_artwork()
    def handle_scroll_down(self, pos):
        if self.x <= pos[0] <= self.x + 100*self.scale and self.y <= pos[1] <= self.y + 100*self.scale:
            self.value -= 1
            self.refresh_artwork()