import subprocess
import re

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Mutators
from pyevolve import Crossovers


# -------------------------------
# Variable class
#
# ------------------------------
class Variable:
	def __init__(self, name, Min, Max, sign):
		self.name = name
		self.Min = Min
		self.Max = Max
		self.sign = sign


	def Eval(self, x):
		power = self.Min + x*(self.Max-self.Min)
		return 10**(self.sign*power)
# ------------------------------------




# -------------------------------
# Environment class
#
# ------------------------------
class Environment:
	def __init__(self):
		self.Vars = list()
		self.cmds = list()
		self.nSeeds = 1

		self.w_missing  = 200.0
		self.w_extra    = 200.0
		self.w_failed   = 100.0
		self.w_tracking = 1.0


	def GetValue(self, match, string):
		g = re.search(match, string, flags=re.MULTILINE)
		if (g != None):
			return float(g.group(1))
		else:
			return None


	def Fitness(self, recipe):
		f = 0.0
		for i in range(1, self.nSeeds+1):
			for c in self.cmds:
				cmd = list(c)
				for var in self.Vars:
					cmd.append( "-f" + str(var.name) + ":" + str(var.Eval( recipe[self.Vars.index(var)] )) )
				cmd.extend( ["-s", str(i)] )

				output = subprocess.check_output( cmd, stderr=subprocess.STDOUT )

				missing  = self.GetValue('^Missing:\s*([0-9]+\.?[0-9]*)', output)
				extra    = self.GetValue('^Extra:\s*([0-9]+\.?[0-9]*)', output)
				failed   = self.GetValue('^Failed:\s*([0-9]+\.?[0-9]*)', output)
				tracking = self.GetValue('^Tracking:\s*([0-9]+\.?[0-9]*)', output)

				if( missing != None ):
					f = f + missing * self.w_missing
				if( extra != None ):
					f = f + extra * self.w_extra
				if( failed != None ):
					f = f + failed * self.w_failed
				if( tracking != None ):
					f = f + tracking * self.w_tracking

		return f
# --------------------------------------------



# ----------------------------------
# custom crossover
# ----------------------------------
def cross(recipe, **args):
	return (args["mom"], args["dad"])



# -----------------------------------------------
# GenAlg class
#
# class encapsulating all genetic algorithm
# behavior of pyevolve
# -----------------------------------------------
class GenAlg:
	def __init__(self, stddev=0.01, pMut=0.5, pCross=0.01, freq=10):
		self.env = Environment()
		self.stddev = stddev
		self.pMut = pMut
		self.pCross = pCross
		
	def Run(self, gens, popSize, dispFreq):
		self.recipe = G1DList.G1DList( len(self.env.Vars) )
		self.recipe.evaluator.set(self.env.Fitness)
		self.recipe.initializator.set(Initializators.G1DListInitializatorReal)
		self.recipe.mutator.set(Mutators.G1DListMutatorRealGaussian);
		self.recipe.setParams(rangemin=0.0, rangemax=1.0, gauss_mu=0.0, gauss_sigma=self.stddev)
		self.recipe.crossover.set(cross)
		#recipe.crossover.set(Crossovers.G1DListCrossoverUniform)
		
		self.ga = GSimpleGA.GSimpleGA(self.recipe)
		self.ga.pMutation = self.pMut
		self.ga.pCrossover = self.pCross
		self.ga.setGenerations(gens)
		self.ga.setPopulationSize(popSize)
		self.ga.setMinimax(Consts.minimaxType["minimize"])

		self.ga.evolve(freq_stats=dispFreq)
		print self.ga.bestIndividual()
# ---------------------------------------------------------


