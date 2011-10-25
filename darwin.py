
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Mutators
from pyevolve import Crossovers

def eval_func(recipe):
   score = 0
   # iterate over the chromosome
   for value in recipe:
       score += abs(value**3.0)
   return score

def cross(recipe, **args):
	return (args["mom"], args["dad"])

genome = G1DList.G1DList(1)
genome.evaluator.set(eval_func)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian);
genome.setParams(rangemin=-1.0, rangemax=1.0, gauss_mu=0.0, gauss_sigma=0.001)
genome.crossover.set(cross)
#genome.crossover.set(Crossovers.G1DListCrossoverUniform)

ga = GSimpleGA.GSimpleGA(genome)
ga.pMutation = 0.1
ga.pCrossover = 0.01
ga.setGenerations(300)
ga.setPopulationSize(200)
ga.setMinimax(Consts.minimaxType["minimize"])
ga.evolve(freq_stats=10)
print ga.bestIndividual()

