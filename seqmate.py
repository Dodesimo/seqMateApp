# Helper functions for the back end.
import glob
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent, create_csv_agent
from langchain_openai import ChatOpenAI
import os
import pandas as pd


def initializeAgent():
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    with open('config.txt') as f:
        first_line = f.readline()

    os.environ["OPENAI_API_KEY"] = first_line

    tools = [PythonREPLTool()]
    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code. You are to use a variety of bioinformatics packages, including but not limited to Bio, fastqp, cutadapt, and HISAT. You have access to the terminal through bash.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)

    agent = create_openai_functions_agent(llm, tools, prompt)
    agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agentExecutor


def fetchFASTQNames():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/*.fastq"):
        names.append(file)

    return names


def fetchFASTQTrimmed():
    names = []

    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/edits/*trimmed.fastq"):
        names.append(file)

    return names


def fetchSAMFiles():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/edits/*.sam"):
        names.append(file)

    return names


def fetchBAMFiles():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/edits/*.bam"):
        names.append(file)

    return names


def fetchGeneInfoFiles():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/genes/*.csv"):
        names.append(file)

    return names


def firstLineFASTQ(agentExecutor):
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = (f"Using Bio, Could you open the FASTA files "
                  f"{f}"
                  f"and print its first line")
        prompts.append(prompt)

    outputs = []
    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


# To do for flask frontend: display graphs.
def qualityControlFASTQ(agentExecutor):
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = ("Using Bio, could you conduct some quality control analysis of FASTA file "
                  f"{f}"
                  "Utilize metrics like PHRED score, duplication rate, and others you feel are beneficial. and create multiple GRAPHS/CHARTS for ALL metrics. THIS IS A MUST. "
                  "Provide exact average results, and narratives for results. "
                  "Do not worry about graph colors, focus on content.")

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


def trimFASTQ(agentExecutor):
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = (
            "Using cutadapt and the Bash command line through the subprocess command, could you remove low quality regions and adapters of FASTA file "
            f"{f}"
            "Use an appropriate nucleotide sequence. Make edits and save your results in a new file within the edits folder"
            "Example command: cutadapt -a AACCGGTT -o output.fastq input.fastq")

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


def getGenome():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/*.fa"):
        names.append(file)

    return names


def fetchGenomeAnnotation():
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/*.gtf"):
        names.append(file)

    return names


def indexGenomeHISAT(agentExecutor):
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/*.fa"):
        names.append(file)

    prompt = (
        "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')' "
        "Run the commands that create a HISAT index from "
        f"{names[0]}")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def genomeAlignmentFASTQ(agentExecutor):
    files = fetchFASTQTrimmed()

    prompts = []

    genomeName = os.path.basename(glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/*.1.ht2")[0])

    for f in files:
        prompt = (
            "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')' "
            "Using the ht2 file formats for the index at hand, align the "
            f"{f} with it. "
            f"The genome index is {genomeName}'. "
            "Produce a SAM file with the alignment outputs in the edits folder"
            "Exampl: os.system('hisat2 -x mus_musculus_index -U /Users/devam/PycharmProjects/SeqMate/data/SRR1552444_trimmed.fastq -S SRR1552444_aligned.sam")

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


def samBamConversion(agentExecutor):
    files = fetchSAMFiles()

    prompts = []

    for f in files:
        prompt = (
            "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
            f"Use Pysam to convert SAM file {f} to BAM file. Store the BAM file in the edits folder. MAKE SURE ALL BAM FILES ARE SAVED IN THE edits FOLDER."
        )

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


def getGenomeAnnotations(agentExecutor):
    genome = getGenome()[0]

    prompt = ("You are in a environment wtih HISAT and featureCounts installed. "
              "The CONDA environment is 'seqmate.' "
              "First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
              "Using wget, download JUST the genome annotation file (with extension .gtf) for"
              f"{genome} from ftp.ensembl.org and unzip it. MAKE SURE TO DOWNLOAD USING WGET AND UNZIP.")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def featureCountGeneration(agentExecutor):
    bams = fetchBAMFiles()
    annotation = fetchGenomeAnnotation()

    prompt = (
        "You are in a environment wtih HISAT and featureCounts installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'Using featureCounts, produce a count matrix using "
        f"{bams} and {annotation}. DELETE THE FIRST LINE OF THE DOCUMENT THAT CONTAINS THE COMMAND, and store it in file 'featureCounts_output.csv'"
        "Example command: 'featureCounts -p -O -T n -a example_genome_annotation.gtf -o example_featureCounts_output.out sorted_example_alignment.bam'")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def countTableColumnEdit(agentExecutor):
    bams = fetchBAMFiles()
    bams = " ".join(str(bam) for bam in bams)
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/featureCounts_output.csv"

    prompt = ("Using the "
              f"{counts}, "
              f"first open it in a pandas dataframe with a tab delimiter and setting skiprows=1. "
              f"Get rid of all columns other than Geneid, {bams}. "
              f"Get rid of rows with zeroes for the column headers {bams}' "
              f"Transpose this matrix. Export this as editedCountMatrix.csv")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def metaDataGeneration(agentExecutor, controls):
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv"

    prompt = ("Open the Pandas DataFrame "
              f"{counts}, skip the first line."
              f"and put the first column of the dataset in a column titled 'Sample.' "
              f"Then create another column titled 'Condition' from the list "
              f"{controls}."
              f"Create a new dataframe with these two columns, and export this as 'metadata.csv'")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def diffExp(agentExecutor):
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv"
    metadata = "/Users/devam/PycharmProjects/seqMateFrontEnd/metadata.csv"

    prompt = ("Using pydeseq2.dds, create a DeseqDataSet object with the counts "
              f"{counts} file being loaded into a Pandas Dataframe with the first line skipped and the first column dropped."
              f"the metadata being the {metadata} loaded into a Pandas Dataframe, and design_factors being 'Condition.' Here is some example code:"
              "dds = DeseqDataSet(counts=counts, metadata=metadata, design_factors='Condition'). Then run dds.deseq2(). Then, using pydeseq.ds, run DeseqStats on the the dds object using stat_res = DeseqStats(dds, contrast=('Condition', 'NC', 'C')). Generate a summary of the stats through stat_res.summary() and store the results dataframe of stat_res.results_df in a csv file titled deseq2Results.csv")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def summaryStatsEdit(agentExecutor):
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv"
    results = "/Users/devam/PycharmProjects/seqMateFrontEnd/deseq2Results.csv"

    prompt = ("You have access to running queries using PubMed. Open the summary stats found at "
              f"{results} "
              "and add the column headers of the "
              f"{counts} "
              "as the first column of the summary stats. "
              "Title this column as 'Genes'. Then, save the updated summary stats as a csv file at the same location")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def filter(agentExecutor, log2FoldChange, pvalue):
    results = "/Users/devam/PycharmProjects/seqMateFrontEnd/updated_deseq2Results.csv"

    prompt = ("Using "
              f"{results}, "
              f"store the entries with high log2FoldChange "
              f"(greater than {log2FoldChange}) and "
              f"low pvalue (less than {pvalue}) "
              f"in an external CSV file titled 'greatestContributors.csv")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def generateUniprotSummaries(agentExecutor):
    df = pd.read_csv("/Users/devam/PycharmProjects/seqMateFrontEnd/greatestContributors.csv")
    df = df.T
    genes = df.head(1).to_string(header=False)

    prompt = ("For all the genes in "
              f"{genes}, use the gget package to get information about each gene and store it in a Pandas Dataframe. Store save each gene's dataframe in a new folder titled 'genes.' Example: 'pd.DataFrame(gget.info('ENSMUSG00000023150')).to_csv()'")

    output = agentExecutor.invoke({'input': prompt})['output']
    return output


def generateGeneSummaries():
    names = fetchGeneInfoFiles()

    outputs = []
    for gene in names:
        agent = create_csv_agent(ChatOpenAI(model='gpt-3.5-turbo-0613'),
                                 gene,
                                 agent_type=AgentType.OPENAI_FUNCTIONS, allow_dangerous_code=True)

        outputs.append(agent.invoke(
            f"Describe {os.path.basename(gene)} using csv file {gene} through a long, three paragraph description, placing emphasis on the ensembl_description, uniprot_description, and ncbi_description. Avoid all boilerplate broad description of the structure of the data, and make it central to the given gene. Include sources mentioned in parenthesis (like PubMed:12213805) verbatim from the ensembl_description, uniprot_description, and ncbi_description columns. Example report:"
            f"The given gene, with the Ensembl ID ENSMUSG00000023150, is known as Ivns1abp or Influenza virus NS1A-binding protein homolog. It is a protein-coding gene found in Mus musculus (mouse). The gene is associated with various cellular functions, including pre-mRNA splicing, the aryl hydrocarbon receptor (AHR) pathway, F-actin organization, and protein ubiquitination (PubMed:12213805, PubMed:16317045). Ivns1abp plays a crucial role in the dynamic organization of the actin skeleton by stabilizing actin filaments through its association with F-actin (PubMed:12213805). Additionally, it protects cells from cell death induced by actin destabilization (PubMed:16952015).\n\nFurthermore, Ivns1abp acts as a modifier of the AHR pathway, increasing the concentration of the AHR available to activate transcription (By similarity). It also functions as a negative regulator of the BCR(KLHL20) E3 ubiquitin ligase complex, preventing ubiquitin-mediated proteolysis of PML and DAPK1, two tumor suppressors (By similarity). In vitro studies have shown that Ivns1abp inhibits pre-mRNA splicing (By similarity). These findings suggest that Ivns1abp may play a role in cell cycle progression in the nucleus (Ensembl description).\n\nThe uniprot_description provides additional insights into the gene's function. Ivns1abp is involved in many cell functions, including pre-mRNA splicing, the AHR pathway, F-actin organization, and protein ubiquitination. It functions as a stabilizer of actin filaments through its association with F-actin (PubMed:12213805, PubMed:16317045). It also protects cells from cell death induced by actin destabilization (PubMed:16952015). Ivns1abp acts as a modifier of the AHR pathway, increasing the concentration of AHR available to activate transcription. It functions as a negative regulator of the BCR(KLHL20) E3 ubiquitin ligase complex, preventing ubiquitin-mediated proteolysis of PML and DAPK1, two tumor suppressors. Moreover, Ivns1abp inhibits pre-mRNA splicing in vitro (Uniprot description).\n\nThe NCBI description provides additional information on the gene's localization and its orthologous relationships. Ivns1abp is located in the nucleus and is expressed in several structures, including the alimentary system, genitourinary system, musculoskeletal system, nervous system, and sensory organ. The human ortholog of Ivns1abp is implicated in immunodeficiency 70. This gene's research and findings contribute to our understanding of various cellular processes and their implications in diseases and cellular dysfunction (NCBI description).\n\nOverall, Ivns1abp is a multifunctional gene involved in pre-mRNA splicing, actin organization, protein ubiquitination, and the AHR pathway. Its role in stabilizing actin filaments and protecting cells from actin destabilization highlights its importance in maintaining cellular integrity. The gene's participation in regulating the AHR pathway and preventing proteolysis of tumor suppressors implies its potential involvement in cancer development. Further research on Ivns1abp and its interactions with other cellular components will provide valuable insights into its precise mechanisms and potential therapeutic applications.")[
                           'output'])


    return outputs
