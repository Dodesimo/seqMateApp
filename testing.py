from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, indexGenomeHISAT)

agentExecutor = initializeAgent()
outputs = indexGenomeHISAT(agentExecutor)
print(outputs)
