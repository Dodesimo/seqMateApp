from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, getGenomeAnnotations, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion, featureCountGeneration, countTableColumnEdit)

agentExecutor = initializeAgent()
outputs = countTableColumnEdit(agentExecutor)
print(outputs)
