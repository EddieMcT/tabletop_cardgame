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
            cls._instance.decklist = None
            cls._instance.gm_deck = None
            cls._instance.battle_deck = None
            cls._instance.search_results = None
            cls._instance.target_deck = None
            cls._instance.player_or_gm = 0
            cls._instance.num_cards = 0
            cls._instance.minimap = None
            cls._instance.minimap_pos = 0
        return cls._instance
