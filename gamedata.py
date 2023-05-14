worlds = {#Information per world to use in building and navigating maps, including character and story information. Exact implementation tbd, but should be robust and accessible for many different arrangements of worlds
    "Place": {#Placeholder world
        # ...
        "events": {#Types of events in this world. Should be the same for all worlds, but doesn't have to be.
            "battle": {#Parameters to use when constructing GM decks for different locations
                    "W": {"fightparams" : {"Color": ["W"]}},
                    "U": {"fightparams" : {"Color": ["U"]}},
                    "B": {"fightparams" : {"Color": ["B"]}},
                    "R": {"fightparams" : {"Color": ["R"]}},
                    "G": {"fightparams" : {"Name":["Llanowar Elves"], "Color": ["G", "N"], "setcode": ["m10"]}},
                    # Additional GM deck configurations
            },
            "faction_event": {"faction1":{"name": "Faction 1",#Events that relate to that world's factions. Can turn into fights depending on outcome so should have deckbuilding parameters
                                          "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],
                                          "fightparams": {"Name":["Llanowar Elves", "Ornithopter", "Forest"], "Color": ["G", "N"], "setcode": ["m10"]},
                                          "negparams" : {"card_type":["Token","Basic"]}
                                         },
                            "faction2":{"name": "Faction 2",'storykey':'storyplace',
                                        "stages": [{'text':"Stage 1 description", #Text to display while figuring out resolution
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                                'legend': [False]},
                                                               {},
                                                               {},]},
                                                   {'text':"Stage 2 description", #Text to display while figuring out resolution
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                                'legend': [False]},
                                                               {},
                                                               {},]},
                                                   {'text':"Hostility description", #Final spot is reserved for when the group has been set to hostile
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,-1,-1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "battle","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                                'legend': [False]},
                                                               {},
                                                               {},]}],
                                        "fightparams" : {"set": [],
                                                       "rarity": ["common","uncommon","rare", "mythic rare"],
                                                       "color": ["W", "U", "B", "R", "G"],
                                                       "mana_cost": [],
                                                       "mana_symbols": [],
                                                       "name": [],
                                                       "cmc": [],
                                                       "card_type": [],
                                                       "subtypes": [],
                                                       "keywords": [],
                                                       "oracle_text": [],
                                                       "legend": []},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                        "exclusive_params" : {"set": False,
                                                            "rarity": False,
                                                            "color": True,
                                                            "mana_cost": False,
                                                            "mana_symbols": False,
                                                            "name": False,
                                                            "cmc": False,
                                                            "card_type": False,
                                                            "subtypes": False,
                                                            "keywords": False,
                                                            "oracle_text": False,
                                                            "legend": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                        "blankparams" : {"set": False,
                                                       "rarity": False,
                                                       "color": False,
                                                       "mana_cost": False,
                                                       "mana_symbols": False,
                                                       "name": False,
                                                       "cmc": False,
                                                       "card_type": False,
                                                       "subtypes": False,
                                                       "keywords": False,
                                                       "oracle_text": False,
                                                       "legend": False}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                        "negparams" : {"set": [],
                                                     "rarity": [],
                                                     "color": [],
                                                     "mana_cost": [],
                                                     "mana_symbols": [],
                                                     "name": [],
                                                     "cmc": [],
                                                     "card_type": ["Token","Basic"],
                                                     "subtypes": [],
                                                     "keywords": [],
                                                     "oracle_text": [],
                                                     "legend": []}, #Values that are specifically not allowed
                                       }
                            # Add more factions here
                             },
            "story_event": {"story1":{"name": "Story 1", #Main story events, usually resolved with a dialogue box and a choice of some kind, may give quests.
                                      "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],},
                            "story2":{"name": "Story 2",
                                      "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],}
                            # Add more stories here
                           },
            "world_event": {"evnt1":{"name": "event 1",#some kind of other world related event, possibly related to the main story
                                     "method": "battle",#Type of logic  to use to resolve event, eg a fight or a event
                                     "fightparams": {"Name":["Llanowar Elves", "Ornithopter", "Forest"], "Color": ["G", "N"], "setcode": ["m10"]}},
                            "evnt2":{"name": "event 2",
                                     "method": "story_event","stages": ["Stage 1 description"],}
                            # Add more story types here
                           }
        },
        "evnt_type":["battle","faction_event","faction_event","faction_event","story_event","world_event","planeswalker"],#Relative weighting of event type
        "lane_id":["W","U","B","R","G"],#Meaning of each lane in this world's minimap, usually based on colour. Will be used to key other features from this data
        "param":{"W":["detail"],"U":["detail"],"B":["detail"],"R":["detail"],"G":["detail"]}, #General form of how lane ids will give other details to be used for events
        "faction_event":{"W":["faction1", "faction2"],"U":["faction1", "faction2"],"B":["faction1", "faction2"],"R":["faction1", "faction2"],"G":["faction1", "faction2"]},
        "story_event":{"W":["story1"],"U":["story1"],"B":["story1"],"R":["story2"],"G":["story2"]}, 
        "planeswalker":{"W":["plane1"],"U":["plane1"],"B":["plane1"],"R":["plane1"],"G":["plane2"]},#Planeswalkers the player might encounter
        "world_event":{"W":["evnt1"],"U":["evnt1"],"B":["evnt1"],"R":["evnt2"],"G":["evnt2"]},
        "setcodes":["m10", "m11"] #sets to use in this plane, if they aren't specified for an event
        #Add more world details here, eg background art and bossfight details
        },
    "lrw": {#Lorwyn
        # ...
        "events": {#Types of events in this world. Should be the same for all worlds, but doesn't have to be.
            "battle": {
                "gm_deck": {#Parameters to use when constructing GM decks for different locations based only on color, these aren't often used in Lorwyn
                    "W": {"Color": ["W"]},
                    "U": {"Color": ["U"]},
                    "B": {"Color": ["B"]},
                    "R": {"Color": ["R"]},
                    "G": {"subtype":["Elf", "Treefolk", "Elemental"], "Color": ["G"], "setcode": ["lrw"]},
                    # Additional GM deck configurations
                },
            },
            "faction_event": {"chn":{"name": "Changelings",
                                          "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],
                                          "fightparams" : {"set": ["lrw", "mrn"],
                                                       "color": ["B", "G"],
                                                       "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                                                       "subtypes": ["Shapeshifter"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                        "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                        "blankparams" : {"subtypes": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                        "negparams" : {"card_type": ["Token","Basic"]}, #Values that are specifically not allowed
                                         },
                              "elv":{"name": "Elves",
                                          "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],
                                          "fightparams" : {"set": ["lrw", "mrn"],
                                                       "color": ["B", "G"],
                                                       "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                                                       "subtypes": ["Elf"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                        "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                        "blankparams" : {"subtypes": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                        "negparams" : {"card_type": ["Token","Basic"]}, #Values that are specifically not allowed
                                         }
                              # Add more factions here
                             },
            "story_event": {"story1":{"name": "Story 1", #Main story events, usually resolved with a dialogue box and a choice of some kind, may give quests.
                                      "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],},
                            "story2":{"name": "Story 2",
                                      "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],}
                            # Add more stories here
                           },
            "world_event": {"evnt1":{"name": "event 1",#some kind of other world related event, possibly related to the main story
                                     "method": "battle",#Type of logic  to use to resolve event, eg a fight or a event
                                     "fightparams": {"Name":["Llanowar Elves", "Ornithopter", "Forest"], "Color": ["G", "N"], "setcode": ["m10"]}},
                            "evnt2":{"name": "event 2",
                                     "method": "story_event",
                                     "stages": ["Stage 1 description"],}
                            # Add more story types here
                           }
            # add more node types here
        },
        "lane_id":["G","W","U","B","R"],#R needs to be an edge for the ring of mountains, and there's BR but no no RG pairs in this world, so the forests have to be in the middle of the circular plane
        "param":{"W":["detail"],"U":["detail"],"B":["detail"],"R":["detail"],"G":["detail"]}, #General form of how lane ids will give other details to be used for events
        "faction_event":{"W":["mer", "mer","gnt", "gnt","gnt",
                        "gnt","kth", "kth","kth", "kth",
                        "kth", "kth","kth", "kth","kth",
                        "kth","ele", "chn","trf", "trf",],
                   "U":["fae", "fae","fae", "fae","fae",
                        "fae","fae", "fae","mer", "mer",
                        "mer", "mer","mer", "mer","mer",
                        "mer","mer", "mer","ele", "chn",],
                   "B":["elv", "elv","elv", "elv","fae",
                        "fae","fae", "fae","bog", "bog",
                        "bog", "bog","bog", "bog","bog",
                        "bog","ele", "chn","trf", "trf",],
                   "R":["bog", "bog","bog", "bog","gnt",
                        "gnt","gnt", "gnt","gnt", "gnt",
                        "gnt", "ele","ele", "ele","ele",
                        "ele","ele", "ele","ele", "chn",],
                   "G":["elv", "elv","elv", "elv","elv",
                        "elv","elv", "elv","kth", "kth",
                        "ele", "chn","trf", "trf","trf",
                        "trf","trf", "trf","trf", "trf",]
                  },#The tribes of Lorwyn, each colour gets a weighted list out of 20 for approximately equal presence
        "story_event":{"W":["brigid"],"U":["cliq"],"B":["mrln"],"R":["ashl"],"G":["rhys"]},#Major characters 
        "world_event":{"W":["evnt1"],"U":["evnt1"],"B":["evnt1"],"R":["evnt2"],"G":["evnt2"]}
        #Add more world details here, eg background art and bossfight details
        },
    }
planeswalkers = {"jace":{"name": "Jace Beleren",'storykey':'jace',
                         "stages": [{'text':"Stage 1 description", #Text to display while figuring out resolution
                                     'card_disp' : 3,
                                     'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]},
                                    {'text':"Stage 2 description", #Text to display while figuring out resolution
                                     'card_disp' : 3,
                                     'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]},
                                    {'text':"Hostility description", #Final spot is reserved for when the group has been set to hostile
                                     'card_disp' : 3,
                                     'new_stage': [-1,-1,-1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "battle","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]}],
                         "fightparams" : {"color": ["U"],},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                         "exclusive_params" : {"color": True}#Should be monoblue only
                         "blankparams" : {"color": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                         "negparams" : {"card_type": ["Token","Basic", "Emblem"]}, #Values that are specifically not allowed
                        },
                 "placeholder_planeswalker":{"name": "Faction 2",'storykey':'storyplace',
                         "stages": [{'text':"Stage 1 description", #Text to display while figuring out resolution
                                     'card_disp' : 3,
                                     'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]},
                                    {'text':"Stage 2 description", #Text to display while figuring out resolution
                                     'card_disp' : 3,
                                     'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]},
                                    {'text':"Hostility description", #Final spot is reserved for when the group has been set to hostile
                                     'card_disp' : 3,
                                     'new_stage': [-1,-1,-1], #Stage this group is set to upon each possible outcome of the event
                                     'method': ["battle", "battle","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                     "reward": [{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                 'legend': [False]},
                                                {},
                                                {},]}],
                         "fightparams" : {"set": [],
                                          "rarity": ["common","uncommon","rare", "mythic rare"],
                                          "color": ["W", "U", "B", "R", "G"],
                                          "mana_cost": [],
                                          "mana_symbols": [],
                                          "name": [],
                                          "cmc": [],
                                          "card_type": [],
                                          "subtypes": [],
                                          "keywords": [],
                                          "oracle_text": [],
                                          "legend": []},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                         "exclusive_params" : {"set": False,
                                               "rarity": False,
                                               "color": True,
                                               "mana_cost": False,
                                               "mana_symbols": False,
                                               "name": False,
                                               "cmc": False,
                                               "card_type": False,
                                               "subtypes": False,
                                               "keywords": False,
                                               "oracle_text": False,
                                               "legend": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                         "blankparams" : {"set": False,
                                          "rarity": False,
                                          "color": False,
                                          "mana_cost": False,
                                          "mana_symbols": False,
                                          "name": False,
                                          "cmc": False,
                                          "card_type": False,
                                          "subtypes": False,
                                          "keywords": False,
                                          "oracle_text": False,
                                          "legend": False}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                         "negparams" : {"set": [],
                                        "rarity": [],
                                        "color": [],
                                        "mana_cost": [],
                                        "mana_symbols": [],
                                        "name": [],
                                        "cmc": [],
                                        "card_type": ["Token","Basic"],
                                        "subtypes": [],
                                        "keywords": [],
                                        "oracle_text": [],
                                        "legend": []}, #Values that are specifically not allowed
                        }
}