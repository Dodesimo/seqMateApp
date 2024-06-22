from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, getGenomeAnnotations, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion)

agentExecutor = initializeAgent()
outputs = getGenomeAnnotations(agentExecutor)
print(outputs)
