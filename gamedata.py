from cardutil import select_cards, shortened_card_data

def find_card(name, searchlist = shortened_card_data): #This method is cleaner for coding, but slower at runtime until the search selection function is improved
    a = select_cards(shortened_card_data,1, {"name":[name]})
    return(a[0])

class option():
    def __init__(self, new_stage = 0, method = "battle", text="You are attacked", req_keys=[], reward=[], boss_reqs=[], boss_reward=[], diff = -1):
        self.text = text #Text to display for this option, usually 1 line, potentially add linebreaks here
        self.req_keys = req_keys #List of requirement keys to execute for this option
        self.new_stage = new_stage #int, the new stage the story will go to if this option is chosen (if there is one)
        self.method = method #text, the code corresponding to how this is resolved if chosen
        self.reward = reward #list of cards (usually as dicts themselves) to be added if this is chosen
        self.boss_reward = boss_reward#List of lists of cards, to be given as conditional reward cards
        self.boss_reqs = boss_reqs #for each boss reward, the list of requirements for it to be included (usually storylines)
        self.diff = diff
    
    def evaluate(self):#Move reqs here, since this is only run once per option when entering a storybeat, how to handle boss_reqs?
        return(True)
    def preparetext(self):
        return(self.text)

class storybeat():#Used for single events that don't contain any story progression
    def __init__(self, text = "", name=None, maptext="", storykey=None, fightparams={}, exclusive_params={}, blankparams={}, negparams={"card_type": ["Token","Basic"]}, enemy_params= {}, options=[], lane_dependency = None, card_disp=0, planar = False):
        self.text = text + '\n'
        self.name = name
        self.maptext = maptext
        self.storykey = storykey
        self.fightparams = fightparams
        self.exclusive_params = exclusive_params
        self.blankparams = blankparams
        self.negparams = negparams
        self.enemy_params = enemy_params
        self.options = options
        self.lane_dependency = lane_dependency
        self.card_disp = card_disp
        self.planar = planar
    def run(self, lane_id, storykeys):#Currently this just constructs an appropriate dictionary of values to be handled by the state machine. TO DO: move more functionality here from main
        modified_stage = {'fightparams' : dict(self.fightparams), #These might get modified, so this has to be a copy
                          'exclusive_params' : self.exclusive_params, 'blankparams' : self.blankparams, 'negparams' : self.negparams, 'enemy_params' : self.enemy_params,
                         'card_disp' : self.card_disp, 'text': self.text, 'storykey': self.storykey, 'maptext':self.maptext}
        if len(self.options):
            text = []
            req_keys = []
            new_stage = []
            method = []
            reward = []
            boss_reqs = []
            boss_reward = []
            diff = []
            for opt in self.options:
                if opt.evaluate():
                    text.append(opt.text)
                    req_keys.append(opt.req_keys)
                    new_stage.append(opt.new_stage)
                    method.append(opt.method)
                    reward.append(opt.reward)
                    boss_reqs.append(opt.boss_reqs)
                    boss_reward.append(opt.boss_reward)
                    diff.append(opt.diff)
            modified_stage["diff"] = diff
            modified_stage["options"] = text
            modified_stage["req_keys"] = req_keys
            modified_stage["new_stage"] = new_stage
            modified_stage["method"] = method
            modified_stage["reward"] = reward
            modified_stage["boss_reqs"] = boss_reqs
            modified_stage["boss_reward"] = boss_reward
        if self.lane_dependency is not None:
            if 'color' in modified_stage['fightparams']:
                modified_stage['fightparams']['color'].append(self.lane_dependency[lane_id][:])
            else:
                modified_stage['fightparams']['color'] = self.lane_dependency[lane_id]
        return(modified_stage) #Return just the data needed to run that story at this stage, including all options therein

class storyline():#Contains story beats to form a storyline
    def __init__(self, name=None, maptext="", storykey=None, fightparams=None, exclusive_params=None, blankparams=None, negparams=None, enemy_params= None, stages=[], options=[], lane_dependency = None):
        self.name = name
        self.maptext = maptext
        self.storykey = storykey
        self.fightparams = fightparams
        self.exclusive_params = exclusive_params
        self.blankparams = blankparams
        self.negparams = negparams
        self.enemy_params = enemy_params
        self.stages = stages #List of substages of this beat/storyline, these will themselves be story beats
        self.lane_dependency = lane_dependency
    def build_substages(self, stages):
        for stage in stages:
            if self.storykey is not None:
                stage.storykey = self.storykey
            if self.name is not None:
                stage.name = self.name
            if self.fightparams is not None:
                stage.fightparams = self.fightparams
            if self.exclusive_params is not None:
                stage.exclusive_params = self.exclusive_params
            if self.blankparams is not None:
                stage.blankparams = self.blankparams
            if self.negparams is not None:
                stage.negparams = self.negparams
            if self.enemy_params is not None:
                stage.enemy_params = self.enemy_params
            if self.lane_dependency is not None:
                stage.lane_dependency = self.lane_dependency
            if len(self.maptext):
                stage.maptext = self.maptext
            self.stages.append(stage)
    def run(self, lane_id, storylines):#Select the correct story stage and run that
        if self.storykey is not None:
            if self.storykey in storylines:#If storyline is tracked, read its current progress
                story = storylines[self.storykey]
            else:#If storyline isn't yet tracked, start it at 0
                storylines[self.storykey] = 0
                story = 0
        else:
            story = 0
        stage = self.stages[story].run(lane_id, storylines)
        return(stage) #Return just the data needed to run that story at this stage, including all options therein
lorwyn_lanes = ["R","B","U","W","G"]
lorwyn_lanesl = [["R"],["B"],["U"],["W"],["G"]]
standard_negs = {"card_type": ["Token","Basic"]}   
fight_opt = option(text="(Left Click) Enter combat")
standard_battle = storybeat(name="Fight", maptext="Combat with inhabitants of this plane",text= 'You are attacked by the denizens of this plane.', options=[fight_opt], lane_dependency = lorwyn_lanesl)#Used for single events that don't contain any story progression

def build_faction_story(storykey, name, factionparams, enemy_params, maptext = "",enemycode = '', text = ["",""], fight_text = ["",""], fight_reward = [], betray_text = "", escalate_text = "", hostile_text = "", betray_reward = [], trade_text = [], join_text = [], join_reward = [], final_method = "reward"):
    stages = []
    for i in range (len(text)):#Main story
        options = [option(text=fight_text[i%len(fight_text)], new_stage=-1, reward = fight_reward)]#Betrayal/fight
        options.append(option(new_stage = i, method = "trade", text=trade_text[i%len(trade_text)], req_keys=["enemy"]))#Trade
        if i == len(text) -1:
            options.append(option(new_stage = i,
                           method = final_method, 
                           text=join_text[i%len(join_text)], 
                           req_keys=["enemy", "match"], 
                           reward=join_reward[i%len(join_reward)] ))#final stage/loop
        elif i ==  len(text)-2:
            enemyreq = enemycode + "_l_-2"
            options.append(option(new_stage = i+1, method = "reward", text=join_text[i%len(join_text)], req_keys=[enemyreq, "enemy"], reward=join_reward[i%len(join_reward)]))#Join/progress story
        else:
            options.append(option(new_stage = i+1, method = "reward", text=join_text[i%len(join_text)], req_keys=["enemy", "match"], reward=join_reward[i%len(join_reward)]))#Join/progress story
        stages.append(storybeat( text = text[i%len(text)], options=options, card_disp=3))
    
    #outcome for attacking repeatedly
    stages.append(storybeat(text = hostile_text, options = [option(new_stage = -2, method = "battle", text = "(Left Click) Attack")]))
    
    #Outcome after attacking once
    stages.append(storybeat(text = betray_text,card_disp=0,
                            options = [option(new_stage = -1, method = "battle", text = "(L) Quickly attack, making sure word of your actions doesn't spread."),
                                      option(new_stage = 0, method = "reward", text = "(M) Approach carefully, apologising and hoping to make amends."),
                                      option(new_stage = -2, method = "battle", text = escalate_text, reward = betray_reward)]))
    faction_story = storyline(name=name, maptext=maptext, storykey=storykey, fightparams=factionparams["fight"], 
                              exclusive_params=factionparams["excl"], blankparams=factionparams["blank"], negparams=factionparams["neg"], stages = [], enemy_params= enemy_params)
    faction_story.build_substages(stages)
    return(faction_story)

fae_params = {"fight":{"color": ["B", "U"],"card_type": ["Creature", "Sorcery","Instant","Enchantment"],"subtypes": ["Faerie", "Aura"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg": {"card_type": ["Token","Basic"], "name":["Wydwen, the Biting Gale"]}}
fae_story = build_faction_story(storykey= "fae", name= "Faeries", factionparams= fae_params, enemy_params= {"subtypes":["Merfolk"]},enemycode = 'mer', 
                                text = ["You meet a clique of faeries, travelling from Kinsbaile to their secret home carrying stolen dreamstuffs.",
                                        "You meet a clique of faeries, discussing how best to sneak past the merfolk and steal from something in the depths of the wanderwine river for their queen Oona.\nThey cannot fly beneath the water, and the merrows are too vigilant to be snuck past anyway.", 
                                        "You come across those same faeries, who eagerly ask if you have yet gotten past the merrows.", 
                                        "Returning to the secret glade shown to you by the faeries, you are greeted as a welcome guest.\nThe tiny beings shower you with gifts, and amidst the excited chittering you gather that they successfully journeyed deep below Lorwyn, through the merrow's paths to a cave home to an enourmous slumbering giant.\nHaving stolen its age-long dreams, hopefully without waking it, they are celebrating with a feast."], 
                                fight_text = ["(L) Fight the thieves before they steal from your mind too. (FIGHT)","(L) These faeries have gone too far, it is time to end their treachery. (FIGHT)", "(L) The deal is off, time to end your short little lives.", "(L) There will be no feast today, their time has come. (FIGHT)"],
                                fight_reward = [{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ["Diviner's Wand"], 'cmc': [3.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Wizard', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "Whenever you draw a card, this creature gets +1/+1 and gains flying until end of turn" and "{4}: Draw a card."\nWhenever a Wizard creature enters the battlefield, you may attach Diviner\'s Wand to it.\nEquip {3}'], 'legend': [False]}],
                                betray_text = "To your surprise, you happen upon a faerie glade, with only a few sprites guarding the edges.\nThey haven't yet spotted you, distracted by something powerful they have created from stolen magic.\nIt's possible they know of your previous hostilities with their kind, as words spread fast among these tiny creatures but so too does the forgetting of grievances.\nBefore you can make up your mind, a patrol finds you.", escalate_text = "(R) Attack the glade, stealing the powerful artifact.", 
                                hostile_text = "As you travel, you are beset by a faerie clique, seeking retribution for your previous attacks.", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['4'], 'mana_symbols': [], 'name': ['Deathrender'], 'cmc': [4.0], 'card_type': ['Artifact'], 'subtypes': ['Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature gets +2/+2.\nWhenever equipped creature dies, you may put a creature card from your hand onto the battlefield and attach Deathrender to it.\nEquip {2}'], 'legend': [False]}],
                                trade_text = ["(M) Barter with them, dreams are not the only form of magic they might use. (TRADE)",
                                              "(M) Perhaps some extra magic will help them, in exchange for some secrets of course. (TRADE)",
                                              "(M) Not yet, I'm here to trade.",
                                              "(M) While their gifts are lovely, you'd much rather offer something in return. (TRADE)"], 
                                join_text = ["(R) Ask if they have stolen any interesting dreams of late, and discuss with them the secrets of the other tribes. (JOIN)",
                                            "(R) Offer to help in getting past the merfolk by force. (JOIN)",
                                            "(R) The merrows won't be a problem anymore, you can send someone down to the depths whenever you're ready.",
                                            "(R) Accept their gifts and join the feast, it seems dreamstuff is not a bad substitute for aether. (JOIN)"],
                                join_reward = [[{'set': ['lrw'],'rarity': ['uncommon'],'color': ['U'],'mana_cost': ['3', 'U'],'mana_symbols': ['U'],'name': ['Faerie Harbinger'],'cmc': [4.0],'card_type': ['Creature'],'subtypes': ['Faerie', 'Wizard'],'keywords': ['Flying', 'Flash'],'power': [2], 'toughness': [2],'watermark': [],'oracle_text': ['Flash\nFlying\nWhen Faerie Harbinger enters the battlefield, you may search your library for a Faerie card, reveal it, then shuffle and put that card on top.'],'legend': [False]}],
                                              [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['U'], 'mana_cost': ['2', 'U'], 'mana_symbols': ['U'], 'name': ['Scion of Oona'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Faerie', 'Soldier'], 'keywords': ['Flying', 'Flash'], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ["Flash\nFlying\nOther Faerie creatures you control get +1/+1.\nOther Faeries you control have shroud. (They can't be the targets of spells or abilities.)"], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'U'], 'mana_cost': ['2', 'U', 'B'], 'mana_symbols': ['U', 'B'], 'name': ['Wydwen, the Biting Gale'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Faerie', 'Wizard'], 'keywords': ['Flying', 'Flash'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Flash\nFlying\n{U}{B}, Pay 1 life: Return Wydwen, the Biting Gale to its owner's hand."], 'legend': [True]}, {'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'U'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Secluded Glen'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Secluded Glen enters the battlefield, you may reveal a Faerie card from your hand. If you don't, Secluded Glen enters the battlefield tapped.\n{T}: Add {U} or {B}."], 'legend': [False]}],
                                               []],
                               final_method = "aether")

elf_params = {"fight":{"color": ["B", "G"],"card_type": ["Creature", "Sorcery","Instant","Artifact"],"subtypes": ["Elf"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], "name":["Nath of the Gilt-Leaf"]}}
 

elf_story = build_faction_story(storykey= "elf", name= "Elves",maptext = "Elf faction story", factionparams= elf_params, enemy_params= {"subtypes":["Goblin"]},enemycode = 'bog', 
                                text = ["You journey across Lorwyn, enjoying the beautiful scenery of the plane's permanent summer day.\nAs the sun lowers one morning in the East, you notice an unusual hush -\nthe birds that would normally anounce the occasion falling silent.\nYou hear a footstep behind you, and at once you are surrounded by strange slight figures.\nThough their horns and hooves set them apart from those you've seen on your home plane,\nthe pointed ears and perfect faces are unmistakably Elvish.\nAs they examine and judge you, one of the hunters holds a blade to your neck.",
                                        "In an opening ahead you see a group of elves stood in a circle around a strange shape on the ground.\nAs you approach, you realise the shape is a boggart, arrows stuck in its back.\n'Eyeblights' one says, 'Too ugly to live.'./n'Care to join in on the hunt?'", 
                                        "Travelling through the Gilt-Leaf wood, you find yourself outside a grand elven palace.\n'Ah, if it isn't the new winnower,' says a guard,\n'Care to present your trophies to our liege?'", 
                                        "You return to the Elvish palace of Gilt-Leaf wood."], 
                                fight_text = ["(L)Suspecting you'll be hunted like the goblins of this world, you launch an attack. (FIGHT)",
                                              "(L) Yes, I think I will. (FIGHT)", 
                                              "(L) Attack the settlement, the elves must have great treasures within (FIGHT)", 
                                              "(L) Attack the settlement, the elves must have great treasures within (FIGHT)"],
                                fight_reward = [{'set': ['mor'],'rarity': ['uncommon'],'color': [],'mana_cost': ['2'],'mana_symbols': [],'name': ['Cloak and Dagger'],'cmc': [2.0],'card_type': ['Tribal', 'Artifact'],'subtypes': ['Rogue', 'Equipment'],'keywords': ['Equip'],'power': [0], 'toughness': [0],'watermark': [],'oracle_text': ["Equipped creature gets +2/+0 and has shroud. (It can't be the target of spells or abilities.)\nWhenever a Rogue creature enters the battlefield, you may attach Cloak and Dagger to it.\nEquip {3}"],'legend': [False]}],
                                betray_text = "You have found the palace of Gilt Leaf wood; ho,e of Lorwyn's most powerful elves./nYou're unsure if they know of your previous hostilities with their kind.", 
                                escalate_text = "(R) Assault the palace, stealing a powerful artifact but ensuring all of their kind know of your misdeeds.", 
                                hostile_text = "Having lost access to the Door of Destinies, the elves blame you for their waning power in Lorwyn. As a trumpet warns of your presence, you find yourself surrounded by an Elvish hunting party.", 
                                betray_reward = [{'set': ['mor'],'rarity': ['rare'],'color': [],'mana_cost': ['4'],'mana_symbols': [],'name': ['Door of Destinies'],'cmc': [4.0],'card_type': ['Artifact'],'subtypes': [],'keywords': [],'power': [0], 'toughness': [0],'watermark': [],'oracle_text': ['As Door of Destinies enters the battlefield, choose a creature type.\nWhenever you cast a spell of the chosen type, put a charge counter on Door of Destinies.\nCreatures you control of the chosen type get +1/+1 for each charge counter on Door of Destinies.'],'legend': [False]}],
                                trade_text = ["(M) You carefully offer a small gift, hoping that trade will be more compelling than beauty. (TRADE)",
                                              "(M) Perhaps another day, say do you have need of some hunting supplies? (TRADE)",
                                              "(M) I've not finished my hunt yet, can I trade for some supplies here? (TRADE)",
                                              "(M) Recruit mercenaries (TRADE)"], 
                                join_text = ["(R) Seeing the beauty of you and your companions, the elves judge you worthy of survival, at least for now. (JOIN)",
                                            "(R) Of course, which way did the others go? (JOIN)",
                                            "(R) I would be honored to, please, lead the way (JOIN)",
                                            "(R) Ask for allies to aid you in ridding Lorwyn of eyeblights (JOIN)"],
                                join_reward = [[{'set': ['lrw'],'rarity': ['uncommon'],'color': ['G'],'mana_cost': ['2', 'G'],'mana_symbols': ['G'],'name': ['Elvish Harbinger'],'cmc': [3.0],'card_type': ['Creature'],'subtypes': ['Elf', 'Druid'],'keywords': [],'power': [1], 'toughness': [2],'watermark': [],'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],'legend': [False]}],
                                               [{'set': ['lrw'],'rarity': ['uncommon'],'color': ['G'],'mana_cost': ['2', 'G'],'mana_symbols': ['G'],'name': ['Imperious Perfect'],'cmc': [3.0],'card_type': ['Creature'],'subtypes': ['Elf', 'Warrior'],'keywords': [],'power': [2], 'toughness': [2],'watermark': [],'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'G'], 'mana_cost': ['3', 'B', 'G'], 'mana_symbols': ['B', 'G'], 'name': ['Nath of the Gilt-Leaf'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Elf', 'Warrior'], 'keywords': [],'power': [4], 'toughness': [4], 'watermark': [], 'oracle_text': ['At the beginning of your upkeep, you may have target opponent discard a card at random.\nWhenever an opponent discards a card, you may create a 1/1 green Elf Warrior creature token.'],  'legend': [True]}, 
               {'set': ['lrw'],  'rarity': ['rare'], 'color': ['B', 'G'],  'mana_cost': [],  'mana_symbols': [],  'name': ['Gilt-Leaf Palace'],  'cmc': [0.0],'power': [0], 'toughness': [0],  'card_type': ['Land'],  'subtypes': [],  'keywords': [],  'watermark': [],  'oracle_text': ["As Gilt-Leaf Palace enters the battlefield, you may reveal an Elf card from your hand. If you don't, Gilt-Leaf Palace enters the battlefield tapped.\n{T}: Add {B} or {G}."],  'legend': [False]}],
                                               [{'set': ['lrw'],'rarity': ['uncommon'],'color': ['G'],'mana_cost': ['2', 'G'],'mana_symbols': ['G'],'name': ['Elvish Harbinger'],'cmc': [3.0],'card_type': ['Creature'],'subtypes': ['Elf', 'Druid'],'keywords': [],'power': [1], 'toughness': [2],'watermark': [],'oracle_text': ['When Elvish Harbinger enters the battlefield, you may search your library for an Elf card, reveal it, then shuffle and put that card on top.\n{T}: Add one mana of any color.'],'legend': [False]},
                                               {'set': ['lrw'],'rarity': ['uncommon'],'color': ['G'],'mana_cost': ['2', 'G'],'mana_symbols': ['G'],'name': ['Imperious Perfect'],'cmc': [3.0],'card_type': ['Creature'],'subtypes': ['Elf', 'Warrior'],'keywords': [],'power': [2], 'toughness': [2],'watermark': [],'oracle_text': ['Other Elves you control get +1/+1.\n{G}, {T}: Create a 1/1 green Elf Warrior creature token.'],'legend': [False]}]],
                               final_method = "reward")

bog_params = {"fight":{"color": ["B", "R"],
                  "card_type": ["Creature", "Sorcery","Instant","Artifact"],
                  "subtypes": ["Goblin"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Wort, Boggart Auntie']}}
 

bog_story = build_faction_story(storykey= "bog", name= "Goblins", factionparams= bog_params, enemy_params= {"subtypes":["Kithkin"]},
                                enemycode = 'kth', 
                                text = ["You meet a group of boggarts, the mischeivous kind of goblin that inhabit this world.",
                                        "On the outskirts of Kinsbaile you find a goblin camp.\nAn elder among them explains that the kithkin captured several boggarts that strayed too close to Kinsbaile.\nBut with the big guard towers they've been building, they've got no hope of getting back their friends without burning the towers down.", 
                                        "Coming across the goblin encampment again, they ask if you've burned down the kithkin towers yet.\nKnowing how great the story must be, they invite you in to share your experiences.", 
                                        "You return to the Boggart encampment."], 
                                fight_text = ["(L) (FIGHT)",
                                              "(L) Tell them you'll warn the kithkin, those towers are important. (FIGHT)", 
                                              "(L) Tell them you'll warn the kithkin, those towers are important in their defense against the giants. (FIGHT)", 
                                              "(L) Attack the makeshift settlement. (FIGHT)"],
                                fight_reward = [{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ['Springleaf Drum'], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Tap an untapped creature you control: Add one mana of any color.'], 'legend': [False]}],
                                betray_text = "You come across a Boggart encampment./nGiven how they love to share tales, you're unsure if they will have heard of your previous conflicts with their kind.", 
                                escalate_text = "(R) Attack the makeshift settlement. (FIGHT)", 
                                hostile_text = "You're spotted by a group of goblins, angry at your previous attacks", 
                                betray_reward = [{'set': ['m10'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['5'], 'mana_symbols': [], 'name': ['Coat of Arms'], 'cmc': [5.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Each creature gets +1/+1 for each other creature on the battlefield that shares at least one creature type with it. (For example, if two Goblin Warriors and a Goblin Shaman are on the battlefield, each gets +2/+2.)'], 'legend': [False]}],
                                trade_text = ["(M) The boggarts value new sensations above all else, perhaps your magic is worth some kind of deal. (TRADE)",
                                              "(M) That sounds... fun, but can I interest you in some magic? (TRADE)",
                                              "(M) Not yet, you need to trade for some supplies first. (TRADE)",
                                              "(M) Share your stories, for a price. (TRADE)"], 
                                join_text = ["(R) Tell them about the pranks you got up to on your home plane. (JOIN)",
                                            "(R) Offer to help with dramatic sorcery, perhaps a distraction will help. (JOIN)",
                                            "(R) Regail them with the story of how high the towers burned, and the warmth and smell of it. (JOIN)",
                                            "(R) Listen to the tales of new experiences the goblins have found."],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Boggart Harbinger'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': [], 'power': ['2'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['When Boggart Harbinger enters the battlefield, you may search your library for a Goblin card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Mad Auntie'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Other Goblin creatures you control get +1/+1.\n{T}: Regenerate another target Goblin.'], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'R'], 'mana_cost': [], 'mana_symbols': [], 'name': ["Auntie's Hovel"], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Auntie's Hovel enters the battlefield, you may reveal a Goblin card from your hand. If you don't, Auntie's Hovel enters the battlefield tapped.\n{T}: Add {B} or {R}."], 'legend': [False]}, 
                                                {'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'R'], 'mana_cost': ['2', 'B', 'R'], 'mana_symbols': ['B', 'R'], 'name': ['Wort, Boggart Auntie'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Shaman'], 'keywords': ['Fear'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Fear (This creature can't be blocked except by artifact creatures and/or black creatures.)\nAt the beginning of your upkeep, you may return target Goblin card from your graveyard to your hand."], 'legend': [True]}],
                                               []],
                               final_method = "puzzle")

mer_params = {"fight":{"color": ["U", "W"],
                  "card_type": ["Creature", "Sorcery","Instant"],
                  "subtypes": ["Merfolk"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Wort, Boggart Auntie']}}
 

mer_story = build_faction_story(storykey= "mer", name= "Merfolk", factionparams= mer_params, maptext = "A meeting with the merfolk", enemy_params= {"subtypes":["Treefolk"]},
                                enemycode = 'trf', 
                                text = ["You meet a contingent of merfolk tideshapers travelling along a stream.\nThey are busily using their merrow magic to move the waterway through a nearby grove.",
                                        "On a branch of the wanderwine, you meet a group of tideshapers puzzling over a still point in the water's flow.\n'It's stopped,' says one. 'I told you the roots are too thick to get through without pyromancy.'\n'Well we need to get it out of there, this disruption to our magic will only get worse otherwise!'", 
                                        "", 
                                        ""], 
                                fight_text = ["(L) What do you think you're doing? There are treefolk living in there that'll never survive the flood! (FIGHT)",
                                              "(L) Burning the treefolk out is a step too far, I'll stop you myself. (FIGHT)", "(L) (FIGHT)", "(L)  (FIGHT)"],
                                fight_reward = [{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ["Veteran's Armaments"], 'cmc': [2.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Soldier', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "Whenever this creature attacks or blocks, it gets +1/+1 until end of turn for each attacking creature."\nWhenever a Soldier creature enters the battlefield, you may attach Veteran\'s Armaments to it.\nEquip {2}'], 'legend': [False]}],
                                betray_text = "", 
                                escalate_text = "(R) ", 
                                hostile_text = "", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ['Thorn of Amethyst'], 'cmc': [2.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Noncreature spells cost {1} more to cast.'], 'legend': [False]}],
                                trade_text = ["(M) What learned wizards you are, to so shape a river. Say, could you teach me some of your craft? (TRADE)",
                                              "(M) Are these elemental bursts affecting your magic too? Perhaps we can understand it together. (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)"], 
                                join_text = ["(R) That's not nearly enough water, would you like some help? (JOIN)",
                                            "(R) These magical disturbances are a threat to the whole plane, I'll gladly clear out those treefolk for you (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)"],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['U'], 'mana_cost': ['3', 'U'], 'mana_symbols': ['U'], 'name': ['Merrow Harbinger'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Merfolk', 'Wizard'], 'keywords': ['Landwalk', 'Islandwalk'], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Islandwalk (This creature can't be blocked as long as defending player controls an Island.)\nWhen Merrow Harbinger enters the battlefield, you may search your library for a Merfolk card, reveal it, then shuffle and put that card on top."], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['U'], 'mana_cost': ['2', 'U'], 'mana_symbols': ['U'], 'name': ['Merrow Reejerey'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Merfolk', 'Soldier'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Other Merfolk creatures you control get +1/+1.\nWhenever you cast a Merfolk spell, you may tap or untap target permanent.'], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['U', 'W'], 'mana_cost': ['W', 'U'], 'mana_symbols': ['W', 'U'], 'name': ['Sygg, River Guide'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Merfolk', 'Wizard'], 'keywords': ['Landwalk', 'Islandwalk'], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ["Islandwalk (This creature can't be blocked as long as defending player controls an Island.)\n{1}{W}: Target Merfolk you control gains protection from the color of your choice until end of turn."], 'legend': [True]},
                                               {'set': ['lrw'], 'rarity': ['rare'], 'color': ['U', 'W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Wanderwine Hub'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Wanderwine Hub enters the battlefield, you may reveal a Merfolk card from your hand. If you don't, Wanderwine Hub enters the battlefield tapped.\n{T}: Add {W} or {U}."], 'legend': [False]}],
                                               []],
                               final_method = "reward")
                               

trf_params = {"fight":{"color": ["G","B", "W"],
                  "card_type": ["Creature", "Land", "Instant", "Enchantment"],
                  "subtypes": ["Treefolk", "Forest"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Doran, the Siege Tower']}}
 

trf_story = build_faction_story(storykey= "trf", name= "Treefolk", factionparams= trf_params, maptext = "A living grove of Treefolk", enemy_params= {"subtypes":["Elemental"], "color":["R"]},
                                enemycode = 'ele', 
                                text = ["[placeholder: You meet the Treefolk]",
                                        "[placeholder: You meet the Treefolk]", 
                                        "[placeholder: You meet the Treefolk]", 
                                        "[placeholder: You meet the Treefolk]"], 
                                fight_text = ["(L)  (FIGHT)",
                                              "(L)  (FIGHT)", "(L) (FIGHT)", "(L)  (FIGHT)"],
                                fight_reward = [{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['1'], 'mana_symbols': [], 'name': ["Wanderer's Twig"], 'cmc': [1.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["{1}, Sacrifice Wanderer's Twig: Search your library for a basic land card, reveal it, put it into your hand, then shuffle."], 'legend': [False]}],
                                betray_text = "", 
                                escalate_text = "(R) ", 
                                hostile_text = "", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ["Colfenor's Urn"], 'cmc': [3.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Whenever a creature with toughness 4 or greater is put into your graveyard from the battlefield, you may exile it.\nAt the beginning of the end step, if three or more cards have been exiled with Colfenor's Urn, sacrifice it. If you do, return those cards to the battlefield under their owner's control."], 'legend': [False]}],
                                trade_text = ["(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)"], 
                                join_text = ["(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)"],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['G'], 'mana_symbols': ['G'], 'name': ['Treefolk Harbinger'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Treefolk', 'Druid'], 'keywords': [], 'power': ['0'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['When Treefolk Harbinger enters the battlefield, you may search your library for a Treefolk or Forest card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['G'], 'mana_cost': ['4', 'G'], 'mana_symbols': ['G'], 'name': ['Timber Protector'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Treefolk', 'Warrior'], 'keywords': [], 'power': ['4'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ['Other Treefolk creatures you control get +1/+1.\nOther Treefolk and Forests you control have indestructible.'], 'legend': [False]}],
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['B', 'G', 'W'], 'mana_cost': ['W', 'B', 'G'], 'mana_symbols': ['W', 'B', 'G'], 'name': ['Doran, the Siege Tower'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Treefolk', 'Shaman'], 'keywords': [], 'power': ['0'], 'toughness': ['5'], 'watermark': [], 'oracle_text': ['Each creature assigns combat damage equal to its toughness rather than its power.'], 'legend': [True]},
                                               {'set': ['mor'], 'rarity': ['rare'], 'color': ['B', 'G', 'W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Murmuring Bosk'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': ['Forest'], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["({T}: Add {G}.)\nAs Murmuring Bosk enters the battlefield, you may reveal a Treefolk card from your hand. If you don't, Murmuring Bosk enters the battlefield tapped.\n{T}: Add {W} or {B}. Murmuring Bosk deals 1 damage to you."], 'legend': [False]}],
                                               [{'set': ['m10'], 'rarity': ['common'], 'color': [], 'mana_cost': [], 'mana_symbols': [], 'name': ['Terramorphic Expanse'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{T}, Sacrifice Terramorphic Expanse: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle.'], 'legend': [False]},
                                               {'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['3', 'G', 'G'], 'mana_symbols': ['G', 'G'], 'name': ['Incremental Growth'], 'cmc': [5.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Put a +1/+1 counter on target creature, two +1/+1 counters on another target creature, and three +1/+1 counters on a third target creature.'], 'legend': [False]},
                                               {'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['3', 'G'], 'mana_symbols': ['G'], 'name': ['Woodland Guidance'], 'cmc': [4.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': ['Clash'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Return target card from your graveyard to your hand. Clash with an opponent. If you win, untap all Forests you control. (Each clashing player reveals the top card of their library, then puts that card on the top or bottom. A player wins if their card had a higher mana value.)\nExile Woodland Guidance.'], 'legend': [False]}]],
                               final_method = "reward")
ele_params = {"fight":{"color": ["R"],
                  "card_type": ["Creature", "Land", "Instant", "Enchantment","Sorcery"],
                  "subtypes": ["Elemental"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Horde of Notions']}}
 

ele_story = build_faction_story(storykey= "ele", name= "Flamekin", factionparams= ele_params, maptext = "A meeting with the flamekin", enemy_params= {"subtypes":["Elf"]},
                                enemycode = 'elf', 
                                text = ["[placeholder: You meet the fire elementals known as flamekin]",
                                        "[placeholder: You meet the flamekin of the Brighthearth, they ask you to aid in their attack against the elves]", 
                                        "[placeholder: You meet the Brighthearth]", 
                                        "[placeholder: You meet the Brighthearth]"], 
                                fight_text = ["(L)  (FIGHT)",
                                              "(L)  (FIGHT)", "(L) (FIGHT)", "(L)  (FIGHT)"],
                                fight_reward = [{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ['Thornbite Staff'], 'cmc': [2.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Shaman', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "{2}, {T}: This creature deals 1 damage to any target" and "Whenever a creature dies, untap this creature."\nWhenever a Shaman creature enters the battlefield, you may attach Thornbite Staff to it.\nEquip {4}'], 'legend': [False]}],
                                betray_text = "", 
                                escalate_text = "(R) ", 
                                hostile_text = "", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ['Rings of Brighthearth'], 'cmc': [3.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Whenever you activate an ability, if it isn't a mana ability, you may pay {2}. If you do, copy that ability. You may choose new targets for the copy."], 'legend': [False]}],
                                trade_text = ["(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)"], 
                                join_text = ["(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)"],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['R'], 'mana_symbols': ['R'], 'name': ['Flamekin Harbinger'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Shaman'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['When Flamekin Harbinger enters the battlefield, you may search your library for an Elemental card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],#Harbinger
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['R'], 'mana_cost': ['2', 'R'], 'mana_symbols': ['R'], 'name': ['Incandescent Soulstoke'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Shaman'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Other Elemental creatures you control get +1/+1.\n{1}{R}, {T}: You may put an Elemental creature card from your hand onto the battlefield. That creature gains haste until end of turn. Sacrifice it at the beginning of the next end step.'], 'legend': [False]}],#Lord
                                               [{'set': ['mor'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['3', 'R', 'R'], 'mana_symbols': ['R', 'R'], 'name': ['Pyroclast Consul'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Shaman'], 'keywords': ['Kinship'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Kinship — At the beginning of your upkeep, you may look at the top card of your library. If it shares a creature type with Pyroclast Consul, you may reveal it. If you do, Pyroclast Consul deals 2 damage to each creature.'], 'legend': [False]},
                                               {'set': ['mor'], 'rarity': ['rare'], 'color': ['R'], 'mana_cost': ['3', 'R'], 'mana_symbols': ['R'], 'name': ['Vengeful Firebrand'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Warrior'], 'keywords': [], 'power': ['5'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Vengeful Firebrand has haste as long as a Warrior card is in your graveyard.\n{R}: Vengeful Firebrand gets +1/+0 until end of turn.'], 'legend': [False]}],#Legend, Land
                                               [{'set': ['mor'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['1', 'R'], 'mana_symbols': ['R'], 'name': ['Brighthearth Banneret'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Warrior'], 'keywords': ['Reinforce'], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Elemental spells and Warrior spells you cast cost {1} less to cast.\nReinforce 1—{1}{R} ({1}{R}, Discard this card: Put a +1/+1 counter on target creature.)'], 'legend': [False]},
                                               {'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['3', 'R'], 'mana_symbols': ['R'], 'name': ['Rebellion of the Flamekin'], 'cmc': [4.0], 'card_type': ['Tribal', 'Enchantment'], 'subtypes': ['Elemental'], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Whenever you clash, you may pay {1}. If you do, create a 3/1 red Elemental Shaman creature token. If you won, that token gains haste until end of turn. (This ability triggers after the clash ends.)'], 'legend': [False]}]],
                               final_method = "reward")
ele_stages = list(ele_story.stages[:-2])
ele_stages_final = list(ele_story.stages[-3:])
ele_branch_opt = option(new_stage = 4, method = "reward", text="(ScrDn) Convince them to return to the peaceful ways of the greater elementals", req_keys=["austere_g_1", "incend_l_1"], reward=[{'set': ['lrw'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['1', 'R'], 'mana_symbols': ['R'], 'name': ['Smokebraider'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Shaman'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Add two mana in any combination of colors. Spend this mana only to cast Elemental spells or activate abilities of Elementals.'], 'legend': [False]}], boss_reqs=[], boss_reward=[], diff = -1)

ele_fight_option = option(new_stage = 0, method = "battle", text="(L) Attack", req_keys=[], reward=[{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ['Thornbite Staff'], 'cmc': [2.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Shaman', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature has "{2}, {T}: This creature deals 1 damage to any target" and "Whenever a creature dies, untap this creature."\nWhenever a Shaman creature enters the battlefield, you may attach Thornbite Staff to it.\nEquip {4}'], 'legend': [False]}], boss_reqs=[], boss_reward=[], diff = -1)
ele_trade_option = option(new_stage = 4, method = "trade", text="(M) Trade", req_keys=["austere_g_1", "incend_l_1"], reward=[], boss_reqs=[], boss_reward=[], diff = -1)
ele_progress_option = option(new_stage = 4, method = "reward", text="(R) Explain to them the lessons you have learned from the auroras, that elemental fire encompasses more than the rage of the pyroclasts.", req_keys=["austere_g_1", "cryptic_g_1"], reward=[{'set': ['mor'], 'rarity': ['rare'], 'color': [], 'mana_cost': [], 'mana_symbols': [], 'name': ['Primal Beyond'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Primal Beyond enters the battlefield, you may reveal an Elemental card from your hand. If you don't, Primal Beyond enters the battlefield tapped.\n{T}: Add {C}.\n{T}: Add one mana of any color. Spend this mana only to cast an Elemental spell or activate an ability of an Elemental."], 'legend': [False]}], boss_reqs=[], boss_reward=[], diff = -1)
ele_branch1 = storybeat(text = "You meet again with the elementals.\nThey explain that they have been trying to follow the path of the greater elementals, seeking visions of the mystic horizon.\nBut the steps they must take run seem opposed to the path of flame, calling for reflection and calm.", name=None, maptext="A meeting with the elementals", storykey=None, fightparams=ele_params, exclusive_params={}, blankparams={}, negparams={"card_type": ["Token","Basic"]}, enemy_params= {}, options=[ele_fight_option, ele_trade_option, ele_progress_option], lane_dependency = lorwyn_lanesl, card_disp=0, planar = False)
ele_progress_option2 = option(new_stage = 4, method = "puzzle", text="(R) Bear witness to the glory of Lorwyn's ancient mysteries.", req_keys=["austere_g_2", "cryptic_g_2", "primal_g_1"], reward=[{'set': ['lrw'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['1', 'R'], 'mana_symbols': ['R'], 'name': ['Smokebraider'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Shaman'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Add two mana in any combination of colors. Spend this mana only to cast Elemental spells or activate abilities of Elementals.'], 'legend': [False]},{'set': ['mor'], 'rarity': ['rare'], 'color': [], 'mana_cost': [], 'mana_symbols': [], 'name': ['Primal Beyond'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Primal Beyond enters the battlefield, you may reveal an Elemental card from your hand. If you don't, Primal Beyond enters the battlefield tapped.\n{T}: Add {C}.\n{T}: Add one mana of any color. Spend this mana only to cast an Elemental spell or activate an ability of an Elemental."], 'legend': [False]}], boss_reqs=[], boss_reward=[], diff = -1)
ele_branch2 = storybeat(text = "You meet again with the elementals.\nHaving travelled to the edge of the plane and witnessed the primal beyond, they have restored their connection to the greater elementals.", name=None, maptext="A meeting with the elementals", storykey=None, fightparams=ele_params, exclusive_params={}, blankparams={}, negparams={"card_type": ["Token","Basic"]}, enemy_params= {}, options=[ele_fight_option, ele_trade_option, ele_progress_option2], lane_dependency = lorwyn_lanesl, card_disp=0, planar = False)

ele_stages.append(ele_branch1)
ele_stages.append(ele_stages_final[-2])
ele_stages.append(ele_stages_final[-1])

kth_params = {"fight":{"card_type": ["Creature", "Land", "Instant", "Enchantment", "Artifact"],
                  "subtypes": ["Kithkin"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Gaddock Teeg']}}
 

kth_story = build_faction_story(storykey= "kth", name= "Kithkin", factionparams= kth_params, maptext = "A visit to a Kithkin settlement", enemy_params= {"subtypes":["Giant"]},
                                enemycode = 'gnt', 
                                text = ["[placeholder: You meet the Kithkin]",
                                        "[placeholder: You meet the Kithkin]", 
                                        "[placeholder: You meet the Kithkin]", 
                                        "[placeholder: You meet the Kithkin]"], 
                                fight_text = ["(L)  (FIGHT)",
                                              "(L)  (FIGHT)", "(L) (FIGHT)", "(L)  (FIGHT)"],
                                fight_reward = [{'set': ['lrw'], 'rarity': ['common'], 'color': [], 'mana_cost': ['0'], 'mana_symbols': [], 'name': ['Herbal Poultice'], 'cmc': [0.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{3}, Sacrifice Herbal Poultice: Regenerate target creature.'], 'legend': [False]}],
                                betray_text = "", 
                                escalate_text = "(R) ", 
                                hostile_text = "", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ['Dolmen Gate'], 'cmc': [2.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Prevent all combat damage that would be dealt to attacking creatures you control.'], 'legend': [False]}],
                                trade_text = ["(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)"], 
                                join_text = ["(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (Rest)"],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['W'], 'mana_cost': ['2', 'W'], 'mana_symbols': ['W'], 'name': ['Kithkin Harbinger'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Kithkin', 'Wizard'], 'keywords': [], 'power': ['1'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['When Kithkin Harbinger enters the battlefield, you may search your library for a Kithkin card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],#Harbinger
                                               [{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['W'], 'mana_cost': ['W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Wizened Cenn'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Kithkin', 'Cleric'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Other Kithkin creatures you control get +1/+1.'], 'legend': [False]}],#Lord
                                               [{'set': ['mor'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Rustic Clachan'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': ['Reinforce'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Rustic Clachan enters the battlefield, you may reveal a Kithkin card from your hand. If you don't, Rustic Clachan enters the battlefield tapped.\n{T}: Add {W}.\nReinforce 1—{1}{W} ({1}{W}, Discard this card: Put a +1/+1 counter on target creature.)"], 'legend': [False]},
                                               {'set': ['lrw'], 'rarity': ['rare'], 'color': ['G', 'W'], 'mana_cost': ['G', 'W'], 'mana_symbols': ['G', 'W'], 'name': ['Gaddock Teeg'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Kithkin', 'Advisor'], 'keywords': [], 'power': ['2'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ["Noncreature spells with mana value 4 or greater can't be cast.\nNoncreature spells with {X} in their mana costs can't be cast."], 'legend': [True]}],#Legend, Land
                                               []],
                               final_method = "rest")
                               
gnt_params = {"fight":{"card_type": ["Creature", "Land", "Instant", "Enchantment", "Artifact"],
                  "subtypes": ["Giant"]},
              "excl": {"set": True}, "blank": {"subtypes": True}, "neg":  {"card_type": ["Token","Basic"], 'name': ['Brion Stoutarm']}}
 

gnt_story = build_faction_story(storykey= "gnt", name= "Giant", factionparams= gnt_params, maptext = "A meeting with a giant", enemy_params= {"subtypes":["Faerie"]},
                                enemycode = 'fae', 
                                text = ["[placeholder: You meet a Giant",
                                        "[placeholder: You meet a Giant, who asks you to break the fae enchantments upon a sleeping titan]", 
                                        "[placeholder: You meet a Giant]", 
                                        "[placeholder: You meet a Giant, who tells you a strange tale]"], 
                                fight_text = ["(L)  (FIGHT)",
                                              "(L)  (FIGHT)", "(L) (FIGHT)", "(L)  (FIGHT)"],
                                fight_reward = [{'set': ['mor'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ['Obsidian Battle-Axe'], 'cmc': [3.0], 'card_type': ['Tribal', 'Artifact'], 'subtypes': ['Warrior', 'Equipment'], 'keywords': ['Equip'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Equipped creature gets +2/+1 and has haste.\nWhenever a Warrior creature enters the battlefield, you may attach Obsidian Battle-Axe to it.\nEquip {3}'], 'legend': [False]}],
                                betray_text = "", 
                                escalate_text = "(R) ", 
                                hostile_text = "", 
                                betray_reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['3'], 'mana_symbols': [], 'name': ['Thousand-Year Elixir'], 'cmc': [3.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['You may activate abilities of creatures you control as though those creatures had haste.\n{1}, {T}: Untap target creature.'], 'legend': [False]}],
                                trade_text = ["(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)",
                                              "(M)  (TRADE)"], 
                                join_text = ["(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (JOIN)",
                                            "(R)  (Puzzle)"],
                                join_reward = [[{'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['4', 'R'], 'mana_symbols': ['R'], 'name': ['Giant Harbinger'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Giant', 'Shaman'], 'keywords': [], 'power': ['3'], 'toughness': ['4'], 'watermark': [], 'oracle_text': ['When Giant Harbinger enters the battlefield, you may search your library for a Giant card, reveal it, then shuffle and put that card on top.'], 'legend': [False]}],#Harbinger
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['R'], 'mana_cost': ['5', 'R'], 'mana_symbols': ['R'], 'name': ['Sunrise Sovereign'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Giant', 'Warrior'], 'keywords': [], 'power': ['5'], 'toughness': ['5'], 'watermark': [], 'oracle_text': ['Other Giant creatures you control get +2/+2 and have trample.'], 'legend': [False]}],#Lord
                                               [{'set': ['lrw'], 'rarity': ['rare'], 'color': ['R', 'W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Ancient Amphitheater'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["As Ancient Amphitheater enters the battlefield, you may reveal a Giant card from your hand. If you don't, Ancient Amphitheater enters the battlefield tapped.\n{T}: Add {R} or {W}."], 'legend': [False]},
                                               {'set': ['lrw'], 'rarity': ['rare'], 'color': ['R', 'W'], 'mana_cost': ['2', 'R', 'W'], 'mana_symbols': ['R', 'W'], 'name': ['Brion Stoutarm'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Giant', 'Warrior'], 'keywords': ['Lifelink'], 'power': ['4'], 'toughness': ['4'], 'watermark': [], 'oracle_text': ["Lifelink\n{R}, {T}, Sacrifice another creature: Brion Stoutarm deals damage equal to the sacrificed creature's power to target player or planeswalker."], 'legend': [True]}],#Legend, Land
                                               []],
                               final_method = "puzzle")



def make_aurora_story(colour, self_lines = [], texts=[], land = {}, hero = {}, command = {}, incarnation = {}):
    colour_name = ["White", "Blue", "Black", "Red", "Green"][colour]
    storykeys = ["austere", "cryptic", "profane", "incend", "primal"]
    colour_keys = ["W", "U", "B", "R", "G"]
    storykey = storykeys[colour]
    block_names = [crd["name"][0] for crd in [land, hero, command, incarnation]]
    outputstory = storyline(name=f"Greater Elementals ({colour_name})", maptext="A magical aurora", storykey=storykey, fightparams={"color": [colour_name],"card_type": ["Creature", "Sorcery","Enchantment"],"subtypes": ["Elemental", "Aura"]}, exclusive_params={"set": False}, blankparams={"subtypes": False}, 
    negparams={"name":block_names,"subtypes": ["Soldier", "Warrior", "Incarnation"],"card_type": ["Token","Basic"]}, enemy_params= {"subtypes":["Elemental"]}, stages = list([]))
    outputstory.stages = list([])
    stages = list([])
    for i in range(4):
        opt_texts = ["(L) Allow the strange aurora to pass over yourself and the world, accepting the changes it will bring.",#Solution corresponding to Purity
        "(M) Seeking visions in the strange lights, you begin to divine intention from these manifestations of thought and magic.",#Guile
        "(R) This disturbance will corrupt the beauty of this plane, and only power will withstand it. So power is what you will take.",#Dread
        "(ScrUp) Fight against the magical disturbances, even as it resists your magic.",#Hostility
        "(ScrDn) Allow the energy to suffuse and reinvigorate you as you connect to this land's mana."#Vigor
        ]
        opt_texts[colour] = self_lines[i]
        reqs = [[f"{k}_g_{i}"] for k in storykeys]
        reqs[(colour+2)%5] += ["cost2"]
        methods = ["rest", "puzzle","aether", "battle", "aether"]
        reward = [[[land], [hero], [command, incarnation], [land]][i] for _ in storykeys]
        reward[(colour+2)%5] = [reward[(colour+2)%5][0]]
        reward[(colour+3)%5] = [reward[(colour+3)%5][-1]]
        options = [option(new_stage = min(i+1,3), method = methods[c], text=opt_texts[c], req_keys=reqs[c], reward=reward[c]) for c in range(5)]
        stage1 = storybeat(text = texts[i], options=options)
        stages.append(stage1)
    
    outputstory.build_substages(list(stages))
    return(outputstory)
    
austere = make_aurora_story(0, self_lines = ["(L) Harmonizing your breath with the rhythm of the world, you welcome the aurora, drawing upon its light to suffuse yourself and the land with its otherworldly luminescence.",
"(L) Seeing how the aurora reacts to your thoughts, you try your utmost to remain austere. The purity of your emotion calms the storm, reassuring the wary kithkin.",
"(L) As the overwhelming serenity threatens to sway your resolve to control these events, you stand firm. Instead of resisting, you embrace the raw, unfiltered intensity of white mana, using it as a beacon to guide you through the storm of the aurora.",
"(L) Guided by the memories of previous auroras, you embrace the inevitable change. With a heart full of acceptance, you open yourself up to the aurora's magic, letting it wash over you like a tide carrying away all remnants of fear and doubt."],
texts=["You find yourself in an open field, filled with the beauty of this plane.\nThe magical energy here is strong, and at first you suspect it may be a leyline.\nThe magical energy suddenly swells, splitting into its five components and causing strange lights to dance through the air.\nThe magic begins to distort the landscape, taking strange forms and coalescing as elementals.",
"As you travel through a field near Kinsbaile, an archer travels out to meet you.\nIntroducing herself as Brigid, she asks if you and your magic are a threat to her home.\nSensing your confusion, Brigid's suspicion softens into concern. 'I've seen the lights in the sky, the wild magic spilling over our fields... We need help. Can I trust you to protect Kinsbaile?'\nBefore you can explain that you want to protect Lorwyn, a shimmering in the air alerts you to another surge of magical energy.\nThe suspicious kithkin draws her bow, suspecting you as the cause.",
"Another elemental disturbance descends upon you, stronger than the others.\nYou feel an overwhelming sense of calm that threatens to reshape you and the world you set out to protect.\nThe serenity is overpowering, as you feel your will begin to submit to the changes of the aurora.",
"A familiar sense of calm washes over the landscape, as an aurora aligned with white mana takes form."],
land = {'set': ['lrw'], 'rarity': ['uncommon'], 'color': ['W'], 'mana_cost': [], 'mana_symbols': [], 'name': ['Vivid Meadow'], 'cmc': [0.0], 'card_type': ['Land'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Vivid Meadow enters the battlefield tapped with two charge counters on it.\n{T}: Add {W}.\n{T}, Remove a charge counter from Vivid Meadow: Add one mana of any color.'], 'legend': [False]}, 
hero = {'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['2', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Brigid, Hero of Kinsbaile'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Kithkin', 'Archer'], 'keywords': ['First strike'], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['First strike\n{T}: Brigid, Hero of Kinsbaile deals 2 damage to each attacking or blocking creature target player controls.'], 'legend': [True]}, 
command = {'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['4', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Austere Command'], 'cmc': [6.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [],'oracle_text': ['Choose two —\n• Destroy all artifacts.\n• Destroy all enchantments.\n• Destroy all creatures with mana value 3 or less.\n• Destroy all creatures with mana value 4 or greater.'], 'legend': [False]}, 
incarnation = {'set': ['lrw'], 'rarity': ['rare'], 'color': ['W'], 'mana_cost': ['3', 'W', 'W', 'W'], 'mana_symbols': ['W', 'W', 'W'], 'name': ['Purity'], 'cmc': [6.0], 'card_type': ['Creature'], 'subtypes': ['Elemental', 'Incarnation'], 'keywords': ['Flying'], 'power': ['6'], 'toughness': ['6'], 'watermark': [], 'oracle_text': ["Flying\nIf noncombat damage would be dealt to you, prevent that damage. You gain life equal to the damage prevented this way.\nWhen Purity is put into a graveyard from anywhere, shuffle it into its owner's library."], 'legend': [False]})

cryptic = make_aurora_story(1, self_lines = ["(M) Absorbing the aurora's rhythm, you let it guide your thoughts, seeking answers within its cryptic pattern.",
"(M) As visions begin to assault your thoughts, you shape your mind to the guile and mystery of the aurora in an effort to understand.",
"(M) You open your mind, letting the cryptic patterns seep into your consciousness, daring to understand the incomprehensible.",
"(M) Standing on the river's edge, you wade in and open your senses to the mystery of the aurora's lights."],
texts=["You are standing beside a gently flowing river, whose surface begins reflecting the mesmerizing dance of an aurora overhead.\nThe rippling blues and violets of the lights twist and contort in the flowing water, mirroring the disturbances happening across the plane.\nThe energy here feels cryptic, harboring an intelligence within the chaos.\nPulsations of magic ripple outward, suggesting a hidden pattern beneath the spectacle.",
"As you approach a shade-dappled bend in the Wanderwine, three fae emerge from the spectral gloam cast across the river, their eyes gleaming with suspicion and curiosity.\n'A strange sight, isn't it?' one of them asks, gesturing to an aurora forming overhead.\n'Who might be behind this?' they puzzle.\n'You look almost as lost as we are. Let's unravel this mystery together, shall we?' The fairies invite you to collaborate, their demeanor brimming with a playful sense of guile.",
"A concentrated blast of magical energy manifests, the aurora's waves vibrating with an intensity you've not encountered before.\nIn the shimmering cascades of light, you glimpse flashes of knowledge, cryptic messages flickering past too quickly to fully grasp.\n'Surely not' whispers Veesa of the clique. 'This could never be her plan'\n'The horned one,' mutters Iliona, 'Or the puppet' responds Endry.\nAs the world around you morphs in response to the energy's whisperings, the faes' words echo in your thoughts once again.",
"Returning to the Wanderwine, you watch as the river's surface reflects a different scene now.\nThe aurora carries with it not only the energy of transformation but the promise of untold secrets.\nEmbracing the river’s memory, you let the enigmatic lights guide you, ready to unveil the mysteries hidden within the  dance of the aurora."],
land = find_card("Vivid Creek"), 
hero = find_card("Vendilion Clique"), 
command = find_card("Cryptic Command"), 
incarnation = find_card("Guile"))

profane = make_aurora_story(2, self_lines = ["(R) As the aurora casts its eerie shadows you reach out, opening yourself to the darker power pulsating within.",
"(R) The elf's promise of power resonates with you, and you reach out to claim it together.",
"(R) You embrace the power, commanding your own fear with the profane magic.",
"(R) You reach out once more, drawing power from the aurora and its profanity."],
texts=["The sky above you grows dark, swirling patterns of black and purple weaving into a foreboding portrait.\nThe land around you grows dark, the once vibrant colors replaced by shades of violet.\nA feeling of hopelessness seeps into the world, as though a great malevolence were just beyond the horizon.\nYet at the same time, the surge of magic seems to invite you to tap into its immense and profane power.",
"In the heart of the eerily quiet woodland, a figure emerges from the shadows.\nIntroducing herself as Maralen, she asks if you too can feel the power of what is to come.\n'It offers power, to those who'll take it.'\n'Power enough to do something truly dreadful.'\nAfraid as you are of this force, there is a certain allure in her words.",
"As the aurora intensifies, the world around you takes on an ever more fearsome aspect.\nShadows stretch and distort, taking on forms that make your heart pound, and the sky darkens as if the sun itself hides in fear of what's to come.\nA vision of a world shrouded in perpetual darkness overwhelms you, and you see Maralen grinning at the possibility.\n'Now's your moment,' she whispers.",
"The haunting spectacle of the aurora returns, darkening the sun as the air grows thick with magic.\nA premonition of the coming darkness wraps around your heart.\nAt first you found these visions terrifying, then exhilerating.\nNow the feeling is rich and intoxicating as you aniticipate the power it will grant you."],
land = find_card("Vivid Marsh"), 
hero = find_card("Maralen of the Mornsong"), 
command = find_card("Profane Command"), 
incarnation = find_card("Dread"))

incend = make_aurora_story(3, self_lines = ["(ScrUp) You fight against the aurora's influence, lest these visions become reality.",
"(ScrUp) Moved by her words, you feel your resolve ignite to fight against this omen.",
"(ScrUp) We must resist this tyranny as any other! No magic nor hatred can drive us to such an end.",
"(ScrUp) Grit your teeth and fight again against these horrors."],
texts=["Making your way through the mountains, you find yourself overlooking a forge of the Brighthearth.\nShifting amber lights surround you, distorting your vision of the flamekins' work.\nWhat you thought were tools take on the appearance of weapons, and great engines of war.\nYou see the future as described by the pyroclasts, a revolution of fire and metal overtaking the world.",
"Upon a mountain path you meet the flamekin Ashling.\nShe tells you of her journey to understand the greater elementals and the path of flame.\nSomething grows unstable in the world, pulling us towards hostility and violence far beyond our elvish oppressors.\nAn aurora forms around her words, sharing with you her vision of violent uprising and technological brutality.",
"At once an aurora bursts forth, blinding you with visions of a world overcome by progress.\nThe great work of the Brighthearth, fueled by a passion not of Lorwyn that burns like a furnace.\nIron clad suffering outstrips that dreamt of by the cruelest elf.\nThe sight fills you not with fear, but an undeniable sense of incendiary rebellion.",
"You see the chromatic fire of the aurora dance through the sky once more.\nRebellious passion fills you as you consider Lorwyn's grim and violent future."],
land = find_card("Vivid Crag"), 
hero = find_card("Ashling the Pilgrim"), 
command = find_card("Incendiary Command"), 
incarnation = find_card("Hostility"))

primal = make_aurora_story(4, self_lines = ["(ScrDn) Attune yourself to the land and its lifeforce, while letting the aurora amplify your magic to reinvigorate you both.",
"(ScrDn) Aid in his quest, letting the surge of magic reinvigorate you and the scorched land.",
"(ScrDn) Channeling the vigor of green mana, you seek out growth and recovery amidst the rot.",
"(ScrDn) You tap into the pulsating energy of the life around you, growing as it does."],
texts=["As you traverse the sunlit groves of Lorwyn, your heart sinks at the sight of once-lush treefolk groves now ashen and wilting.\nUnstable elementals have wrought havoc on the land, yet you can sense the profound resilience of nature.\nThe primal vigor of life strives to heal, and to regrow even before your eyes.\nAnother aurora begins to take form, threatening to reignite the fires or to spur regrowth.",
"You come across an elf named Rhys, seemingly in mourning amongst a ruined grove.\nHe tells you of his past as a winnower, before being exiled after losing control of his magic.\nA growing aurora shows you his past, how his use of poison magic to corrupt his enemies' life force.\nHe seeks now to return that living magic to the plane, hoping that with the aurora he might aid the regrowth of such places as this.",
"A powerful aurora spreads across the sky, casting all in a hue as verdant as it is sickly. You see at once two worlds:\nThe plane you now know, wounded but full of light, grows vital amidst the magic\n.But the other world is full of darkness, with life becoming twisted and venomous as it feeds upon itself.\nEach world grows from the other, in a cycle of death and rebirth that sinks now towards decay.",
"As the aurora dances across the sky once more, you return to the ravaged groves.\nYou are heartened to find shoots of new growth pushing through the charred bark.\nDespite the reminder of past destruction, life endures."],
land = find_card("Vivid Grove"), 
hero = find_card("Rhys the Exiled"), 
command = find_card("Primal Command"), 
incarnation = find_card("Vigor"))

mirror_story = storyline(name="Magic Mirror", maptext="An Enchanted Mirror", storykey="twinning", fightparams={"card_type": ["Creature"],"subtypes": ["Spirit", "Wraith", "Illusion", "Shade", "Shapeshifter"]},exclusive_params={"set": False}, blankparams={"subtypes": True}, negparams={"card_type": ["Token","Basic"]}, enemy_params= {"subtypes":["Vampire"]}, stages = [])

mirror_peaceful = option(new_stage = 0, method = "rest", text="(L) Raise a hand in response. If your reflection is a friend, this place could be a welcome respite.", req_keys=["enemy", "match"])
mirror_trade = option(new_stage = 0, method = "m_trade", text="(M) Explore the power of the mirror, perhaps it can reflect your magic as well.", req_keys=["enemy"])
mirror_take = option(new_stage = 1, method = "m_battle", text="(R) Expend 2 aether to control the mirror by force, stealing the powerful artifact.", req_keys=["cost2"], reward = [{'set': ['lrw'], 'rarity': ['rare'], 'color': [], 'mana_cost': ['4'], 'mana_symbols': [], 'name': ['Twinning Glass'], 'cmc': [4.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['{1}, {T}: You may cast a spell from your hand without paying its mana cost if it has the same name as a spell that was cast this turn.'], 'legend': [False]}])
mirror_destroy = option(new_stage = -1, method = "m_battle", text="(ScrUp) Smash the mirror before something worse is unleashed.", req_keys=["cost-3"])
mirror_commune = option(new_stage = 1, method = "aether", text="(ScrDn) Commune with your reflection, perhaps your power will be reflected here too.", req_keys=["match"])
mirror_start = storybeat(text = "You see a figure approaching, matching your movements and pace.\nCautious, you ready a few spells to protect yourself in case of a fight.\nAs you get closer, you realise it is not a stranger, but your own reflection.\nA mirror, made of polished silver and with an ornate frame, sits wedged between two rocks and overgrown with vegetation.\nYour own reflection, hazy and indistinct, begins to raise a hand.", options=[mirror_peaceful,mirror_trade,mirror_take, mirror_destroy, mirror_commune], card_disp=3)

mirror_peaceful2 = option(new_stage = 1, method = "rest", text="(L) The area seems safe enough to rest in now you're sure the mirror is not a threat.")
mirror_trade2 = option(new_stage = 1, method = "m_trade", text="(M) The mirror replicated the spirit of the subject, perhaps you can recreate this yourself", req_keys=["match"])
mirror_puzzle = option(new_stage = 1, method = "m_puzzle", text="(R) Commune with the spirits in the mirror, divining their intentions.", req_keys=["enemy"])
mirror_return = storybeat(text = "You return to the spot where you once found the enchanted mirror.", options=[mirror_peaceful2,mirror_trade2,mirror_puzzle], card_disp=3)
mirror_gone = storybeat(text = "You return to the spot where the enchanted mirror once sat.", options=[mirror_peaceful2], card_disp=0)
mirror_story.build_substages([mirror_start,mirror_return,mirror_gone])

omn1fight = option(new_stage = 1, text="(L) Defend Lorwyn", req_keys=[], reward=[find_card("Omnath, Locus of Mana")], boss_reqs=[["cryptic_l_1"], ["incend_l_1"], ["primal_l_1"]], boss_reward=[[find_card("Guile")],[find_card("Hostility")],[find_card("Vigor")]], diff = 20)
omn1ele = option(new_stage = 1, text="(R) As the flamekin seek peace, many elementals leave your foe's cause", req_keys=[], reward=[find_card("Omnath, Locus of Mana")], boss_reqs=[["incend_l_1"], ["primal_l_1"]], boss_reward=[[find_card("Hostility")],[find_card("Vigor")]], diff = 15)
omn1 = storybeat(text = "", name="Elementalist", maptext="An enemy elementalist", storykey="omn", fightparams={"card_type": ["Creature", "Enchantment"],"color": ["U","R","G"], "subtypes":["Elemental"]}, 
exclusive_params={"set": False}, blankparams={"subtypes": False}, negparams={"card_type": ["Token","Basic"]},options=[omn1fight,omn1ele], lane_dependency = None, card_disp=0, planar = True)
omn2fight = option(new_stage = 1, text="(Left click to continue)", req_keys=[], reward=[find_card("Pyrrhic Revival")], boss_reqs=[["austere_l_1"], ["incend_l_1"], ["profane_l_1"]], boss_reward=[[find_card("Purity")],[find_card("Hostility")],[find_card("Dread")]], diff = 20)
omn2ele = option(new_stage = 1, text="As the flamekin seek peace, many elementals leave your foe's cause", req_keys=[], reward=[find_card("Pyrrhic Revival")], boss_reqs=[["incend_l_1"], ["profane_l_1"]], boss_reward=[[find_card("Hostility")],[find_card("Dread")]], diff = 15)
omn2 = storybeat(text = "", name="Elementalist", maptext="An enemy elementalist", storykey="omn", fightparams={"card_type": ["Creature", "Enchantment"],"color": ["W","R","B"], "subtypes":["Elemental"]}, 
exclusive_params={"set": False}, blankparams={"subtypes": False}, negparams={"card_type": ["Token","Basic"]},options=[omn2fight,omn2ele], lane_dependency = None, card_disp=0, planar = True)
omnath = storyline(name="Elementalist", maptext="An enemy elementalist.", storykey="omn", fightparams=None, exclusive_params=None, blankparams=None, negparams=None, enemy_params= None, stages=[omn1, omn2])

worlds = {#Information per world to use in building and navigating maps, including character and story information. Exact implementation tbd, but should be robust and accessible for many different arrangements of worlds
    "Place": {#Placeholder world
        # ...
        "events": {#Types of events in this world. Should be the same for all worlds, but doesn't have to be.
            "battle": standard_battle,#{#Although this functions like any other event and can involve storylines or choices if you want, the intention is to use it for basic per-lane events, equivalent to world events but with one event that has internal colour splits
            "faction_event": {"fae":fae_story,
                              "bog":bog_story,
                              "elv":elf_story,
                              "mer":mer_story,
                              "ele":ele_story,
                              "trf":trf_story,
                              "kth":kth_story,
                              "gnt":gnt_story
                            # Add more factions here
                             },
            "story_event": {#The key difference with this type of event is that they should be enforced to occur a set number of times in a map. Other than that, they don't really function any differently than regular faction events
                "austere":austere, "cryptic":cryptic, "profane":profane,"incend":incend,"primal":primal,
                            "phiW":{"name": "Phyrexian Invasion (W)",
                                     "fightparams" : {"color": ["W"],
                                                      "watermark": ["phyrexian"], 'set' : ['mom','nph','som']},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"watermark": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "stages": [{'text':
                                                 "Placeholder planar invasion.\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Fight"],'method': ["battle"] #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                               }]},
                            "phiU":{"name": "Phyrexian Invasion (U)",
                                     "fightparams" : {"color": ["U"],
                                                      "watermark": ["phyrexian"], 'set' : ['mom','nph','som']},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"watermark": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "stages": [{'text':
                                                 "Placeholder planar invasion.\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Fight"],'method': ["battle"] #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                               }]},
                            "phiB":{"name": "Phyrexian Invasion (B)",
                                     "fightparams" : {"color": ["B"],
                                                      "watermark": ["phyrexian"], 'set' : ['mom','nph','som']},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"watermark": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "stages": [{'text':
                                                 "Placeholder planar invasion.\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Fight"],'method': ["battle"] #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                               }]},
                            "phiR":{"name": "Phyrexian Invasion (R)",
                                     "fightparams" : {"color": ["R"],
                                                      "watermark": ["phyrexian"], 'set' : ['mom','nph','som']},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"watermark": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "stages": [{'text':
                                                 "Placeholder planar invasion.\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Fight"],'method': ["battle"] #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                               }]},
                            "phiG":{"name": "Phyrexian Invasion (G)",
                                     "fightparams" : {"color": ["G"],
                                                      "watermark": ["phyrexian"], 'set' : ['mom','nph','som']},#Values that are desired, such that at least one should be present if a card has any values for that parameter
                                     "exclusive_params" : {"set": False},#Whether the parameter list is exclusive, ie any values outside of that list are disallowed if exclusive_params[params]==True
                                     "blankparams" : {"watermark": True}, #Dict of whether blank values are disallowed, eg colorless cards or no subtypes
                                     "stages": [{'text':
                                                 "Placeholder planar invasion.\n", #Stage 0, first experience of the aurora (in white, at least)
                                                 'options': ["(L) Fight"],'method': ["battle"] #possible methods, corresponding to left click, middle, and right click (1,2,3)
                                               }]}
                            # Add more stories here
                           },
            "boss":{ "omnath": omnath
            },
            "world_event": {#Other world events, which may be adjacent to the main storyline but aren't required for completion.
                "mirror":mirror_story
                            # Add more story types here
                           }
        },
        "evnt_type":["battle",
        "story_event","story_event","story_event","story_event",
        "base","base",
        "faction_event",
        "world_event"],#Relative weighting of event type, placeholder world is mostly factions as they are finished first for testing
        "lane_id":lorwyn_lanes,#Meaning of each lane in this world's minimap, usually based on colour. Will be used to key other features from this data
        "param":{"W":["detail"],"U":["detail"],"B":["detail"],"R":["detail"],"G":["detail"]}, #General form of how lane ids will give other details to be used for events
        "faction_event":{"W":["mer", "mer","gnt", "gnt","gnt",
                        "gnt","kth", "kth","kth", "kth",
                        "kth", "kth","kth", "kth","kth",
                        "kth","ele", "trf", "trf",],
                   "U":["fae", "fae","fae", "fae","fae",
                        "fae","fae", "fae","mer", "mer",
                        "mer", "mer","mer", "mer","mer",
                        "mer","mer", "mer","ele"],
                   "B":["elv", "elv","elv", "elv","fae",
                        "fae","fae", "fae","bog", "bog",
                        "bog", "bog","bog", "bog","bog",
                        "bog","ele", "trf", "trf",],
                   "R":["bog", "bog","bog", "bog","gnt",
                        "gnt","gnt", "gnt","gnt", "gnt",
                        "gnt", "ele","ele", "ele","ele",
                        "ele","ele", "ele","ele"],
                   "G":["elv", "elv","elv", "elv","elv",
                        "elv","elv", "elv","kth", "kth",
                        "ele", "trf", "trf","trf",
                        "trf","trf", "trf","trf", "trf",]},
        "base":{"W":["rest", "puzzle"],"U":["puzzle"],"B":["summon", "puzzle"],"R":["puzzle"],"G":["rest", "summon"]},
        "boss":{"W":["omnath"],"U":["omnath"],"B":["omnath", "omnath"],"R":["omnath"],"G":["omnath"]},
        "story_event":{"W":["austere", "austere"],"U":["cryptic"],"B":["profane"],"R":["incend"],"G":["primal"]}, #,"U":["cryptic"],"B":["profane"],"R":["incend"],"G":["primal"]}, 
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
default_decks = [[{'set': ['m10'],
 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['W'], 'mana_symbols': ['W'], 'name': ['Soul Warden'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Cleric'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Whenever another creature enters the battlefield, you gain 1 life.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['uncommon'], 'color': [], 'mana_cost': ['2'], 'mana_symbols': [], 'name': ["Lifelink"], 'cmc': [2.0], 'card_type': ['Artifact'], 'subtypes': [], 'keywords': [], 'watermark': [], 'oracle_text': ['Whenever a player casts a white spell, you may gain 1 life.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['2', 'W'], 'mana_symbols': ['W'], 'name': ['Griffin Sentinel'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Griffin'], 'keywords': ['Flying', 'Vigilance'], 'power': ['1'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ["Flying\nVigilance (Attacking doesn't cause this creature to tap.)"], 'legend': [False]}, {'set': ['m11'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['2', 'W', 'W'], 'mana_symbols': ['W', 'W'], 'name': ['Cloud Crusader'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Knight'], 'keywords': ['Flying', 'First strike'], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Flying\nFirst strike (This creature deals combat damage before creatures without first strike.)'], 'legend': [False]}, {'set': ['lrw'], 'rarity': ['common'], 'color': ['W'], 'mana_cost': ['4', 'W'], 'mana_symbols': ['W'], 'name': ['Battle Mastery'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Cleric'], 'keywords': [], 'power': ['2'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['When Tireless Missionaries enters the battlefield, you gain 3 life.'], 'legend': [False]}],
                                                            [{'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['U'], 'mana_symbols': ['U'], 'name': ['Zephyr Sprite'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Faerie'], 'keywords': ['Flying'], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Flying'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['1', 'U'], 'mana_symbols': ['U'], 'name': ['Convincing Mirage'], 'cmc': [2.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Enchant land\nAs Convincing Mirage enters the battlefield, choose a basic land type.\nEnchanted land is the chosen type.'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['2', 'U'], 'mana_symbols': ['U'], 'name': ['Scroll Thief'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Merfolk', 'Rogue'], 'keywords': [], 'power': ['1'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Whenever Scroll Thief deals combat damage to a player, draw a card.'], 'legend': [False]},{'set': ['m11'], 'rarity': ['uncommon'], 'color': ['U'], 'mana_cost': ['2', 'U', 'U'], 'mana_symbols': ['U', 'U'], 'name': ['Sleep'], 'cmc': [4.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Tap all creatures target player controls. Those creatures don't untap during that player's next untap step."], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['U'], 'mana_cost': ['4', 'U'], 'mana_symbols': ['U'], 'name': ['Serpent of the Endless Sea'], 'cmc': [5.0], 'card_type': ['Creature'], 'subtypes': ['Serpent'], 'keywords': [], 'power': ['*'], 'toughness': ['*'], 'watermark': [], 'oracle_text': ["Serpent of the Endless Sea's power and toughness are each equal to the number of Islands you control.\nSerpent of the Endless Sea can't attack unless defending player controls an Island."], 'legend': [False]}],
                                                            [{'set': ['m11'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['B'], 'mana_symbols': ['B'], 'name': ['Disentomb'], 'cmc': [1.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Return target creature card from your graveyard to your hand.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['1', 'B'], 'mana_symbols': ['B'], 'name': ['Doom Blade'], 'cmc': [2.0], 'card_type': ['Instant'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Destroy target nonblack creature.'], 'legend': [False]}, {'set': ['m11'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['1', 'B'], 'mana_symbols': ['B'], 'name': ['Child of Night'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Vampire'], 'keywords': ['Lifelink'], 'power': ['2'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Lifelink'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['B'], 'mana_cost': ['2', 'B'], 'mana_symbols': ['B'], 'name': ['Soul Bleed'], 'cmc': [3.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ["Enchant creature\nAt the beginning of the upkeep of enchanted creature's controller, that player loses 1 life."], 'legend': [False]}, {'set': ['m10'], 'rarity': ['uncommon'], 'color': ['B'], 'mana_cost': ['2', 'B', 'B'], 'mana_symbols': ['B', 'B'], 'name': ['Howling Banshee'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Spirit'], 'keywords': ['Flying'], 'power': ['3'], 'toughness': ['3'], 'watermark': [], 'oracle_text': ['Flying\nWhen Howling Banshee enters the battlefield, each player loses 3 life.'], 'legend': [False]}],
                                                            [{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['R'], 'mana_symbols': ['R'], 'name': ['Firebreathing'], 'cmc': [1.0], 'card_type': ['Enchantment'], 'subtypes': ['Aura'], 'keywords': ['Enchant'], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Enchant creature\n{R}: Enchanted creature gets +1/+0 until end of turn.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['1', 'R'], 'mana_symbols': ['R'], 'name': ['Goblin Piker'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Goblin', 'Warrior'], 'keywords': [], 'watermark': [], 'oracle_text': [''], 'legend': [False]},{'set': ['m10'], 'rarity': ['uncommon'], 'color': ['R'], 'mana_cost': ['2', 'R'], 'mana_symbols': ['R'], 'name': ['Prodigal Pyromancer'], 'cmc': [3.0], 'card_type': ['Creature'], 'subtypes': ['Human', 'Wizard'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Prodigal Pyromancer deals 1 damage to any target.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['3', 'R'], 'mana_symbols': ['R'], 'name': ['Lightning Elemental'], 'cmc': [4.0], 'card_type': ['Creature'], 'subtypes': ['Elemental'], 'keywords': ['Haste'], 'power': ['4'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['Haste (This creature can attack and {T} as soon as it comes under your control.)'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['R'], 'mana_cost': ['4', 'R'], 'mana_symbols': ['R'], 'name': ['Lava Axe'], 'cmc': [5.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Lava Axe deals 5 damage to target player or planeswalker.'], 'legend': [False]}],
                                                            [{'set': ['m11'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['G'], 'mana_symbols': ['G'], 'name': ['Llanowar Elves'], 'cmc': [1.0], 'card_type': ['Creature'], 'subtypes': ['Elf', 'Druid'], 'keywords': [], 'power': ['1'], 'toughness': ['1'], 'watermark': [], 'oracle_text': ['{T}: Add {G}.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['1', 'G'], 'mana_symbols': ['G'], 'name': ['Deadly Recluse'], 'cmc': [2.0], 'card_type': ['Creature'], 'subtypes': ['Spider'], 'keywords': ['Reach', 'Deathtouch'], 'power': ['1'], 'toughness': ['2'], 'watermark': [], 'oracle_text': ['Reach (This creature can block creatures with flying.)\nDeathtouch (Any amount of damage this deals to a creature is enough to destroy it.)'], 'legend': [False]},{'set': ['m11'], 'rarity': ['common'], 'color': ['G'], 'mana_cost': ['2', 'G'], 'mana_symbols': ['G'], 'name': ['Cultivate'], 'cmc': [3.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Search your library for up to two basic land cards, reveal those cards, put one onto the battlefield tapped and the other into your hand, then shuffle.'], 'legend': [False]},{'set': ['m10'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['6', 'G'], 'mana_symbols': ['G'], 'name': ['Howl of the Night Pack'], 'cmc': [7.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Create a 2/2 green Wolf creature token for each Forest you control.'], 'legend': [False]}, {'set': ['m10'], 'rarity': ['uncommon'], 'color': ['G'], 'mana_cost': ['2', 'G', 'G', 'G'], 'mana_symbols': ['G', 'G', 'G'], 'name': ['Overrun'], 'cmc': [5.0], 'card_type': ['Sorcery'], 'subtypes': [], 'keywords': [], 'power': [0], 'toughness': [0], 'watermark': [], 'oracle_text': ['Creatures you control get +3/+3 and gain trample until end of turn.'], 'legend': [False]}] 
                                                           ]
startw = option(method = "reward", text="(L) White", reward=default_decks[0])
startu = option(method = "reward", text="(M) Blue", reward=default_decks[1])
startb = option(method = "reward", text="(R) Black", reward=default_decks[2])
startr = option(method = "reward", text="(ScrUp) Red", reward=default_decks[3])
startg = option(method = "reward", text="(ScrDwn) Green", reward=default_decks[4])


start_event = storybeat(text = "Choose a starting deck:", name="Start", maptext="Start", options=[startw, startu, startb, startr, startg])
summon = storybeat(text = "A site of magical power allows you to reconnect to the blind eternities.\n You may use this connection to banish cards from your deck.", name = "Summoning Circle", options = [option(method = "trade", diff = 0,text = "(Left click) Banish any number of cards, receiving one aether for each card."), option(method = "aether", diff = 0, text = "(Middle click) Drain energy from the site, gaining 5 aether."), option(method = "summon", req_keys = ["cost2"], diff = 20,text = "(Right click) Spend two aether to strengthen the connection, allowing you to banish or resummon cards.")] )
rest = storybeat(text = "A safe spot to rest", name = "Campsite", options = [option(method = "rest", text = "(Left click) Recover some HP")])
puzzle = storybeat(text = "You encounter a puzzling situation. The GM will reveal 3 cards and desribe the situation you encounter.\nDraw a full hand of 7 cards, and with unlimited land plays describe how you approach the situation.", name = "Puzzle", options = [option(method = "puzzle", text = "(Left click to continue)")])

#Base events: event types that are used in every world and should never change (though their proportions can change)


base_events = {"start":start_event,
               "summon": summon,
               "rest": rest,
               "puzzle": puzzle
              }
