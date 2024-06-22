from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, getGenomeAnnotations, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion, featureCountGeneration)

agentExecutor = initializeAgent()
outputs = featureCountGeneration(agentExecutor)
print(outputs)
