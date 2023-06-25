# globals.py

class GlobalVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.screen = None
            cls._instance.screen_width = None
            cls._instance.screen_height = None
            cls._instance.scene = None
            cls._instance.banished = []
            cls._instance.decklist = None
            cls._instance.gm_deck = None
            cls._instance.landlist = []
            cls._instance.gm_land = []
            cls._instance.battle_deck = None
            cls._instance.search_results = None
            cls._instance.target_deck = None
            cls._instance.player_or_gm = 0
            cls._instance.num_cards = 0
            cls._instance.health = 20
            cls._instance.minimap = None
            cls._instance.minimap_pos = -1 #Start back one, to allow beginning properly
            cls._instance.minimap_lane = 0
            cls._instance.dialog = None
            cls._instance.trade = False
            cls._instance.combat = False #Whether the current event is true combat
            cls._instance.currency = 0 #Wallet of the main character
            cls._instance.node_details = None
            cls._instance.planned_coords = [0,0]
            cls._instance.storylines = {'storyplace':0} #Something to be moved to a save file? Information about where the player is in each story
            cls._instance.gifts = {'storyplace':0} #Equivalent, but tracks whether the player has sold the right kind of card
        return cls._instance
