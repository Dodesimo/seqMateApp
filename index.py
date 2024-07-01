from flask import Flask, render_template, request, flash, url_for
from seqmate import initializeAgent, qualityControlFASTQ, indexGenomeHISAT, trimFASTQ, genomeAlignmentFASTQ, \
    samBamConversion, getGenomeAnnotations, featureCountGeneration, countTableColumnEdit, metaDataGeneration, diffExp, \
    summaryStatsEdit, generateUniprotSummaries, generateGeneSummaries
import os
import requests

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/analysis", methods=['GET', 'POST'])
def analysis():
    if request.method == "POST":

        fastqs = request.files.getlist("uploadDataset")

        for fastq in fastqs:
            fastq.save(os.path.join("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads", fastq.filename))

        fastqsControl = request.form.get('controlExperimental').split(",")
        genome = request.files.get('genomeUpload')
        genome.save(os.path.join("/Users/devam/PycharmProjects/seqMateFrontEnd", genome.filename))

        log2FoldChange = request.form.get('log2FoldChange')
        pValueThreshold = request.form.get('pvalue')
        sequence = request.form.get('adapterSequence')
        topNGenes = request.form.get('topXGenes')

        agentExecutor = initializeAgent()
        qualityControlFASTQ(agentExecutor)
        trimFASTQ(agentExecutor)
        indexGenomeHISAT(agentExecutor)
        genomeAlignmentFASTQ(agentExecutor)
        samBamConversion(agentExecutor)
        getGenomeAnnotations(agentExecutor)
        featureCountGeneration(agentExecutor)
        countTableColumnEdit(agentExecutor)
        metaDataGeneration(agentExecutor,fastqsControl)
        diffExp(agentExecutor)
        summaryStatsEdit(agentExecutor)
        filter(agentExecutor, log2FoldChange, pValueThreshold)
        generateUniprotSummaries(agentExecutor, topNGenes)
        generateGeneSummaries()

        return render_template('analysis.html')



    else:
        return render_template('analysis.html')


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


if __name__ == '__main__':
    app.run()
