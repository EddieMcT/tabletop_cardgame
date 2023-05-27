import random
import json
import numpy as np
import pygame
import os

from globals import GlobalVariables

#global_vars = GlobalVariables()
#screen = global_vars.screen
#screen_width = global_vars.screen_width
#screen_height = global_vars.screen_height
#scene = global_vars.scene
#decklist = global_vars.decklist
#gm_deck = global_vars.gm_deck
#battle_deck = global_vars.battle_deck

    
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

            if len(card_e[param]): #Blanks checked separately, therefore only check for overlap with values 
                if exclusive_param:
                    if not set(card_e[param]).issubset(set(values)):
                        return False
                elif len(values): #Non-exclusive empty lists should permit everything
                    if not set(card_e[param]).intersection(set(values)):
                        return False

    return True



def select_cards(cards, n, params, exclusive=True, negparams=None, blankparams=None): #This, and the match function, and bottlenecks at gamesetup and should be improved
    matching_cards = [card_e for card_e in cards if match(card_e, params, exclusive, negparams, blankparams)]
    if len(matching_cards):# < n:
        return random.choices(matching_cards, k=n) #choose with replacement, should this always be used instead of sample?
    else:
        return([])
    #    return random.sample(matching_cards, n)

def select_lands(n = 20, card_list = None, sets = None):
    ratios = {"W":0, "U":0, "B":0,"R":0,"G":0,"N":0}
    minimums = {"W":0, "U":0, "B":0,"R":0,"G":0,"N":0}
    for card in card_list:
        card_ratios = {"W":0, "U":0, "B":0,"R":0,"G":0,"N":0}
        for c in card["color"]:
            ratios[c] += 1
            card_ratios[c] += 1
        for c, v in card_ratios.items():
            if v > minimums[c]:
                ratios[c] = v
    total_c = 0
    
    for c, v in ratios.items():
        total_c += v #calculate inital total of colours
        
    for c, v in ratios.items(): #reweight so that there's a more even spread of lands
        if v > 0:
            if v > total_v*0.9:
                ratios[c] = 3
            elif v > total_v*0.5:
                ratios[c] = 2
            else:
                ratios[c] = 1
    total_c = 0
    for c, v in ratios.items():
        total_c += v #recalculate totals in weighted lists
    if total_c == 0:
        ratios = {"W":1, "U":3, "B":1,"R":0,"G":0,"N":0} #Default arrangement for colorless decks
        total_c = 5
    for c, v in ratios.items():
        ratios[c] = max(int(v * n/total_c),minimums[c])#Currently just one step, weighted ratio will be used unless it's less than the minimum amount needed
    land_list = []
    for c, v in ratios.items():
        parameters = {"set": [], 'card_type': ['Basic'],'color': [c]}
        exclusive={"set": False, 'card_type': False,'color': True}
        blankparams={"set": True, 'card_type': True,'color': True}
        if c == "N":
            parameters["color"] = []
            blankparams["color"] = False
        if sets is not None:
            parameters["set"] = sets
            exclusive["set"] = True
        land_list.append(i for i in select_cards(shortened_card_data, v, params = parameters, exclusive=exclusive, negparams=None, blankparams=blankparams))
    return(land_list)
        
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
  'watermark': [],
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
  'watermark': [],
  'oracle_text': ['Flying\nWhenever Umara Raptor or another Ally enters the battlefield under your control, you may put a +1/+1 counter on Umara Raptor.'],
  'legend': [False]},
 {'set': ['ala'],
  'rarity': ['common'],
  'color': ['G'],
  'mana_cost': ['1', 'G'],
  'mana_symbols': ['G'],
  'name': ['Cylian Elf'],
  'cmc': [2.0],
  'card_type': ['Creature'],
  'subtypes': ['Elf', 'Scout'],
  'keywords': [],
  'watermark': [],
  'oracle_text': [''],
  'legend': [False]},
 {'set': ['mor'],
  'rarity': ['common'],
  'color': ['B'],
  'mana_cost': ['B'],
  'mana_symbols': ['B'],
  'name': ['Prickly Boggart'],
  'cmc': [1.0],
  'card_type': ['Creature'],
  'subtypes': ['Goblin', 'Rogue'],
  'keywords': ['Fear'],
  'watermark': [],
  'oracle_text': ["Fear (This creature can't be blocked except by artifact creatures and/or black creatures.)"],
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
  'watermark': [],
  'oracle_text': [''],
  'legend': [False]}]