from random import choice, randint
from math import ceil, floor
from copy import deepcopy

mage_wars_die = [(0,0), (0,0), (1,0), (2,0), (0,1), (0,2)]
skylar_die = [(0,0),(1,0),(1,0),(2,0),(0,1),(0,1)]


	
#print(simulate(5, 3, 1))
# defense, doublestrike, incorporeal, burn, rot,
class Creature():
	def __init__(self, armor, health, attack_dice, piercing, defense=None):
		self.armor = armor
		self.health = health
		self.attack_dice = attack_dice
		self.piercing = piercing
		self.defense = defense

	def attack(self, attacker, defender):
		normal, crit = (0,0)
		if defender.defense and randint(1,12) >= defender.defense:
			return 0
		else :
			for _ in range(attacker.attack_dice):
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
	print(turn_sims[ceil(num_trials*(alpha/2))], "to", turn_sims[floor(num_trials*(1-alpha/2))])


trial(Creature(1, 15, 4, 1), Creature(2, 36, 4, 0, 7))