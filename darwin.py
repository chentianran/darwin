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
		print recipe[0]
		return 0
		f = 0.0
		for c in self.cmds:
			cmd = list(c)
			for var in self.Vars:
				cmd.append( "-f" + str(var.name) + ":" + str(var.Eval( recipe[self.Vars.index(var)] )) )


			
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
				print tracking
				f = f + tracking * self.w_tracking

		return f
# --------------------------------------------



# ----------------------------------
# custom crossover
# ----------------------------------
def cross(recipe, **args):
	return (args["mom"], args["dad"])





# ------------------------------------------
# main driver
#
# -----------------------------------------

polysys = ['cassou', 'barry', 'boon', 'heart', 'cyclic5', 'cyclic6', 'cyclic7', 'reimer4', 'reimer5', 'reimer6', 'reimer7']
options = "--post=jump --post=check-against --no-mp"

env = Environment()

for name in polysys:
	cmdLine = ["/home/ovenhouse/h3/h3", "-s1", 
					  "-fanswers:/home/ovenhouse/h3/testcases/answers/" + str(name),
					  "/home/ovenhouse/h3/testcases/" + str(name) + ".lee"]
	cmdLine.extend( options.split() )
	env.cmds.append( cmdLine )

env.Vars.append( Variable("facet-begin",    2.0, 6.0, -1.0) )
env.Vars.append( Variable("facet-stable",   1.0, 4.0, -1.0) )
env.Vars.append( Variable("facet-small",    1.0, 4.0, -1.0) )
env.Vars.append( Variable("facet-negative", 0.7, 4.0, -1.0) )


recipe = G1DList.G1DList(4)
recipe.evaluator.set(env.Fitness)
recipe.initializator.set(Initializators.G1DListInitializatorReal)
recipe.mutator.set(Mutators.G1DListMutatorRealGaussian);
recipe.setParams(rangemin=0.0, rangemax=1.0, gauss_mu=0.0, gauss_sigma=0.001)
recipe.crossover.set(cross)
#recipe.crossover.set(Crossovers.G1DListCrossoverUniform)

ga = GSimpleGA.GSimpleGA(recipe)
ga.pMutation = 0.1
ga.pCrossover = 0.01
ga.setGenerations(300)
ga.setPopulationSize(200)
ga.setMinimax(Consts.minimaxType["minimize"])
ga.evolve(freq_stats=10)
print ga.bestIndividual()

