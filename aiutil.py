import itertools
import torch.nn.init as init
from torch import nn, optim
import math
import torch
import random
import numpy as np
from cardutil import select_cards, shortened_card_data

def get_color_combinations(colors):
    color_combinations = []
    for length in range(len(colors) + 1):
        for subset in itertools.combinations(colors, length):
            color_combinations.append(list(subset))
    return color_combinations


# Get all color combinations, including the colorless deck
colors = ["W", "U", "B", "R", "G"]
color_combinations = get_color_combinations(colors)
color_combinations+= [random.sample(["W", "U","B", "R","G", ""],3) for _ in range(32)]

def deck_costs(deck):
    
    if len(deck):
        symbols = ["W", "U", "B","R","G","C"]
        ratios = np.zeros(len(symbols))
        minimums = np.zeros(len(symbols))
        fractions = np.zeros(len(symbols))
        for i in range(len(symbols)):
            c = symbols[i]
            costs = [card["mana_cost"].count(c) for card in deck]
            devotions = [card["mana_cost"].count(c)/max(card["cmc"][0], 1) for card in deck]
            ratios[i] = sum(costs)/len(deck)
            fractions[i] = sum(devotions)/len(deck)
            minimums[i] = max(costs)
        #ratios = ratios/(max(np.sum(ratios),1))
        costs = np.asarray([card["cmc"][0] for card in deck])
        colorscount = np.asarray([sum([min(card["mana_cost"].count(c),0.2) for c in symbols]) for card in deck])
        return(np.concatenate((ratios, minimums*0.2, fractions*2, [np.min(costs)*0.05], [np.max(costs)*0.05], [np.mean(costs)*0.05], [np.mean(colorscount)],[np.max(colorscount)])), minimums)#1*23 array of normalised values, and a separate mins array
    else:
        return(np.zeros(23),np.zeros(6))
def soft_integer_round(x, factor=0.8):
    return torch.add(x , (torch.sin((0.5+x) * 2 * math.pi) / (2 * math.pi)),alpha=factor)

def eval_deck_tensor(deck, land_ratio_dict_tensor, filtered_land_ratio_dict_tensor=None):
    min_probs = []
    card_probs = []
    total_l = torch.sum(land_ratio_dict_tensor).clone().detach().requires_grad_(True)
    for card in deck:
        prob = eval_card_tensor(card, land_ratio_dict_tensor, total_l)
        card_probs.append(prob)
    min_probs.append(torch.min(torch.stack(card_probs)))
    min_probs.append(torch.mean(torch.stack(card_probs)))
    if filtered_land_ratio_dict_tensor is not None:
        for land_ratio_dict_tensor in [filtered_land_ratio_dict_tensor]:
            card_probs = []
            total_l = torch.sum(land_ratio_dict_tensor).clone().detach().requires_grad_(True)
            for card in deck:
                prob = eval_card_tensor(card, land_ratio_dict_tensor, total_l)
                card_probs.append(prob)
            min_probs.append(torch.min(torch.stack(card_probs))*0.01)
    loss = torch.sum(torch.stack(min_probs))
    loss = torch.div(1,torch.add(loss,0.1))#loss = torch.pow(loss,4) #Steeper gradient around probability of 0
    if filtered_land_ratio_dict_tensor is not None:
        loss += torch.sum(torch.abs(torch.sub(land_ratio_dict_tensor,filtered_land_ratio_dict_tensor))*0.05)
    return loss.requires_grad_(True), min_probs


def combo (n, k):#Number of possible combinations, adjusted to allow continuous variables and to work with tensors
    return ((n + 1).lgamma() - (k + 1).lgamma() - ((n - k) + 1).lgamma()).exp()
def hypergeom_cdf(k, N, K, n):#Cumulative distribution function for draw likelihoods (likelihood of up to a certain value)
    i = torch.arange(0, int(k + 1)).float()
    num_comb = combo(K, i) * combo(N - K, n - i)
    total = num_comb.sum()
    return total / combo(N, n)

def hypergeom_sf(k, N, K, n):#Survival function: odds of not getting k or fewer hits on n draws without replacement, given K targets in a pool of N
    return 1 - hypergeom_cdf(k, N, K, n).requires_grad_(True)


def eval_card_tensor(card, land_ratio_dict_tensor, total_l):
    cmc = torch.tensor(float(card["cmc"][0]), dtype=torch.float32)
    probability = torch.tensor(1.0, dtype=torch.float32)

    if cmc > total_l:
        return torch.tensor(0.0, dtype=torch.float32)

    for idx, color in enumerate(["W", "U", "B", "R", "G", "C"]):
        num = torch.tensor(float(card["mana_cost"].count(color)), dtype=torch.float32)
        if num > 0: #If a card requires a certain type of mana
            if num > land_ratio_dict_tensor[idx]:
                return torch.tensor(0.0, dtype=torch.float32) #If there isn't enough of that type
            else:
                hg = hypergeom_sf(num - 1, total_l, land_ratio_dict_tensor[idx], cmc)#Probablity of getting enough of that type
                probability *= hg#adjust overall probability

    return probability
# Define the neural network architecture

class ContinuousPolicyNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ContinuousPolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size*2)
        self.fc2 = nn.Linear(hidden_size*2, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

        # Initialize weights
        init.normal_(self.fc1.weight, mean=0, std=0.25)
        init.normal_(self.fc2.weight, mean=0, std=0.25)
        init.normal_(self.fc3.weight, mean=0, std=0.25)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        #x = torch.mul(x,x1[0,0:6])
        return x
    
    def print_weights(self):
        print("fc1.weight", torch.sum(self.fc1.weight).item())
        print("fc1.bias", torch.sum(self.fc1.bias).item())
        print("fc2.weight", torch.sum(self.fc2.weight).item())
        print("fc2.bias", torch.sum(self.fc2.bias).item())
        print("fc3.weight", torch.sum(self.fc3.weight).item())
        print("fc3.bias", torch.sum(self.fc3.bias).item())
class ContinuousPolicyNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, hidden_layers=1):
        super(ContinuousPolicyNetwork, self).__init__()
        self.output_size = output_size
        self.input_size = input_size
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(input_size, hidden_size))
        for _ in range(hidden_layers):
            self.layers.append(nn.Linear(hidden_size, hidden_size))
        self.layers.append(nn.Linear(hidden_size, output_size))

        # Initialize weights
        for layer in self.layers:
            init.normal_(layer.weight, mean=0, std=0.25)

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = torch.relu(layer(x))
        x = self.layers[-1](x)  # Remove activation function from the last layer
        return x
    
    def print_weights(self):
        for layer in self.layers:
            print("weight", torch.sum(layer.weight).item())
            print("bias", torch.sum(layer.bias).item())
    
    def add_preprocess(self):
        new_layer = nn.Linear(self.input_size, self.input_size)
        init.normal_(new_layer.weight, mean=0, std=0.1)
        self.layers.insert(0, new_layer)
    
    def add_postprocess(self):
        new_layer = nn.Linear(self.output_size, self.output_size)
        init.normal_(new_layer.weight, mean=-0.2, std=0.1)
        self.layers.append(new_layer)


# Define hyperparameters
input_size = 24  # cost_ratios and minimums concatenated
hidden_size = 48
output_size = 6  # number of possible actions (land_ratios)


# Create the policy network
land_policy_net = ContinuousPolicyNetwork(input_size, hidden_size, output_size, 2)


def train_land_model(policy_net = land_policy_net, num_episodes = 500, prelearning = 1000, deck_refresh = 1, learning_rate = 1e-2): #This code isn't actually needed in the game now that the model's trained and saved, but I'm just really proud of it. I might later add a feature that retrains a little (10 iterations) on each deck as it's predicted.
    optimizer = optim.Adam(policy_net.parameters(), lr=learning_rate)
    for episode in range(prelearning):#Quicker training to reconstruct minimums (so it starts with something playable for the real training)
        if episode % deck_refresh == 0: #Keep decks for a short length of time, so that training can go towards something consistent for a while
            total_lands = int(random.random()*20)+10 #Currently randomised, should this be fed into the model?
            # Generate a random cost_ratio and minimums
            newdeck = select_cards(shortened_card_data, total_lands, 
                         {'color': random.sample(["W", "U","B", "R","G", ""],3)},
                         exclusive = False, blankparams = False,  negparams = {"card_type":["Land", "Token", "Emblem"]})
            cost_ratios, minimums = deck_costs(newdeck) #One normalised 1*23 array, and the minimums
            #total_lands = sum(minimums)
            state = torch.tensor(np.concatenate((cost_ratios, np.asarray([total_lands*0.05]))), dtype=torch.float32).unsqueeze(0)


        # Sample action (land_ratios) from the policy
        # Convert probabilities to land_ratios
        land_ratios = policy_net(state).requires_grad_().squeeze(0)
        land_ratios = torch.abs(land_ratios).requires_grad_()

        # Perform any necessary normalization or conversion to integers, etc. here
        # Example: Normalize the values to sum to a specific total number of lands
        land_ratios = torch.mul(land_ratios, total_lands*0.2).requires_grad_()
        land_ratios = soft_integer_round(land_ratios)
        loss = torch.nn.functional.cross_entropy(land_ratios, torch.tensor(minimums, dtype=torch.float32))
        loss = torch.add(loss, torch.pow(torch.sub(torch.div(torch.sum(land_ratios),total_lands),1),2), alpha=0.1) #Aim for total lands close to desired value
        # Update the model's parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    learning_rate = learning_rate*0.1
    weight_decay = 1e-5  # You can adjust this value as needed
    optimizer = optim.Adam(policy_net.parameters(), lr=learning_rate, weight_decay=weight_decay)

    for episode in range(num_episodes):
        if episode % deck_refresh == 0: #Keep decks for a short length of time, so that training can go towards something consistent for a while
            total_lands = int(random.random()*10)+15 #Currently randomised, should this be fed into the model?
            # Generate random cost_ratios
            color_combinations = get_color_combinations(colors)
            color_combinations+= [random.choices(["W", "U","B", "R","G"],k=2) for _ in range(32)]
            decks = [
                select_cards(shortened_card_data, total_lands, 
                             {'color': c},
                             exclusive = {'color': True}, blankparams = False,  negparams = {"card_type":["Land", "Token", "Emblem"]}
                            ) for c in color_combinations]
            states = [# Sample state (land_ratios) from the policy
                torch.tensor(np.concatenate((deck_costs(deck)[0], np.asarray([total_lands*0.05]))), dtype=torch.float32).unsqueeze(
                    0)
                for deck in decks
            ]
        batch_losses = []
        batch_minprob = []
        for state, deck in zip(states, decks):
            # Sample action (land_ratios) from the policy
            land_ratios = policy_net(state).requires_grad_().squeeze(0)
            land_ratios = torch.abs(land_ratios)#Positive values only, without losing gradients

            # Perform any necessary normalization or conversion to integers, etc. here
            land_ratios = torch.mul(land_ratios, total_lands*0.2).requires_grad_()
            land_ratios = soft_integer_round(land_ratios)
            loss, minprob = eval_deck_tensor(deck, land_ratios)
            loss = torch.add(loss, torch.pow(torch.sub(torch.div(torch.sum(land_ratios),total_lands),1),2), alpha=2)
            batch_losses.append(loss)
            batch_minprob.append(minprob[0])


        # Update the model's parameters
        avg_loss = torch.stack(batch_losses).mean()
        optimizer.zero_grad()
        avg_loss.backward()
        optimizer.step()


def save_model(model, pathway =  'land_select_model.pth'):
    torch.save(model.state_dict(),pathway)


# First, create a model object
# Then, load the saved state_dict into the model
land_policy_net.load_state_dict(torch.load('land_select_model.pth'))

# Make sure to call model.eval() method before inference
land_policy_net.eval()

def select_lands(decklist,total_lands = 20, sets = None,tolerance = 1, policy_net = land_policy_net):
    cost_ratios, minimums = deck_costs(decklist) #One normalised 1*23 array, and the minimums
    state = torch.tensor(np.concatenate((cost_ratios, np.asarray([total_lands*0.05]))), dtype=torch.float32).unsqueeze(0)
    # Sample action (land_ratios) from the landgen policy
    land_ratios = policy_net(state).squeeze(0)
    land_ratios = torch.abs(land_ratios)
    land_ratios = torch.mul(land_ratios, total_lands*0.2)#Undo normalization
    
    land_ratios = land_ratios.detach().numpy().round(0).astype(int)
    land_ratios = np.maximum(land_ratios, minimums)
    
    if sum(minimums):#Make obvious fixes to the land lists. Keep these changes to a minimum though if they will change ratios
        land_ratios = np.where(minimums==0,0,land_ratios)
        while sum(land_ratios) > total_lands + tolerance and not min(minimums):
            land_ratios = np.where(minimums==0,land_ratios-1,land_ratios)
        land_ratios = np.maximum(land_ratios, 0)
        while sum(land_ratios) < total_lands - tolerance:
            land_ratios = np.where(minimums!=0,land_ratios+1,land_ratios)
    land_list = []
    for c, v in zip(colors, land_ratios):
        if v:
            v = int(v)
            parameters = {"set": [], 'card_type': ['Basic'],'color': [c]}
            exclusive={"set": False, 'card_type': False,'color': True}
            blankparams={"set": True, 'card_type': True,'color': True}
            if c == "C":
                parameters["color"] = []
                blankparams["color"] = False
            if sets is not None:
                parameters["set"] = sets
                exclusive["set"] = True
            
            sublist = select_cards(shortened_card_data, v, params = parameters, exclusive=exclusive, negparams=None, blankparams=blankparams)
            for i in sublist:
                land_list.append( i )
    return(land_list)
