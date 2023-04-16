import random
import json
import numpy as np
import pygame
import os

from globals import GlobalVariables

global_vars = GlobalVariables()
screen = global_vars.screen
screen_width = global_vars.screen_width
screen_height = global_vars.screen_height
scene = global_vars.scene
decklist = global_vars.decklist
gm_deck = global_vars.gm_deck
battle_deck = global_vars.battle_deck


    
def match(card_e, params, exclusive, negparams=None, blankparams=None):
    all_params = set(params.keys())
    if negparams:
        all_params = all_params.union(set(negparams.keys()))
    if blankparams:
        all_params = all_params.union(set(blankparams.keys()))
    for param in all_params:
        if param in card_e:
            values = params.get(param, [])
            if isinstance(exclusive, dict):
                if (param in exclusive) and (param in params):
                    exclusive_param = exclusive[param]
                else:
                    exclusive_param = False#Default to inclusive mode
            else:
                exclusive_param = exclusive

            if negparams and (param in negparams) and (negparams[param]):
                if set(card_e[param]).intersection(set(negparams[param])):
                    return False

            if blankparams and (param in blankparams):
                if blankparams[param]:
                    if len(card_e[param]) == 0:
                        return False

            if len(card_e[param]) and len(values): #Blanks checked separately, therefore only check for overlap with values 
                if exclusive_param:
                    if not set(card_e[param]).issubset(set(values)):
                        return False
                else:
                    if not set(card_e[param]).intersection(set(values)):
                        return False

    return True



def select_cards(cards, n, params, exclusive=True, negparams=None, blankparams=None):
    matching_cards = [card_e for card_e in cards if match(card_e, params, exclusive, negparams, blankparams)]
    if len(matching_cards) < n:
        return random.sample(matching_cards, len(matching_cards))
    else:
        return random.sample(matching_cards, n)

with open("shortened_card_data.json", "r") as file:
    shortened_card_data = json.load(file)
    
sample_deck = [{'set': ['con'],#Output of a previous select_cards query
  'rarity': ['mythic'],
  'color': ['W'],
  'mana_cost': ['5', 'W'],
  'mana_symbols': ['W'],
  'name': ['Mirror-Sigil Sergeant'],
  'cmc': [6.0],
  'card_type': ['Creature'],
  'subtypes': ['Rhino', 'Soldier'],
  'keywords': ['Trample'],
  'oracle_text': ["Trample\nAt the beginning of your upkeep, if you control a blue permanent, you may create a token that's a copy of Mirror-Sigil Sergeant."],
  'legend': [False]},
 {'set': ['zen'],
  'rarity': ['common'],
  'color': ['U'],
  'mana_cost': ['2', 'U'],
  'mana_symbols': ['U'],
  'name': ['Umara Raptor'],
  'cmc': [3.0],
  'card_type': ['Creature'],
  'subtypes': ['Bird', 'Ally'],
  'keywords': ['Flying'],
  'oracle_text': ['Flying\nWhenever Umara Raptor or another Ally enters the battlefield under your control, you may put a +1/+1 counter on Umara Raptor.'],
  'legend': [False]},
 {'set': ['m11'],
  'rarity': ['common'],
  'color': ['B'],
  'mana_cost': [],
  'mana_symbols': [],
  'name': ['Swamp'],
  'cmc': [0.0],
  'card_type': ['Basic', 'Land'],
  'subtypes': ['Swamp'],
  'keywords': [],
  'oracle_text': ['({T}: Add {B}.)'],
  'legend': [False]},
 {'set': ['shm'],
  'rarity': ['common'],
  'color': ['R'],
  'mana_cost': [],
  'mana_symbols': [],
  'name': ['Mountain'],
  'cmc': [0.0],
  'card_type': ['Basic', 'Land'],
  'subtypes': ['Mountain'],
  'keywords': [],
  'oracle_text': ['({T}: Add {R}.)'],
  'legend': [False]},
 {'set': ['roe'],
  'rarity': ['common'],
  'color': ['G'],
  'mana_cost': ['4', 'G'],
  'mana_symbols': ['G'],
  'name': ['Nema Siltlurker'],
  'cmc': [5.0],
  'card_type': ['Creature'],
  'subtypes': ['Lizard'],
  'keywords': [],
  'oracle_text': [''],
  'legend': [False]}]