from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion)

agentExecutor = initializeAgent()
outputs = samBamConversion(agentExecutor)
print(outputs)
