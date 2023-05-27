worlds = {#Information per world to use in building and navigating maps, including character and story information. Exact implementation tbd, but should be robust and accessible for many different arrangements of worlds
    "Place": {#Placeholder world
        # ...
        "events": {#Types of events in this world. Should be the same for all worlds, but doesn't have to be.
            "battle": {#Parameters to use when constructing GM decks for different locations
                #Although this functions like any other event and can involve storylines or choices if you want, the intention is to use it for basic per-lane events, equivalent to world events but with one event that has internal colour splits
                    "W": {"fightparams" : {"color": ["W"]},"negparams" : {"card_type": ["Token","Basic"]},
                         "stages" : [{'text':'You are attacked by the denizens of this plane.\n', 'method':['battle'], 'options':['(Left click to continue)']}]
                         },
                    "U": {"fightparams" : {"color": ["U"]},"negparams" : {"card_type": ["Token","Basic"]},
                         "stages" : [{'text':'You are attacked by the denizens of this plane.\n', 'method':['battle'], 'options':['(Left click to continue)']}]},
                    "B": {"fightparams" : {"color": ["B"]},"negparams" : {"card_type": ["Token","Basic"]},
                         "stages" : [{'text':'You are attacked by the denizens of this plane.\n', 'method':['battle'], 'options':['(Left click to continue)']}]},
                    "R": {"fightparams" : {"color": ["R"]},"negparams" : {"card_type": ["Token","Basic"]},
                         "stages" : [{'text':'You are attacked by the denizens of this plane.\n', 'method':['battle'], 'options':['(Left click to continue)']}]},
                    "G": {"fightparams" : {"color": ["G"]},"negparams" : {"card_type": ["Token","Basic"]},
                         "stages" : [{'text':'You are attacked by the denizens of this plane.\n', 'method':['battle'], 'options':['(Left click to continue)']}]},
                    # Additional GM deck configurations
            },
            "faction_event": {"fae":{"name": "Faeries",'storykey':'fae',
                                     "fightparams" : {"color": ["B", "U"],
                                                      "card_type": ["Creature", "Sorcery","Instant","Enchantment"],
                                                      "subtypes": ["Faerie", "Aura"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"subtypes": False}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "negparams" : {"card_type": ["Token","Basic"], "name":["Nath of the Gilt-Leaf"]}, #Values that are specifically not allowed
                                     "enemy_params":{"subtypes":["Merfolk"]},
                                     "stages": [{'text':
                                                 "You meet a clique of faeries, travelling from Kinsbaile to their secret home carrying stolen dreamstuffs.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Fight the thieves before they steal from your mind too. (FIGHT)","(M) Barter with them, dreams are not the only form of magic they might use. (TRADE)","(R) Ask if they have stolen any interesting dreams of late, and discuss with them the secrets of the other tribes. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ["Diviner's Wand"], 'cmc': [3.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Wizard', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "Whenever you draw a card, this creature gets +1/+1 and gains flying until end of turn" and "{4}: Draw a card."\nWhenever a Wizard creature enters the battlefield, you may attach Diviner\'s Wand to it.\nEquip {3}'], 'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'],#Harbinger
                                                              'rarity': ['uncommon'],
                                                              'color': ['U'],
                                                              'mana_cost': ['3', 'U'],
                                                              'mana_symbols': ['U'],
                                                              'name': ['Faerie Harbinger'],
                                                              'cmc': [4.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Faerie', 'Wizard'],
                                                              'keywords': ['Flying', 'Flash'],'power': [2], 'toughness': [2],
                                                              'watermark': [],
                                                              'oracle_text': ['Flash\nFlying\nWhen Faerie Harbinger enters the battlefield, you may search your library for a Faerie card, reveal it, then shuffle and put that card on top.'],
                                                              'legend': [False]}],]},
                                                {'text':
                                                 "You meet a clique of faeries, discussing how best to sneak past the merfolk and steal from something in the depths of the wanderwine river for their queen Oona.\nThey cannot fly beneath the water, and the merrows are too vigilant to be snuck past anyway./n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) These faeries have gone too far, it is time to end their treachery. (FIGHT)","(M) Perhaps some extra magic will help them, in exchange for some secrets of course. (TRADE)","(R) Offer to help in getting past the merfolk by force. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,1,2], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ["Diviner's Wand"], 'cmc': [3.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Wizard', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "Whenever you draw a card, this creature gets +1/+1 and gains flying until end of turn" and "{4}: Draw a card."\nWhenever a Wizard creature enters the battlefield, you may attach Diviner\'s Wand to it.\nEquip {3}'], 'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['U'], 'mana_cost': ['2', 'U'], 'mana_symbols': ['U'], 'name': ['Scion of Oona'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Faerie', 'Soldier'], 'keywords': ['Flying', 'Flash'], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ["Flash\nFlying\nOther Faerie creatures you control get +1/+1.\nOther Faeries you control have shroud. (They can't be the targets of spells or abilities.)"], 'legend': [False]}],]},
                                                {'text':
                                                 "You come across those same faeries, who eagerly ask if you have yet gotten past the merrows.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) The deal is off, time to end your short little lives.","(M) Not yet, I'm here to trade.","(R) The merrows won't be a problem anymore, you can send someone down to the depths whenever you're ready."],
                                                 "req_keys":[[],["enemy"], ["mer_l_-1", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,2,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ["Diviner's Wand"], 'cmc': [3.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Wizard', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "Whenever you draw a card, this creature gets +1/+1 and gains flying until end of turn" and "{4}: Draw a card."\nWhenever a Wizard creature enters the battlefield, you may attach Diviner\'s Wand to it.\nEquip {3}'], 'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'U'], 'mana_cost': ['2', 'U', 'B'], 'mana_symbols': ['U', 'B'], 'name': ['Wydwen, the Biting Gale'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Faerie', 'Wizard'], 'keywords': ['Flying', 'Flash'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Flash\nFlying\n{U}{B}, Pay 1 life: Return Wydwen, the Biting Gale to its owner's hand."], 'legend': [True]}, 
                                                               {'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'U'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Secluded Glen'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Secluded Glen enters the battlefield, you may reveal a Faerie card from your hand. If you don't, Secluded Glen enters the battlefield tapped.\n{T}: Add {U} or {B}."], 'legend': [False]}],]},
                                                {'text':
                                                 "Returning to the secret glade shown to you by the faeries, you are greeted as a welcome guest.\nThe tiny beings shower you with gifts, and amidst the excited chittering you gather that they successfully journeyed deep below Lorwyn, through the merrow's paths to a cave home to an enourmous slumbering giant.\nHaving stolen its age-long dreams, hopefully without waking it, they are celebrating with a feast.", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) There will be no feast today, their time has come. (FIGHT)","(M) While their gifts are lovely, you'd much rather offer something in return. (TRADE)","(R) Accept their gifts and join the feast, it seems dreamstuff is not a bad substitute for aether. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,3,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [],]},
                                                {'text':"As you travel, you are beset by a faerie clique, seeking retribution for your previous attacks.\n", #Group is set to be hostile indefinitely
                                                 'new_stage': [-2], #Stage this group is set to upon each possible outcome of the event
                                                 'options': ["(L) FIGHT"],
                                                 'method': ["battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                },
                                                {'text':"To your surprise, you happen upon a faerie glade, with only a few sprites guarding the edges.\nThey haven't yet spotted you, distracted by something powerful they have created from stolen magic.\nIt's possible they know of your previous hostilities with their kind, as words spread fast among these tiny creatures but so too does the forgetting of grievances.\nBefore you can make up your mind, a patrol finds you.\n", #Group is set to be hostile
                                                 'new_stage': [-1,0,-2], #Stage this group is set to upon each possible outcome of the event
                                                 'options': ["(L) Quickly attack, making sure word of your actions doesn't spread.", "(M) Approach carefully, apologising and hoping to make amends.", "(R) Attack the glade, stealing the powerful artifact."],
                                                 'method': ["battle", "reward","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[],
                                                            [],
                                                            [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['4'], 'mana_symbols': [], 'name': ['Deathrender'], 'cmc': [4.0], 'card_type': ['Artifact'], 'subtypes': ['Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature gets +2/+2.\nWhenever equipped creature dies, you may put a creature card from your hand onto the battlefield and attach Deathrender to it.\nEquip {2}'], 'legend': [False]}],]}],},
                              "bog":{"name": "Elves",'storykey':'bog',
                                     "fightparams" : {"color": ["B", "R"],
                                                      "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                                                      "subtypes": ["Goblin"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"subtypes": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "negparams" : {"card_type": ["Token","Basic"], 'name': ['Wort, Boggart Auntie']}, #Values that are specifically not allowed
                                     "enemy_params":{"subtypes":["Kithkin"]},
                                     "stages": [{'text':
                                                 "You meet a group of boggarts, the mischeivous kind of goblin that inhabit this world.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Goblin1 placeholder (FIGHT)","(M) The boggarts value new sensations above all else, perhaps your magic is worth some kind of deal. (TRADE)","(R) Tell them about the pranks you got up to on your home plane. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ['Springleaf Drum'], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Tap an untapped creature you control: Add one mana of any color.'], 'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Boggart Harbinger'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': [], 'power': ['2'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['When Boggart Harbinger enters the battlefield, you may search your library for a Goblin card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],]},
                                                {'text':
                                                 "On the outskirts of Kinsbaile you find a goblin camp.\nAn elder among them explains that the kithkin captured several boggarts that strayed too close to Kinsbaile.\nBut with the big guard towers they've been building, they've got no hope of getting back their friends without burning the towers down.\n", #Quest giving
                                                 'card_disp' : 3,
                                                 'options': ["(L) Tell them you'll warn the kithkin, those towers are important. (FIGHT)","(M) That sounds... fun, but can I interest you in some magic? (TRADE)","(R) Offer to help with dramatic sorcery, perhaps a distraction will help. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],'new_stage': [-1,1,2], 'method': ["battle", "trade","reward"], 
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ['Springleaf Drum'], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Tap an untapped creature you control: Add one mana of any color.'], 'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Mad Auntie'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Other Goblin creatures you control get +1/+1.\n{T}: Regenerate another target Goblin.'], 'legend': [False]}],]},
                                                {'text':
                                                 "Coming across the goblin encampment again, they ask if you've burned down the kithkin towers yet.\nKnowing how great the story must be, they invite you in to share your experiences.", #Quest resolution
                                                 'card_disp' : 3,
                                                 'options': ["(L) Goblin meeting 3 placeholder combat. (FIGHT)","(M) Not yet, you need to trade for some supplies first. (TRADE)","(R) Regail them with the story of how high the towers burned, and the warmth and smell of it. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["kth_l_-2", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,2,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ['Springleaf Drum'], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Tap an untapped creature you control: Add one mana of any color.'], 'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'R'], 'mana_cost': [], 'mana_symbols': [], 'name': ["Auntie's Hovel"], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Auntie's Hovel enters the battlefield, you may reveal a Goblin card from your hand. If you don't, Auntie's Hovel enters the battlefield tapped.\n{T}: Add {B} or {R}."], 'legend': [False]}, 
                                                               {'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'R'], 'mana_cost': ['2', 'B', 'R'], 'mana_symbols': ['B', 'R'], 'name': ['Wort, Boggart Auntie'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': ['Fear'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Fear (This creature can't be blocked except by artifact creatures and/or black creatures.)\nAt the beginning of your upkeep, you may return target Goblin card from your graveyard to your hand."], 'legend': [True]}],]},
                                                {'text':
                                                 "You return to the Boggart encampment.\n", #Stage 4, indefinite
                                                 'card_disp' : 3,
                                                 'options': ["(L) Attack the makeshift settlement. (FIGHT)","(M) Share your stories, for a price. (TRADE)","(R) Listen to the tales of new experiences the goblins have found. (PUZZLE)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,3,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ['Springleaf Drum'], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Tap an untapped creature you control: Add one mana of any color.'], 'legend': [False]}],
                                                               [],
                                                               [],]},
                                                {'text':
                                                "You're spotted by a group of goblins, angry at your previous attacks\n.", #-1, Group is set to be hostile indefinitely
                                                 'new_stage': [-2],'options': ["(L) FIGHT"],'method': ["battle"],},
                                                {'text':
                                                "To your surprise, you happen upon a faerie glade, with only a few sprites guarding the edges.\nThey haven't yet spotted you, distracted by something powerful they have created from stolen magic.\nIt's possible they know of your previous hostilities with their kind, as words spread fast among these tiny creatures but so too does the forgetting of grievances.\nBefore you can make up your mind, a patrol finds you.\n",
                                                'new_stage': [-1,0,-2], 'options': ["(L) Quickly attack, making sure word of your actions doesn't spread.", "(M) Approach carefully, apologising and hoping to make amends.", "(R) Attack the glade, stealing the powerful artifact."],
                                                 'method': ["battle", "reward","battle"], 
                                                 "reward": [[],[],[{'set': ['m10'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['5'], 'mana_symbols': [], 'name': ['Coat of Arms'], 'cmc': [5.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Each creature gets +1/+1 for each other creature on the battlefield that shares at least one creature type with it. (For example, if two Goblin Warriors and a Goblin Shaman are on the battlefield, each gets +2/+2.)'], 'legend': [False]}],]}],},
                              "elv":{"name": "Elves",'storykey':'elf',
                                     "fightparams" : {"color": ["B", "G"],
                                                      "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                                                      "subtypes": ["Elf"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"subtypes": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "negparams" : {"card_type": ["Token","Basic"], "name":["Nath of the Gilt-Leaf"]}, #Values that are specifically not allowed
                                     "enemy_params":{"subtypes":["Goblin"]},
                                     "stages": [{'text':
                                                 "You journey across Lorwyn, enjoying the beautiful scenery of the plane's permanent summer day.\nAs the sun lowers one morning in the East, you notice an unusual hush -\nthe birds that would normally anounce the occasion falling silent.\nYou hear a footstep behind you, and at once you are surrounded by strange slight figures.\nThough their horns and hooves set them apart from those you've seen on your home plane,\nthe pointed ears and perfect faces are unmistakably Elvish.\nAs they examine and judge you, one of the hunters holds a blade to your neck.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Suspecting you'll be hunted like the goblins of this world, you launch an attack. (FIGHT)","(M) You carefully offer a small gift, hoping that trade will be more compelling than beauty. (TRADE)","(R) Seeing the beauty of you and your companions, the elves judge you worthy of survival, at least for now. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'],#First reward: Harbinger
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Elvish Harbinger'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Druid'],
                                                              'keywords': [],'power': [1], 'toughness': [2],
                                                              'watermark': [],
                                                              'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],
                                                              'legend': [False]}],]},
                                                {'text':
                                                 "In an opening ahead you see a group of elves stood in a circle around a strange shape on the ground.\nAs you approach, you realise the shape is a boggart, arrows stuck in its back.\n'Care to join in on the hunt?' one says, turning to face you.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Yes, I think I will. (FIGHT)","(M) Perhaps another day, say do you have need of some hunting supplies? (TRADE)","(R) EOf course, which way did the others go? (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,1,2], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                            [],
                                                            [{'set': ['lrw'],#Second reward: Lord
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Imperious Perfect'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],'power': [2], 'toughness': [2],
                                                              'watermark': [],
                                                              'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [False]}],]},
                                                {'text':
                                                 "Travelling through the Gilt-Leaf wood, you find yourself outside a grand elven palace.\n'Ah, if it isn't the new winnower,' says a guard,\n'Care to present your trophies to our liege?'\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Elf meeting 3 placeholder combat. (FIGHT)","(M) Elf meeting 3 placeholder trade. (TRADE)","(R) Elf meeting 3 placeholder reward. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["bog_l_-2", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,2,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#Third reward: Land and Legend
                                                              'rarity': ['rare'],
                                                              'color': ['B', 'G'],
                                                              'mana_cost': ['3', 'B', 'G'],
                                                              'mana_symbols': ['B', 'G'],
                                                              'name': ['Nath of the Gilt-Leaf'],
                                                              'cmc': [5.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],'power': [4], 'toughness': [4],
                                                              'watermark': [],
                                                              'oracle_text': ['At the beginning of your upkeep, you may have target opponent discard a card at random.\nWhenever an opponent discards a card, you may create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [True]}, 
                                                               {'set': ['lrw'],
                                                              'rarity': ['rare'],
                                                              'color': ['B', 'G'],
                                                              'mana_cost': [],
                                                              'mana_symbols': [],
                                                              'name': ['Gilt-Leaf Palace'],
                                                              'cmc': [0.0],'power': [0], 'toughness': [0],
                                                              'card_type': ['Land'],
                                                              'subtypes': [],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ["As Gilt-Leaf Palace enters the battlefield, you may reveal an Elf card from your hand. If you don't, Gilt-Leaf Palace enters the battlefield tapped.\n{T}: Add {B} or {G}."],
                                                              'legend': [False]}],]},
                                                {'text':
                                                 "You return to Gilt-Leaf wood.\n", #Stage 4, indefinite
                                                 'card_disp' : 3,
                                                 'options': ["(L) Attack the elvish settlement. (FIGHT)","(M) Elf meeting 4 placeholder trade. (TRADE)","(R) Ask for allies in your quest. (JOIN)"],
                                                 "req_keys":[[],["enemy"], ["match", "enemy"]],#Per option, a list of its requirements
                                                 'new_stage': [-1,3,3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#Repeated reward: Lord and Harbinger
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Imperious Perfect'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],'power': [2], 'toughness': [2],
                                                              'watermark': [],
                                                              'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [False]},
                                                               {'set': ['lrw'],
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Elvish Harbinger'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Druid'],
                                                              'keywords': [],'power': [1], 'toughness': [2],
                                                              'watermark': [],
                                                              'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],
                                                              'legend': [False]}],]},
                                                {'text':"Having lost access to the Door of Destinies, the elves blame you for their waning power in Lorwyn. As a trumpet warns of your presence, you find yourself surrounded by an Elvish hunting party", #Group is set to be hostile indefinitely
                                                 'new_stage': [-2], #Stage this group is set to upon each possible outcome of the event
                                                 'options': ["(L) FIGHT"],
                                                 'method': ["battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                },
                                                {'text':"Up ahead you see an encampment of elves. You're unsure if they know of your previous hostilities with their kind.\n(L) Quickly attack, making sure word of your actions doesn't spread.\n(M) Approach carefully, apologising and hoping to make amends.\n(R) Assault the camp, stealing a powerful artifact but ensuring all of their kind know of your misdeeds.", #Group is set to be hostile
                                                 'new_stage': [-1,0,-2], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["battle", "reward","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[],
                                                            [],
                                                            [{'set': ['mor'],
                                                              'rarity': ['rare'],
                                                              'color': [],
                                                              'mana_cost': ['4'],
                                                              'mana_symbols': [],
                                                              'name': ['Door of Destinies'],
                                                              'cmc': [4.0],
                                                              'card_type': ['Artifact'],
                                                              'subtypes': [],
                                                              'keywords': [],'power': [0], 'toughness': [0],
                                                              'watermark': [],
                                                              'oracle_text': ['As Door of Destinies enters the battlefield, choose a creature type.\nWhenever you cast a spell of the chosen type, put a charge counter on Door of Destinies.\nCreatures you control of the chosen type get +1/+1 for each charge counter on Door of Destinies.'],
                                                              'legend': [False]}],]}],},
                            "faction2":{"name": "Faction 2",'storykey':'storyplace',
                                        "stages": [{'text':"Stage 1 description", #Text to display while figuring out resolution
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['roe'],#Reward at this stage, card is specified, depends on method taken
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
                                                                'legend': [False]}],
                                                               [],
                                                               [],]},
                                                   {'text':"Stage 2 description", #Text to display while figuring out resolution
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,0,2], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                   },
                                                   {'text':"Hostility description", #Final spot is reserved for when the group has been set to hostile
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,-1,-1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "battle","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[],
                                                               [],[]]}],
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
            "story_event": {#The key difference with this type of event is that they should be enforced to occur a set number of times in a map. Other than that, they don't really function any differently than regular faction events
                "austere":{"name": "Greater Elementals (White)",'storykey':'austere',
                                     "fightparams" : {"color": ["W"],
                                                      "card_type": ["Creature", "Sorcery","Enchantment"],
                                                      "subtypes": ["Elemental"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"subtypes": False}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "negparams" : {"name":["Austere Command", "Cryptic Command", "Profane Command", "Incendiary Command", "Primal Command"],"subtypes": ["Soldier", "Warrior", "Incarnation"],"card_type": ["Token","Basic"]}, #Values that are specifically not allowed, this should leave mostly greater elementals
                                     "enemy_params":{"subtypes":["Elemental"]},
                                     "stages": [{'text':
                                                 "You find yourself in an open field, filled with the beauty of this plane.\nThe magical energy here is strong, and at first you suspect it may be a leyline.\nThe magical energy suddenly swells, splitting into its five components and causing strange lights to dance through the air.\nThe magic begins to distort the landscape, taking strange forms and coalescing as elementals\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Seeing how the energy reacts to your thoughts and emotions, you clear your mind and connect to the mana of this place. You allow the strange aurora to pass over both it and you.",#Solution corresponding to Purity
                                                             "(M) Seeking visions in the strange lights, you begin to divine intention from these manifestations of thought and magic.",#Guile
                                                             "(R) This disturbance will corrupt the beauty of this place, and only power will let you withstand it. So power is what you will take.",#Dread
                                                             "(ScrUp) As the elemental energies grow ever more unstable, you prepare to defend yourself.",#Hostility
                                                             "(ScrDn) Allow the energy to suffuse and reinvigorate you as you connect to this land's mana."#Vigor
                                                            ],
                                                 "req_keys":[["austere_g_0"],["cryptic_g_0"], ["profane_g_0", "cost2"], ["incend_g_0"], ["primal_g_0"]],#Each option requires you to at least begin the relevant storyline for the other colour. 
                                                 'new_stage': [1], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["rest", "puzzle","aether", "battle", "aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Vivid Meadow'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Vivid Meadow enters the battlefield tapped with two charge counters on it.\n{T}: Add {W}.\n{T}, Remove a charge counter from Vivid Meadow: Add one mana of any color.'], 'legend': [False]}]]},
                                                {'text':
                                                 "As you travel through a field near Kinsbaile, an archer travels out to meet you. Introducing herself as Brigid, she asks if you and your magic are a threat to her home.\nA shimmering in the air alerts you to another surge of magical energy.\nThe suspicious kithkin draws her bow, suspecting you as the cause, ", #Stage 1, Currently a placeholder!!!
                                                 'options': ["(L) Knowing the importance of emotions to these elemental disturbances, you remain austere, hoping to preserve the purity of the land.",#Solution corresponding to Purity
                                                             "(M) Seeking visions in the strange lights, you begin to divine intention from these manifestations of thought and magic.",#Guile
                                                             "(R) This disturbance will corrupt the beauty of this place, and only power will let you withstand it. So power is what you will take.",#Dread
                                                             "(ScrUp) As the elemental energies grow ever more unstable, you prepare to defend yourself.",#Hostility
                                                             "(ScrDn) Allow the energy to suffuse and reinvigorate you as you connect to this land's mana."#Vigor
                                                            ],
                                                 "req_keys":[["austere_g_1"],["cryptic_g_0"], ["profane_g_1", "cost2"], ["incend_g_1"], ["primal_g_0"]],#Each option requires you to at least begin the relevant storyline for the other colour. 
                                                 'new_stage': [2], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["rest", "puzzle","aether", "battle", "aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['2', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Brigid, Hero of Kinsbaile'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Kithkin', 'Archer'], 'keywords': ['First strike'], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['First strike\n{T}: Brigid, Hero of Kinsbaile deals 2 damage to each attacking or blocking creature target player controls.'], 'legend': [True]}]]},
                                                {'text':
                                                 "Purity story stage 2\n", #Stage 2, Currently a placeholder!!!
                                                 'options': ["(L) Seeing how the energy reacts to your thoughts and emotions, you clear your mind and connect to the mana of this place. You allow the strange aurora to pass over both it and you.",#Solution corresponding to Purity
                                                             "(M) Seeking visions in the strange lights, you begin to divine intention from these manifestations of thought and magic.",#Guile
                                                             "(R) This disturbance will corrupt the beauty of this place, and only power will let you withstand it. So power is what you will take.",#Dread
                                                             "(ScrUp) As the elemental energies grow ever more unstable, you prepare to defend yourself.",#Hostility
                                                             "(ScrDn) Allow the energy to suffuse and reinvigorate you as you connect to this land's mana."#Vigor
                                                            ],
                                                 "req_keys":[["austere_g_0"],["cryptic_g_0"], ["profane_g_0", "cost2"], ["incend_g_0"], ["primal_g_0"]],#Each option requires you to at least begin the relevant storyline for the other colour. 
                                                 'new_stage': [3], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["rest", "puzzle","aether", "battle", "aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['3', 'W', 'W', 'W'], 'mana_symbols': ['W', 'W', 'W'], 
                                                              'name': ['Purity'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Flying'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 
                                                              'oracle_text': ["Flying\nIf noncombat damage would be dealt to you, prevent that damage. You gain life equal to the damage prevented this way.\nWhen Purity is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]},
                                                             {'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['4', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Austere Command'], 'cmc': [6.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [],
                                                               'oracle_text': ['Choose two —\n• Destroy all artifacts.\n• Destroy all enchantments.\n• Destroy all creatures with mana value 3 or less.\n• Destroy all creatures with mana value 4 or greater.'], 'legend': [False]}
                                                              ]]},
                                                {'text':
                                                 "Purity story stage 3\n", #Stage 3, Currently a placeholder!!!
                                                 'options': ["(L) Knowing the importance of emotions to these elemental disturbances, you remain austere, hoping to preserve the purity of the land.",#Solution corresponding to Purity
                                                             "(M) Seeking visions in the strange lights, you begin to divine intention from these manifestations of thought and magic.",#Guile
                                                             "(R) This disturbance will corrupt the beauty of this place, and only power will let you withstand it. So power is what you will take.",#Dread
                                                             "(ScrUp) As the elemental energies grow ever more unstable, you prepare to defend yourself.",#Hostility
                                                             "(ScrDn) Allow the energy to suffuse and reinvigorate you as you connect to this land's mana."#Vigor
                                                            ],
                                                 "req_keys":[["austere_g_0"],["cryptic_g_0"], ["profane_g_0", "cost2"], ["incend_g_0"], ["primal_g_0"]],#Each option requires you to at least begin the relevant storyline for the other colour. 
                                                 'new_stage': [2], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["rest", "puzzle","aether", "battle", "aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                }
                                               ]},
                            "story2":{"name": "Story 2",
                                      "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],}
                            # Add more stories here
                           },
            "boss":{ "boss1": {"name": "Placeholder Boss",'storykey':'Boss1',#Boss events are enforced to always happen in the final nodes, though there's no reason they can't also be used earlier
                               "fightparams" : {"card_type": ["Creature", "Enchantment"],"color": ["W", "U","B","R","G"], "subtypes":["Elemental"]},#Values that match the mirror itself
                                     "exclusive_params" : {"set": False}, "blankparams" : {"subtypes": False}, 
                                     "negparams" : {"card_type": ["Token","Basic"], "rarity": ["common"], "subtypes":["Shaman"]},
                                     "stages":[{'text': "This is a placeholder boss battle.\n",
                                                "options": ["(Left click to continue)"], #Only one option here
                                                "method": ["battle"], #Only one option here
                                                "bossreq":[
                                                    [
                                                        ["austere_l_1"],["cryptic_l_-1"], ["profane_l_1"], ["incend_l_1"], ["primal_l_1"]]],
                                                "bossreward":[
                                                    [
                                                        [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['3', 'W', 'W', 'W'], 'mana_symbols': ['W', 'W', 'W'], 'name': ['Purity'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Flying'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Flying\nIf noncombat damage would be dealt to you, prevent that damage. You gain life equal to the damage prevented this way.\nWhen Purity is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]}],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['U'], 'mana_cost': ['3', 'U', 'U', 'U'], 'mana_symbols': ['U', 'U', 'U'], 'name': ['Guile'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': [], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Guile can't be blocked except by three or more creatures.\nIf a spell or ability you control would counter a spell, instead exile that spell and you may play that card without paying its mana cost.\nWhen Guile is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]}],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B'], 'mana_cost': ['3', 'B', 'B', 'B'], 'mana_symbols': ['B', 'B', 'B'], 'name': ['Dread'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Fear'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Fear (This creature can't be blocked except by artifact creatures and/or black creatures.)\nWhenever a creature deals damage to you, destroy it.\nWhen Dread is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]}],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['R'], 'mana_cost': ['3', 'R', 'R', 'R'], 'mana_symbols': ['R', 'R', 'R'], 'name': ['Hostility'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Haste'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Haste\nIf a spell you control would deal damage to an opponent, prevent that damage. Create a 3/1 red Elemental Shaman creature token with haste for each 1 damage prevented this way.\nWhen Hostility is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]}],
                                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['G'], 'mana_cost': ['3', 'G', 'G', 'G'], 'mana_symbols': ['G', 'G', 'G'], 'name': ['Vigor'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Trample'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Trample\nIf damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way.\nWhen Vigor is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]}]
                                                    ]
                                                ]
                                     }]
                              }
            },
            "world_event": {#Other world events, which may be adjacent to the main storyline but aren't required for completion.
                "mirror":{"name": "Magic Mirror",'storykey':'twinning',#Reflections of the player's own deck, used for copying cards
                                     "fightparams" : {"card_type": ["Creature"],
                                                      "subtypes": ["Spirit", "Wraith", "Illusion", "Shade", "Shapeshifter"]},#Values that match the mirror itself
                                     "exclusive_params" : {"set": False}, "blankparams" : {"subtypes": True}, 
                                     "negparams" : {"card_type": ["Token","Basic"]},
                                     "enemy_params":{"subtypes":["Vampire"]},
                                     "stages": [{'text':
                                                 "You see a figure approaching, matching your movements and pace. Cautious, you ready a few spells to protect yourself in case of a fight.\nAs you get closer, you realise it is not a stranger, but your own reflection.\nA mirror, made of polished silver and with an ornate frame, sits wedged between two rocks and overgrown with vegetation.\nYour own reflection, hazy and indistinct, begins to raise a hand.\n", #Stage 0, first meeting
                                                 'card_disp' : 3,
                                                 'options': ["(L) Raise a hand in response. If your reflection is a friend, this place could be a welcome respite.",#Peaceful option
                                                             "(M) Test the limits of the mirror, perhaps it can reflect your magic as well.",#Summoning option
                                                             "(R) Spend 2 aether to try to control the mirror's power.",#Try to steal the mirror
                                                             "(ScrUp) This reflection is not your own. This mirror must be destroyed before something horrible is conjured.",#Try to smash the mirror
                                                             "(ScrDn) Commune with your reflection, perhaps your power will be reflected here too."#If you have a spirit or shapeshifter with you
                                                            ],
                                                 "req_keys":[["enemy", "match"],["enemy"], ["cost2"], ["cost-3"], ["match"]],#Each option requires you to at least begin the relevant storyline for the other colour. 
                                                 'new_stage': [0,0,1,-1,0], #Stage this group is set to upon each possible outcome of the event
                                                 'method': ["rest", "m_trade","m_battle", "m_battle", "aether"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[], [], [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['4'], 'mana_symbols': [], 'name': ['Twinning Glass'], 'cmc': [4.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{1}, {T}: You may cast a spell from your hand without paying its mana cost if it has the same name as a spell that was cast this turn.'], 'legend': [False]}]]},
                                                {'text': "You return to the spot where the mirror once sat.\n",
                                                 "options": ["(L) With its magic gone, the area is safe enough to rest.", "(M) Whatever it was, its magic seemed to replicate the spirit of the subject. Perhaps you can recreate this magic yourself."],
                                                 "req_keys":[[],["match"]],
                                                 "method":[["rest"],["m_trade"]]},
                                                {'text': "You return to the spot where the mirror once sat.\n",
                                                 "options": ["(L) With its magic gone, the area is safe enough to rest."],
                                                 "method":[["rest"]]}
                                               ]}
                            # Add more story types here
                           }
        },
        "evnt_type":["battle","base","base","base","faction_event","faction_event","story_event","story_event","story_event","world_event","world_event","world_event","planeswalker"],#Relative weighting of event type, placeholder world is mostly factions as they are finished first for testing
        "lane_id":["R","B","U","W","G"],#Meaning of each lane in this world's minimap, usually based on colour. Will be used to key other features from this data
        "param":{"W":["detail"],"U":["detail"],"B":["detail"],"R":["detail"],"G":["detail"]}, #General form of how lane ids will give other details to be used for events
        "faction_event":{"W":["faction2", "faction2"],"U":["fae"],"B":["fae", "elv"],"R":["elv", "elv"],"G":["elv", "elv"]},
        "base":{"W":["rest"],"U":["puzzle"],"B":["summon", "puzzle"],"R":["summon"],"G":["rest", "summon"]},
        "boss":{"W":["boss1"],"U":["boss1"],"B":["boss1", "boss1"],"R":["boss1"],"G":["boss1"]},
        "story_event":{"W":["austere"],"U":["austere"],"B":["austere"],"R":["austere"],"G":["austere"]}, #,"U":["cryptic"],"B":["profane"],"R":["incend"],"G":["primal"]}, 
        "planeswalker":{"W":["placeholder_planeswalker"],"U":["jace"],"B":["placeholder_planeswalker"],"R":["placeholder_planeswalker"],"G":["placeholder_planeswalker"]},#Planeswalkers the player might encounter
        "world_event":{"W":["mirror"],"U":["mirror"],"B":["mirror"],"R":["mirror"],"G":["mirror"]},
        "setcodes":["m10", "m11", "lrw", "mor"] #sets to use in this plane, if they aren't specified for an event
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
                              "elv":{"name": "Elves",'storykey':'elf',
                                          "stages": ["Stage 1 description","Stage 2 description","Stage 3 description"],
                                          "fightparams" : {"set": ["lrw", "mrn"],
                                                       "color": ["B", "G"],
                                                       "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                                                       "subtypes": ["Elf"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                        "exclusive_params" : {"set": True},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                        "blankparams" : {"subtypes": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                        "negparams" : {"card_type": ["Token","Basic"]}, #Values that are specifically not allowed
                                        
                                        "stages": [{'text':
                                                    "You journey across Lorwyn, enjoying the neautiful scenery of the plane's permanent summer day. As the sun lowers one morning in the East, you notice an unusual hush.\nThe birds that would normally anounce the occasion fall silent.\nYou hear a footstep behind you, and at once you are surrounded by strange slight figures.\nThough their horns and hooves set them apart from those you've seen on your home plane, the pointed ears and perfect faces are unmistakably Elvish. As they examine and judge you, one of the hunters holds a blade to your neck.\n (L) Amongst the murmuring, you hear the words 'eyeblight' and 'hunt'. Not willing to be hunted, you launch an attack.\n(M) As the elves discuss their judgement of you, you carefully offer a small gift, hoping that trade will be more compelling than beauty.\n(R) Seeing the beauty of you and your companions, the elves judge you worthy of survival, at least for now.", #Stage 0, first meeting
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,0,1], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#First reward: Harbinger
                                                                  'rarity': ['uncommon'],
                                                                  'color': ['G'],
                                                                  'mana_cost': ['2', 'G'],
                                                                  'mana_symbols': ['G'],
                                                                  'name': ['Elvish Harbinger'],
                                                                  'cmc': [3.0],
                                                                  'card_type': ['Creature'],
                                                                  'subtypes': ['Elf', 'Druid'],
                                                                  'keywords': [],
                                                                  'watermark': [],
                                                                  'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],
                                                                  'legend': [False]}],]},
                                                   {'text':
                                                    "Elf meeting 2 placeholder text.\n (L) Elf meeting 2 placeholder combat.\n(M) Elf meeting 2 placeholder trade.\n(R) Elf meeting 2 placeholder reward.", #Stage 0, first meeting
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,1,2], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#Second reward: Lord
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Imperious Perfect'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [False]}],]},
                                                   {'text':
                                                    "Elf meeting 3 placeholder text.\n (L) Elf meeting 3 placeholder combat.\n(M) Elf meeting 3 placeholder trade.\n(R) Elf meeting 3 placeholder reward.", #Stage 0, first meeting
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,2,3], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#Third reward: Land and Legend
                                                              'rarity': ['rare'],
                                                              'color': ['B', 'G'],
                                                              'mana_cost': ['3', 'B', 'G'],
                                                              'mana_symbols': ['B', 'G'],
                                                              'name': ['Nath of the Gilt-Leaf'],
                                                              'cmc': [5.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ['At the beginning of your upkeep, you may have target opponent discard a card at random.\nWhenever an opponent discards a card, you may create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [True]}, 
                                                               {'set': ['lrw'],
                                                              'rarity': ['rare'],
                                                              'color': ['B', 'G'],
                                                              'mana_cost': [],
                                                              'mana_symbols': [],
                                                              'name': ['Gilt-Leaf Palace'],
                                                              'cmc': [0.0],
                                                              'card_type': ['Land'],
                                                              'subtypes': [],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ["As Gilt-Leaf Palace enters the battlefield, you may reveal an Elf card from your hand. If you don't, Gilt-Leaf Palace enters the battlefield tapped.\n{T}: Add {B} or {G}."],
                                                              'legend': [False]}],]},
                                                   {'text':
                                                    "Elf meeting 4 placeholder text.\n (L) Elf meeting 4 placeholder combat.\n(M) Elf meeting 4 placeholder trade.\n(R) Elf meeting 4 placeholder reward.", #Stage 0, first meeting
                                                    'card_disp' : 3,
                                                    'new_stage': [-1,3,3], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "trade","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['mor'],#Reward for betraying this faction
                                                              'rarity': ['uncommon'],
                                                              'color': [],
                                                              'mana_cost': ['2'],
                                                              'mana_symbols': [],
                                                              'name': ['Cloak and Dagger'],
                                                              'cmc': [2.0],
                                                              'card_type': ['Tribal', 'Artifact'],
                                                              'subtypes': ['Rogue', 'Equipment'],
                                                              'keywords': ['Equip'],
                                                              'watermark': [],
                                                              'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],
                                                              'legend': [False]}],
                                                               [],
                                                               [{'set': ['lrw'],#Repeated reward: Lord and Harbinger
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Imperious Perfect'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Warrior'],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],
                                                              'legend': [False]},
                                                               {'set': ['lrw'],
                                                              'rarity': ['uncommon'],
                                                              'color': ['G'],
                                                              'mana_cost': ['2', 'G'],
                                                              'mana_symbols': ['G'],
                                                              'name': ['Elvish Harbinger'],
                                                              'cmc': [3.0],
                                                              'card_type': ['Creature'],
                                                              'subtypes': ['Elf', 'Druid'],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],
                                                              'legend': [False]}],]},
                                                   {'text':"Having lost access to the Door of Destinies, the elves blame you for their waning power in Lorwyn. As a trumpet warns of your presence, you find yourself surrounded by an Elvish hunting party", #Group is set to be hostile indefinitely
                                                    'new_stage': [-2,-2,-2], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "battle","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                   },
                                                   {'text':"Up ahead you see an encampment of elves. You're unsure if they know of your previous hostilities with their kind.\n(L) Quickly attack, making sure word of your actions doesn't spread.\n(M) Approach carefully, apologising and hoping to make amends.\n(R) Assault the camp, stealing a powerful artifact but ensuring all of their kind know of your misdeeds.", #Group is set to be hostile
                                                    'new_stage': [-1,0,-2], #Stage this group is set to upon each possible outcome of the event
                                                    'method': ["battle", "reward","battle"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                    "reward": [[{'set': ['mor'],#Reward for escalating the hostilities
                                                              'rarity': ['rare'],
                                                              'color': [],
                                                              'mana_cost': ['4'],
                                                              'mana_symbols': [],
                                                              'name': ['Door of Destinies'],
                                                              'cmc': [4.0],
                                                              'card_type': ['Artifact'],
                                                              'subtypes': [],
                                                              'keywords': [],
                                                              'watermark': [],
                                                              'oracle_text': ['As Door of Destinies enters the battlefield, choose a creature type.\nWhenever you cast a spell of the chosen type, put a charge counter on Door of Destinies.\nCreatures you control of the chosen type get +1/+1 for each charge counter on Door of Destinies.'],
                                                              'legend': [False]}],[],[],]}],}
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
                         "fightparams" : {"color": ["U"]},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                         "exclusive_params" : {"color": True},#Should be monoblue only
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

#Base events: event types that are used in every world and should never change (though their proportions can change)
base_events = {"start":{"name": "Starting Deck", #Maybe make this into a different start option per node colour?
                                     "stages": [{'text':
                                                 "Choose a starting deck:\n",
                                                 'options': ["(L) White","(M) Blue","(R) Black", "(ScrollUp) Red", "(ScrollDwn) Green"], #To do: Add more descriptions, also maybe have this be lane specific, and include option to draft?
                                                 'method': ["reward", "reward","reward", "reward","reward"], #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                                 "reward": [[{'set': ['m10'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['W'], 'mana_symbols': ['W'], 'name': ['Soul Warden'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Cleric'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Whenever another creature enters the battlefield, you gain 1 life.'], 'legend': [False]},{'set': ['m11'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ["Angel's Feather"], 'cmc': [2.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'watermark': [], 'oracle_text': ['Whenever a player casts a white spell, you may gain 1 life.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['2', 'W'], 'mana_symbols': ['W'], 'name': ['Griffin Sentinel'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Griffin'], 'keywords': ['Flying', 'Vigilance'], 'power': ['1'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Flying\nVigilance (Attacking doesn't cause this creature to tap.)"], 'legend': [False]}, {'set': ['m11'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['2', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Cloud Crusader'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Knight'], 'keywords': ['Flying', 'First strike'], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Flying\nFirst strike (This creature deals combat damage before creatures without first strike.)'], 'legend': [False]}, {'set': ['m11'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['4', 'W'], 'mana_symbols': ['W'], 'name': ['Tireless Missionaries'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Cleric'], 'keywords': [], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['When Tireless Missionaries enters the battlefield, you gain 3 life.'], 'legend': [False]}],
                                                            [{'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['U'], 'mana_symbols': ['U'], 'name': ['Zephyr Sprite'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Faerie'], 'keywords': ['Flying'], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Flying'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['1', 'U'], 'mana_symbols': ['U'], 'name': ['Convincing Mirage'], 'cmc': [2.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Enchant land\nAs Convincing Mirage enters the battlefield, choose a basic land type.\nEnchanted land is the chosen type.'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['2', 'U'], 'mana_symbols': ['U'], 'name': ['Scroll Thief'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Merfolk', 'Rogue'], 'keywords': [], 'power': ['1'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Whenever Scroll Thief deals combat damage to a player, draw a card.'], 'legend': [False]},{'set': ['m11'], 'rarity': ['uncommon'], 'color': ['U'], 'mana_cost': ['2', 'U', 'U'], 'mana_symbols': ['U', 'U'], 'name': ['Sleep'], 'cmc': [4.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Tap all creatures target player controls. Those creatures don't untap during that player's next untap step."], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['4', 'U'], 'mana_symbols': ['U'], 'name': ['Serpent of the Endless Sea'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Serpent'], 'keywords': [], 'power': ['*'], 'toughness': ['*'], 'watermark': [], 'oracle_text': ["Serpent of the Endless Sea's power and toughness are each equal to the number of Islands you control.\nSerpent of the Endless Sea can't attack unless defending player controls an Island."], 'legend': [False]}],
                                                            [{'set': ['m11'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['B'], 'mana_symbols': ['B'], 'name': ['Disentomb'], 'cmc': [1.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Return target creature card from your graveyard to your hand.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['1', 'B'], 'mana_symbols': ['B'], 'name': ['Doom Blade'], 'cmc': [2.0], 'card_type': ['Instant'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Destroy target nonblack creature.'], 'legend': [False]}, {'set': ['m11'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['1', 'B'], 'mana_symbols': ['B'], 'name': ['Child of Night'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Vampire'], 'keywords': ['Lifelink'], 'power': ['2'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Lifelink'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Soul Bleed'], 'cmc': [3.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Enchant creature\nAt the beginning of the upkeep of enchanted creature's controller, that player loses 1 life."], 'legend': [False]}, {'set': ['m10'], 'rarity': ['uncommon'], 'color': ['B'], 'mana_cost': ['2', 'B', 'B'], 'mana_symbols': ['B', 'B'], 'name': ['Howling Banshee'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Spirit'], 'keywords': ['Flying'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Flying\nWhen Howling Banshee enters the battlefield, each player loses 3 life.'], 'legend': [False]}],
                                                            [{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['R'], 'mana_symbols': ['R'], 'name': ['Firebreathing'], 'cmc': [1.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Enchant creature\n{R}: Enchanted creature gets +1/+0 until end of turn.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['1', 'R'], 'mana_symbols': ['R'], 'name': ['Goblin Piker'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Warrior'], 'keywords': [], 'watermark': [], 'oracle_text': [''], 'legend': [False]},{'set': ['m10'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['2', 'R'], 'mana_symbols': ['R'], 'name': ['Prodigal Pyromancer'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Wizard'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Prodigal Pyromancer deals 1 damage to any target.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['3', 'R'], 'mana_symbols': ['R'], 'name': ['Lightning Elemental'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Elemental'], 'keywords': ['Haste'], 'power': ['4'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Haste (This creature can attack and {T} as soon as it comes under your control.)'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['4', 'R'], 'mana_symbols': ['R'], 'name': ['Lava Axe'], 'cmc': [5.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Lava Axe deals 5 damage to target player or planeswalker.'], 'legend': [False]}],
                                                            [{'set': ['m11'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['G'], 'mana_symbols': ['G'], 'name': ['Llanowar Elves'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Elf', 'Druid'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Add {G}.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['1', 'G'], 'mana_symbols': ['G'], 'name': ['Deadly Recluse'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Spider'], 'keywords': ['Reach', 'Deathtouch'], 'power': ['1'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Reach (This creature can block creatures with flying.)\nDeathtouch (Any amount of damage this deals to a creature is enough to destroy it.)'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['2', 'G'], 'mana_symbols': ['G'], 'name': ['Cultivate'], 'cmc': [3.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Search your library for up to two basic land cards, reveal those cards, put one onto the battlefield tapped and the other into your hand, then shuffle.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['6', 'G'], 'mana_symbols': ['G'], 'name': ['Howl of the Night Pack'], 'cmc': [7.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Create a 2/2 green Wolf creature token for each Forest you control.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['2', 'G', 'G', 'G'], 'mana_symbols': ['G', 'G', 'G'], 'name': ['Overrun'], 'cmc': [5.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Creatures you control get +3/+3 and gain trample until end of turn.'], 'legend': [False]}] 
                                                           ]
                                                }
                                               ]
                       },
               "summon": {"name": "Summoning Circle",#To do, add ability to "purchase" cards from previous runs
                         "stages":[{"text":"A site of magical power allows you to reconnect to the blind eternities.\n You may use this connection to banish cards from your deck.\n",
                                    "options": ["(Left click) Banish any number of cards, receiving one aether for each card.","(Middle click) Drain energy from the site, gaining 5 aether.","(Right click) Spend two aether to strengthen the connection, allowing you to banish or resummon cards."],
                                    "req_keys":[[],[], ["cost2"]],
                                    "diff": [0, 0, 20] ,
                                    "method": ["trade", "aether", "summon"]}]},
               "rest": {"name": "Campsite",#To do, find something more creative here...
                        "stages":[{"text":"A safe spot to rest",
                                   "options": ["(Left click) Recover some HP"],
                                   "method": ["rest"]}] 
                       },
               "puzzle": {"name": "Puzzle",#To do, find something more creative here...
                          "negparams" : {"card_type": ["Token","Basic"]},
                        "stages":[{"text":"You encounter a puzzling situation. The GM will reveal 3 cards and desribe the situation you encounter.\nDraw a full hand of 7 cards, and with unlimited land plays describe how you approach the situation.",
                                   "options": ["Left click to continue"],
                                   "method": ["puzzle"]}] 
                       }
              }