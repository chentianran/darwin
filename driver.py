import darwin


# ------------------------------------------
# main driver
#
# -----------------------------------------

polysys = ['cassou', 'barry'] #, 'boon', 'heart', 'cyclic5', 'cyclic6', 'cyclic7', 'reimer4', 'reimer5', 'reimer6', 'reimer7']
options = "--post=jump --post=check-against --no-mp -estack"

alg = darwin.GenAlg()

for name in polysys:
	cmdLine = ["/home/ovenhouse/h3/h3", 
					  "-fanswers:/home/ovenhouse/h3/testcases/answers/" + str(name),
					  "/home/ovenhouse/h3/testcases/" + str(name) + ".lee"]
	cmdLine.extend( options.split() )
	alg.env.cmds.append( cmdLine )



alg.env.nSeeds = 1		# number of random seeds to try
alg.env.Vars.append( darwin.Variable("facet-begin",    2.0, 6.0, -1.0) )
alg.env.Vars.append( darwin.Variable("facet-stable",   1.0, 4.0, -1.0) )
alg.env.Vars.append( darwin.Variable("facet-small",    1.0, 4.0, -1.0) )
alg.env.Vars.append( darwin.Variable("facet-negative", 0.7, 4.0, -1.0) )

best = alg.run( gens=2, popSize=2, dispFreq=1, bestN=1 )

for ind in range(0,len(best)):
	print "\nRank", ind+1, "individual:"
	for v in alg.env.Vars:
		print v.name, (best[ind])[v.name]
