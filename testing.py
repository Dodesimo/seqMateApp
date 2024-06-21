from seqmate import fetchFASTQNames, initializeAgent, firstLineFASTQ, qualityControlFASTQ

agentExecutor = initializeAgent()
outputs = qualityControlFASTQ(agentExecutor)
print(outputs[0])
