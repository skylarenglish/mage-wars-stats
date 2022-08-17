from random import choice, randint
from math import ceil, floor
from copy import deepcopy
import streamlit as st
import matplotlib.pyplot as plt

mage_wars_die = [(0,0), (0,0), (1,0), (2,0), (0,1), (0,2)]
incorporeal_die = [(0,0),(0,0),(1,0),(0,0),(0,1),(0,0)]
resilient_die = [(0,0),(0,0),(0,0),(0,0),(0,1),(0,2)]
skylar_die = [(0,0),(1,0),(1,0),(2,0),(0,1),(0,1)]

default_free_variable_levels = {'armor': (0, 6), 'health': (1, 41), 'attack_dice': (1, 8), 'piercing': (0,6)}


	
# doublestrike, burn, rot, will need to make attacks into a list
class Creature():
	def __init__(self, armor=0, health=1, attack_dice=1, piercing=0, defense=None, *args, **kwargs):
		self.armor = armor
		self.health = health
		self.attack_dice = max(attack_dice,1)
		self.piercing = piercing
		self.defense = defense
		for key, value in kwargs.items():
			setattr(self, key, value) 


	def attack(self, attacker, defender):
		normal, crit = (0,0)
		if defender.defense and randint(1,12) >= defender.defense:
			return 0
		else :
			for _ in range(attacker.attack_dice):
				if getattr(defender, 'incorporeal', None):
					normal_add, crit_add = choice(incorporeal_die)
				if getattr(defender, 'resilient', None):
					normal_add, crit_add = choice(resilient_die)
				else:
					normal_add, crit_add = choice(mage_wars_die)
				normal += normal_add
				crit += crit_add
			adjusted = max(normal - max(defender.armor - attacker.piercing, 0),0)
			return adjusted + crit

	def attack_to_death(self, target):
		turns = 0
		while target.health > 0:
			turns += 1
			result = self.attack(self, target)
			target.health -= result
			#print(self, "did ", result, "to ", target, " turn ", turns)
		return turns


def trial(creature1, creature2, num_trials=3000, alpha=0.10):
	turn_sims = [deepcopy(creature1).attack_to_death(deepcopy(creature2)) for _ in range(num_trials)]
	turn_sims.sort()
	return (turn_sims[ceil(num_trials*(alpha/2))], turn_sims[floor(num_trials*(1-alpha/2))])


creatures = {'Werewolf': Creature(3, 15, 4, 1), 'Dwarf': Creature(1, 11, 3, 0)}

creature1_choice = st.selectbox('Attacking Creature',creatures.keys())
creature2_choice = st.selectbox('Defending Creature',creatures.keys())
st.write("Here's how many attacks it would take for", creature1_choice, " to kill ", creature2_choice)
st.write(trial(creatures[creature1_choice], creatures[creature2_choice]))
free_variable = st.selectbox('What variable would you like to see change?', ['armor', 'health', 'attack_dice', 'piercing'])


trials = []
for i in range(default_free_variable_levels[free_variable][0], default_free_variable_levels[free_variable][1]):
	creature1 = deepcopy(creatures[creature1_choice])
	creature2 = deepcopy(creatures[creature2_choice])
	setattr(creature1, free_variable, i)
	setattr(creature2, free_variable, i)
	trials.append(trial(creature1, creature2))

fig, ax = plt.subplots()
ax.plot([vars[0] for vars in trials])
ax.plot([vars[1] for vars in trials])
st.pyplot(fig)
st.write(trials)