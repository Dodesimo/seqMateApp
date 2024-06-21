from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ)

agentExecutor = initializeAgent()
outputs = trimFASTQ(agentExecutor)
print(outputs)
