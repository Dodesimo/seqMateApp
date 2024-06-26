from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, getGenomeAnnotations, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion, featureCountGeneration, diffExp)

agentExecutor = initializeAgent()
outputs = diffExp(agentExecutor)
print(outputs)
