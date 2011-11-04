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


	def eval(self, x):
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


	def __getValue(self, match, string):
		g = re.search(match, string, flags=re.MULTILINE)
		if (g != None):
			return float(g.group(1))
		else:
			return None


	def fitness(self, recipe):
		f = 0.0
		for i in range(1, self.nSeeds+1):
			for c in self.cmds:
				cmd = list(c)
				for var in self.Vars:
					cmd.append( "-f" + str(var.name) + ":" + str(var.eval( recipe[self.Vars.index(var)] )) )
				cmd.extend( ["-s", str(i)] )

				output = subprocess.check_output( cmd, stderr=subprocess.STDOUT )

				missing  = self.__getValue('^Missing:\s*([0-9]+\.?[0-9]*)', output)
				extra    = self.__getValue('^Extra:\s*([0-9]+\.?[0-9]*)', output)
				failed   = self.__getValue('^Failed:\s*([0-9]+\.?[0-9]*)', output)
				tracking = self.__getValue('^Tracking:\s*([0-9]+\.?[0-9]*)', output)

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
	def __init__(self, stddev=0.01, pMut=0.5, pCross=0.01, bestN=1):
		self.env = Environment()
		self.stddev = stddev
		self.pMut = pMut
		self.pCross = pCross
		self.bestN = 1
		self.currGen = 0

	def __everyGen(self, ga):
		self.currGen += 1
		print "\nGeneration:", self.currGen
		if (self.bestN > len(ga.getPopulation())):
			self.bestN = len(ga.getPopulation())
		for n in range(0,self.bestN):
			best = ga.getPopulation().bestFitness(n)
			var = dict( [ (v.name, v.eval(best[self.env.Vars.index(v)])) for v in self.env.Vars ] )
			print "\nRank", n+1, "individual:"
			for k in var:
				print k, var[k]
		print "\n----------"

	def run(self, generations, population, bestN):
		self.currGen = 0
		self.bestN = bestN
		self.recipe = G1DList.G1DList( len(self.env.Vars) )
		self.recipe.evaluator.set(self.env.fitness)
		self.recipe.initializator.set(Initializators.G1DListInitializatorReal)
		self.recipe.mutator.set(Mutators.G1DListMutatorRealGaussian);
		self.recipe.setParams(rangemin=0.0, rangemax=1.0, gauss_mu=0.0, gauss_sigma=self.stddev)
		self.recipe.crossover.set(cross)
		#recipe.crossover.set(Crossovers.G1DListCrossoverUniform)
		
		self.ga = GSimpleGA.GSimpleGA(self.recipe)
		self.ga.pMutation = self.pMut
		self.ga.pCrossover = self.pCross
		self.ga.setGenerations(generations)
		self.ga.setPopulationSize(population)
		self.ga.setMinimax(Consts.minimaxType["minimize"])
		self.ga.stepCallback.set(self.__everyGen)

		self.ga.evolve()

		dictList = list()
		if( bestN > population ):
			bestN = population
		for i in range(0,bestN):
			best = self.ga.getPopulation().bestFitness(i)
			var = dict( [ (v.name, v.eval(best[self.env.Vars.index(v)])) for v in self.env.Vars ] )
			dictList.append(var)

		return dictList
# ---------------------------------------------------------


