from seqmate import (fetchFASTQNames, initializeAgent,
                     firstLineFASTQ, qualityControlFASTQ, trimFASTQ, getGenomeAnnotations, indexGenomeHISAT, fetchFASTQTrimmed, genomeAlignmentFASTQ, samBamConversion, featureCountGeneration, diffExp, generateUniprotSummaries, generateGeneSummaries, fetchGeneInfoFiles)

agentExecutor = initializeAgent()
outputs = generateGeneSummaries()
print(outputs)
