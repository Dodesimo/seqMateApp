from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ)

agentExecutor = initializeAgent()
outputs = genomeAlignmentFASTQ(agentExecutor)
print(outputs)
