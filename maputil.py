import random
import json
import numpy as np
import pygame
import os
#import math

from globals import GlobalVariables
from gamedata import worlds, planeswalkers, base_events

global_vars = GlobalVariables()

def check_linkage(l, l2 = None, conn = []): #Check whether a given set of connections would ensure, for every node that is present in each of the two layers, if it connects at least once to the other layer
    if l2 is None:
        l2 = l[1]
        l1 = l[0]
    else:
        l1 = l
    n = len(l1)
    complete = True
    for i in l1:
        if not np.max(conn[i],axis=-1):
            complete = False
    if complete:
        for i in l2:
            if not np.max(conn[:,i]):
                complete = False
    return(complete)
def linkage(l,l2 = None, rigid = 0.5, fill = 0.1): #Take two lists of nodes (binary lists, indicating presence or absence at each position) and output an array indicating connections to make sure all present nodes can be reached from at least one location on the other step, without any connections crossing
    if l2 is None:
        l2 = l[1]
        l1 = l[0]
    else:
        l1 = l
    n = len(l1)
    exL = [[i for i in range(n) if l1[i]],[i for i in range(n) if l2[i]]]
    conn = np.zeros([n,n],dtype = np.uint8)
    conn[exL[0][0],exL[1][0]]=1
    conn[exL[0][-1],exL[1][-1]]=1
    for i in range(n):
        if l1[i] and l2[i] and random.random() < rigid:
            conn[i,i] = 1
    complete = check_linkage(exL,None,conn)
    i = 0
    while i < 9999 and not complete: #If it can't find a solution after 9999 tries, it's probably stuck in a loop, and a slightly flawed map is better than getting stuck
        i += 1
        suggestion1 = random.choice(exL[0])
        suggestion2 = random.choice(exL[1])
        if not conn[suggestion1,suggestion2]: #Check whether suggested connection, if it doesn't already exist, would cross any others
            #Crossing connections defined as going from before on one layer to after on the other. Of course if one node is the first possible, nothing can be before it, and if it's last nothing can be later, so we don't check those
            if suggestion2 == n-1 or suggestion1 == 0: 
                intsa = 0
            else:
                intsa = np.max(conn[:suggestion1,suggestion2+1:])
            if suggestion1 == n-1 or suggestion2 == 0:
                intsb = 0
            else:
                intsb = np.max(conn[suggestion1+1:,:suggestion2])
            intersect = max(intsa,intsb)
            if not intersect:
                conn[suggestion1,suggestion2] = 1
        
        complete = check_linkage(exL,None,conn)
        if random.random() > fill:
            complete = False
    return(conn)
    
def generate_random_node(world_name, lane_idx, exists = True,is_start=False, is_end = False):
    if is_start:
        return {"event": "start", "data" : base_events["start"],"details": "Beginning of your journey on this world."}

    world = worlds[world_name]
    event_type_weights = world["evnt_type"]
    event_type = random.choice(event_type_weights)#Kind of event, eg faction or battle or story
    if is_end:
        event_type = "boss"
    lane = world["lane_id"][lane_idx] #Description of that lane, usually colour
    if event_type == "planeswalker":#Handled separately as there is no world-specific data per planeswalker
        event_key = random.choice(world[event_type][lane])#There is, however, a list of the planeswalkers found there
        data = planeswalkers[event_key] #full description of that planeswalker
        details = "A fellow planeswalker"
    elif event_type == "base":
        event_key = random.choice(world[event_type][lane])
        data = base_events[event_key] #full description of that planeswalker
        details = "A standard event"
    else:
        event = world["events"][event_type] #full description of that event type, eg all factions
    
        if event_type == "battle":
            data = event
            details = "A random battle, with a chance to earn a reward."
        else:
            event_key = random.choice(world[event_type][lane])
            data = event[event_key]
            try:
                details = event.maptext
            except:
                if event_type == "faction_event":
                    details = "Faction"#f"A meeting with the {data['name']}, potential friends or foes."
                elif event_type == "story_event":
                    details = ""
                elif event_type == "world_event":
                    details = ""
                else:
                    details = ""
        # Add elif branches for other event types to fill in details
    return {"event": event_type, "details": details, "data" : data}
def generate_random_locations(num_nodes, num_lanes):
    if num_nodes == 1:
        locations = [2]
    else:
        locations = random.sample(range(num_lanes), num_nodes)
    output = [0 for _ in range(num_lanes)]
    for i in locations:
        output[i] = 1
    return output


def generate_minimap(num_steps=10, num_lanes=5, special_steps=None, world_name = "Place"):
    if special_steps is None:
        special_steps = {}

    nodes = []
    minimap = []
    connections = []

    prev_step = None
    for step in range(num_steps): #Create a new step: several nodes at the same layer in the map
        num_nodes = special_steps.get(step)
        if num_nodes is None:
            num_nodes = random.choice([2, 3, 3, 3, 4, 4, 5])
        node_locations = generate_random_locations(num_nodes, num_lanes)
        minimap.append(node_locations)
        step_nodes = [generate_random_node(world_name, i, node_locations[i],is_start=(step == 0), is_end=(step == num_steps-1)) for i in range(num_lanes)]
        nodes.append(step_nodes)

        if prev_step: #Create, if possible, links from the previous step to this one
            connections.append(linkage(prev_step, node_locations))

        prev_step = node_locations

    return nodes, minimap, connections

class Minimap:
    def __init__(self, width, length, special_steps = None, world_name = "Place"):
        self.world_name = world_name
        self.width = width
        self.length = length
        self.map = None #list of lists indicating presence (1) or absence(0) of nodes at each point
        self.nodes = None
        self.connections = None
        self.dispx = 400
        self.dispy = 150 #spacings of nodes, to be adjusted during iteration
        self.borderoffset = 100
        self.ypositions = [1, 0.85, 0.73, 0.634, 0.5572, 0.49576, 0.44661, 0.40729, 0.37583, 0.35066, 0.33053, 0.31442, 0.30154, 0.29123, 0.28299]
        self.maxdisp = 10
        if "lane_id" in worlds[world_name]:
            self.lane_id = worlds[world_name]["lane_id"]
        else:
            self.lane_id = ["W","U","B","R","G"]
        if "setcodes" in worlds[world_name]:
            self.sets = worlds[world_name]["setcodes"]
        else:
            self.sets = None
        if "colorcodes" in worlds[world_name]:
            self.colorcodes = worlds[world_name]["colorcodes"]
        else: 
            self.colorcodes = {"W":(250,250,230),#White
                        "U":(20,50,250),#Blue
                        "B":(80,0,150),#Violet/Black
                        "R":(200,30,20),#Red
                        "G":(10,200,30),#Green
                        "C":(120,120,120),#Grey
                              }#The first five should be enough, but who knows
        # Call generate_minimap function here and set the background, nodes, and connections
        self.nodes, self.map, self.connections = generate_minimap(self.length,self.width, special_steps, world_name=world_name)

    def generate(self, special_steps = None):#Can be used to regenerate a map if desired. Probably unused?
        self.nodes, self.map, self.connections = generate_minimap(self.length, self.width, special_steps, world_name = self.world_name)

    def draw(self, screen, offset, playerpos = None):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (100,150,200),pygame.Rect(0, 0, global_vars.screen_width, global_vars.screen_height*0.3))
        dispx = self.dispx
        dispy = self.dispy #spacings of nodes, to be adjusted during iteration
        borderoffset = self.borderoffset
        maxdisp = self.maxdisp #number of nodes ahead to display
        ypositions = self.ypositions
        for i in range(max(offset-1,0),min(offset+maxdisp,self.length)): #Find nodes, this can be cleaned up!!!
            nodes = self.map[i]
            scale = 1- max(i-offset, 0)/maxdisp
            scale1 = 1- max(i+1-offset, 0)/maxdisp
            ypos = global_vars.screen_height*ypositions[max(i-offset,0)]#- int((i-offset+1.5)*dispy)
            ypos1 = global_vars.screen_height*ypositions[max(i-offset+1,0)]
            if i < self.length-1: #Draw connections, can't do for last step in map of course
                conn = self.connections[i]
                for j1 in range(self.width):
                    xpos = int((((j1+0.5)/self.width - 0.5) * scale +0.5)* global_vars.screen_width)
                    for j2 in range(self.width):
                        if conn[j1,j2]:
                            xpos1 = int((((j2+0.5)/self.width - 0.5) * scale1 +0.5)* global_vars.screen_width)
                            pygame.draw.line(screen,(255,128,128),(xpos,ypos),(xpos1,ypos1))#((i-offset + (offset > 0)) * dispx + borderoffset, (j1*dispy + borderoffset)*scale), ((i-offset+1+ (offset > 0))*dispx + borderoffset, (j2*dispy + borderoffset)*scale1))
            for j in range(self.width):
                xpos = int((((j+0.5)/self.width - 0.5) * scale +0.5)* global_vars.screen_width)
                if nodes[j]:
                    eventtype = self.nodes[i][j]['event']
                    if eventtype in ["battle", "boss"]:#Shield shape
                        points = np.asarray([k for k in range(5)])-2
                        points = np.stack((np.sin(points), np.cos(points)), axis = -1)*25*scale
                        points = np.add(points, np.asarray([xpos, ypos]))#(i-offset + (offset > 0)) * dispx + borderoffset, (j * dispy + borderoffset)*scale]))
                        pygame.draw.polygon(screen, self.colorcodes[self.lane_id[j]],points)
                    elif eventtype in ["story_event", "planeswalker"]:
                        points = np.asarray([[0,1],[0.1,0.4],[0.35,0.2],[0.7,0.1],[0.8,-0.1],#Base
                                             [0.7,-0.8],#Outer peak
                                             [0.6,-0.2],
                                             [0.55,-0.1],
                                             [0.5,-0.2],
                                             [0.4,-0.9],#second peak
                                             [0.3,-0.3],
                                             [0.2,-0.1],
                                             [0.1,-0.3],
                                             [0,-1]]) #Middle peak
                        revpoints = np.array(np.flip(points,0))
                        revpoints[:, 0] *= -1
                        points = np.concatenate((points, revpoints), axis=0)
                        points = points*35*scale
                        points = np.add(points, np.asarray([xpos, ypos]))
                        pygame.draw.polygon(screen, self.colorcodes[self.lane_id[j]],points)
                    elif eventtype in ["base", "world_event"]:#Horizon shape
                        points = np.asarray([k for k in range(10)])+0.2124+np.pi/2
                        points = np.stack((np.sin(points), np.cos(points)), axis = -1)*25*scale
                        points = np.add(points, np.asarray([xpos, ypos]))
                        pygame.draw.polygon(screen, self.colorcodes[self.lane_id[j]],points)
                    elif eventtype in ["factions"]:
                        points = np.asarray([k*np.pi for k in range(7)])
                        points = np.stack((np.sin(points), np.cos(points)), axis = -1)*25*scale
                        points = np.add(points, np.asarray([xpos, ypos]))
                        pygame.draw.polygon(screen, self.colorcodes[self.lane_id[j]],points)
                    else:
                        pygame.draw.circle(screen, self.colorcodes[self.lane_id[j]],(xpos, ypos), 25*scale)
        if not playerpos is None:
            pygame.draw.circle(screen, (255,128,100),(borderoffset + int( dispx * 0.2*(offset+1)), 150),35)# playerpos * dispy + borderoffset), 35)
                            
    def is_click_on_node(self, x, y, offset):
        dispx = self.dispx
        dispy = self.dispy #spacings of nodes, to be adjusted during iteration
        borderoffset = self.borderoffset
        maxdisp = self.maxdisp #number of nodes ahead to display
        click_tolerance = 25

        for i in range(offset, min(offset + maxdisp, self.length)):
            nodes = self.map[i]
            scale = 1- max(i-offset, 0)/maxdisp
            node_y = global_vars.screen_height*self.ypositions[max(i-offset,0)]
            for j in range(self.width):
                if nodes[j]:
                    node_x = int((((j+0.5)/self.width - 0.5) * scale +0.5)* global_vars.screen_width)
                    distance = ((x - node_x) ** 2 + (y - node_y) ** 2) ** 0.5
                    if distance <= click_tolerance*scale:
                        return i, j

        return None, None
    def handle_click(self, x, y, offset):
        i, j = self.is_click_on_node(x, y, offset)
        if i is not None and j is not None:
            node = self.nodes[i][j]
            return i, j, node
        return None, None, None
