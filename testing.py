from seqmate import fetchFASTQNames, initializeAgent, firstLineFASTQ

agentExecutor = initializeAgent()
outputs = firstLineFASTQ(agentExecutor)
print(outputs[0])
