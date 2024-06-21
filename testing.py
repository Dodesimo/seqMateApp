from seqmate import fetchFASTQNames, initializeAgent

agentExecutor = initializeAgent()
print(agentExecutor.invoke({"input":"What are the first five fibonacci numbers?"})['output'])