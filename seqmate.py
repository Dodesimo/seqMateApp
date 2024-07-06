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
    Strictly follow the prompt instructions, and make sure all code is actually ran and outputs are produced. Be consistent in the code you are writing and executing for each file/entry/call.
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
    example = "import matplotlib.pyplot as plt import numpy as np import seaborn as sns import pandas as pd fastq_file = '/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/SRR1552445.fastq' phred_scores = [] duplication_rates = [] sequence_lengths = [] for record in SeqIO.parse(fastq_file, 'fastq'): phred_scores.extend(record.letter_annotations['phred_quality']) sequence_lengths.append(len(record.seq)) phred_scores_mean = np.mean(phred_scores) phred_scores_std = np.std(phred_scores) duplication_rate = 1 - len(set(phred_scores)) / len(phred_scores) plt.figure(figsize=(14, 6)) plt.subplot(1, 3, 1) sns.histplot(phred_scores, kde=True) plt.xlabel('Phred Score') plt.ylabel('Frequency') plt.title('Distribution of Phred Scores') plt.subplot(1, 3, 2) sns.histplot(sequence_lengths, kde=True) plt.xlabel('Sequence Length') plt.ylabel('Frequency') plt.title('Distribution of Sequence Lengths') plt.subplot(1, 3, 3) sns.barplot(x=['Duplication Rate'], y=[duplication_rate]) plt.ylabel('Rate') plt.title('Duplication Rate') plt.tight_layout() plt.show() phred_scores_mean, phred_scores_std, duplication_rate` I have conducted quality control analysis of the FASTQ file 'SRR1552445.fastq' using Bio. Here are the results: - **Average Phred Score**: 32.38 - **Standard Deviation of Phred Scores**: 3.89 - **Duplication Rate**: 0.99 ### Interpretation of Results: 1. **Phred Score Distribution**: - The distribution of Phred scores in the FASTQ file shows that the average Phred score is 32.38, indicating good quality scores across the sequences. 2. **Sequence Length Distribution**: - The distribution of sequence lengths in the file indicates the variability in the length of sequences present. 3. **Duplication Rate**: - The high duplication rate of 0.99 suggests that there is a high level of redundancy in the sequences, which may impact downstream analysis and should be considered during data processing. The graphs/charts provided illustrate the distributions of Phred scores and sequence lengths, along with the calculated duplication rate."
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = ("Using Bio, conduct quality control analysis of FASTA file "
                  f"{f}."
                  "Generate and execute all code using the Python REPL tool, do not ask the user to run it on their end. IMPORT ALL PACKAGES PROPERLY. For example, 'import matplotlib as plt' should be the first line of your code. GENERATE ALL OUTPUTS. MAKE SURE TO PROVIDE GRAPHICS/CHARTS AND PROVIDE NARRATION."
                  f"BE CONSISTENT IN THE WAY YOU GENERATE AND RUN CODE FOR ALL FASTA FILES. THE CODE SHOULD STRICTLY BE FOLLOWING: {example}. THE PYTHON REPL WILL ALWAYS GENERATE AN OUTPUT FOR YOUR CODE. DO NOT SAY THAT SOMETHING IS NOT AVAILABLE OR CODE IS NOT OUTPUTTING VALUES. EVERYTHING SHOULD WORK.")

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
            "Use an appropriate nucleotide sequence. Make edits and save your results in a new file with '_trimmed' at the end of the original file name within the /Users/devam/PycharmProjects/seqMateFrontEnd/edits folder. ACTUALLY RUN THE COMMAND. DO NOT END THE CHAIN BEFORE THE COMMAND HAS BEEN RAN."
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

    genomeName = os.path.splitext(
        os.path.basename(glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/*.genome.fa")[0]))[0]

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
    codeExample = "sam_file = '/Users/devam/PycharmProjects/seqMateFrontEnd/edits/SRR1552445_aligned.sam' bam_file = '/Users/devam/PycharmProjects/seqMateFrontEnd/edits/SRR1552445_aligned.bam' with pysam.AlignmentFile(sam_file, 'r') as samfile, pysam.AlignmentFile(bam_file, 'wb', template=samfile) as bamfile: for read in samfile: bamfile.write(read)"
    prompts = []

    for f in files:
        prompt = (
            "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
            f"Use Pysam to convert SAM file {f} to BAM file. Store the BAM file in the edits folder. RUN THE COMMAND PROPERLY. MAKE SURE ALL BAM FILES ARE SAVED IN THE /Users/devam/PycharmProjects/seqMateFrontEnd/edits FOLDER. Example code: {codeExample}. DO NOT TERMINATE THE CHAIN UNLESS THE CODE IS ACTUALLY RAN. USE THIS CODE FOR ALL TASKS."
        )

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs


def getGenomeAnnotations(agentExecutor):
    genome = getGenome()[0]

    prompt = ("You are in a environment wtih HISAT and featureCounts installed."
              "The CONDA environment is 'seqmate.' "
              "First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
              "Using wget, download JUST the genome annotation file (with extension .gtf) for"
              f"{genome} from ftp.ensembl.org and unzip it. MAKE SURE TO DOWNLOAD USING WGET CORRECTLY AND UNZIP INTO /Users/devam/PycharmProjects/seqMateFrontEnd.")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def featureCountGeneration(agentExecutor):
    bams = fetchBAMFiles()
    annotation = fetchGenomeAnnotation()

    prompt = (
        "You are in a environment wtih HISAT and featureCounts installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'Using featureCounts, produce a count matrix using "
        f"command featureCounts -p -O -T {len(bams)} -a {annotation} -o featureCounts_output.csv {bams}. DO NOT TERMINATE THE CHAIN UNTIL THE COMMAND IS ACTUALLY RAN.")

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
    bams = sorted(fetchBAMFiles())

    prompt = (f"Put {bams} in a column titled 'Sample.'"
              f"Then create another column titled 'Condition' from the list "
              f"{controls}."
              f"Create a new dataframe with these two columns, and export this as 'metadata.csv'")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def diffExp(agentExecutor):
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv"
    metadata = "/Users/devam/PycharmProjects/seqMateFrontEnd/metadata.csv"

    prompt = ("Using pydeseq2.dds, create a DeseqDataSet object with the counts "
              f"{counts} file being loaded into a Pandas Dataframe with the first line skipped. ENSURE THAT THE FIRST COLUMN IS DROPPED."
              f"the metadata being the {metadata} loaded into a Pandas Dataframe, and design_factors being 'Condition.' Here is some example code:"
              "import pandas as pd from pydeseq2 import dds, ds counts = pd.read_csv('/Users/devam/PycharmProjects/SeqMate/editedCountMatrix.csv') metadata = pd.read_csv('/Users/devam/PycharmProjects/SeqMate/metadata.csv') dds = dds.DeseqDataSet(counts=counts, metadata=metadata, design_factors='Condition') dds.deseq2() stat_res = ds.DeseqStats(dds, contrast=('Condition', 'NC', 'C')) summary = stat_res.summary() results_df = stat_res.results_df results_df.to_csv('deseq2Results.csv', index=False). Generate a summary of the stats through stat_res.summary() and store the results dataframe of stat_res.results_df (INCLUDING ALL GENE NAMES) in a csv file titled deseq2Results.csv. STRICTLY FOLLOW THE EXAMPLE CODE.")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def summaryStatsEdit(agentExecutor):
    counts = "/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv"
    results = "/Users/devam/PycharmProjects/seqMateFrontEnd/deseq2Results.csv"

    prompt = ("You have access to running queries using PubMed. Open the summary stats found at "
              f"{results} "
              "and drop the first column of "
              f"{counts}. Then, set the first row"
              f"as the first column of {results} stats. Do this using deseq2_results['Genes'] = pd.Series(edited_count_matrix.iloc[0].values)"
              "Title this column as 'Genes'. Then, save the updated summary stats as 'updated_deseq2Results' at the same location. Example code: import pandas as pd # Load the editedCountMatrix.csv file edited_count_matrix = pd.read_csv('/Users/devam/PycharmProjects/seqMateFrontEnd/editedCountMatrix.csv') # Drop the first column edited_count_matrix = edited_count_matrix.drop(columns=edited_count_matrix.columns[0]) edited_count_matrix.head() deseq2_results = pd.read_csv('/Users/devam/PycharmProjects/seqMateFrontEnd/deseq2Results.csv') deseq2_results['Genes'] = edited_count_matrix.iloc[0] deseq2_results edited_count_matrix.iloc[0] deseq2_results['Genes'] = pd.Series(edited_count_matrix.iloc[0].values). USE THIS EXAMPLE STRICTLY.")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def filter(agentExecutor, log2FoldChange, pvalue, numberOfGenes):
    results = "/Users/devam/PycharmProjects/seqMateFrontEnd/updated_deseq2Results.csv"

    prompt = ("Using "
              f"{results}, "
              f"store ONLY THE TOP {numberOfGenes} entries with high log2FoldChange "
              f"(greater than {log2FoldChange}) and "
              f"low pvalue (less than {pvalue}) "
              f"low pvalue (less than {pvalue}) "
              f"in an external CSV file titled 'greatestContributors.csv")

    output = agentExecutor.invoke({"input": prompt})['output']
    return output


def generateUniprotSummaries(agentExecutor, topNGenes):
    df = pd.read_csv("/Users/devam/PycharmProjects/seqMateFrontEnd/greatestContributors.csv")
    df = df.T
    genes = df.head(1).to_string(header=False)

    prompt = (f"For all {topNGenes} genes in "
              f"{genes}, use the gget package to get information about each gene and store it in a Pandas Dataframe. Store save each gene's dataframe in a new folder titled 'genes.' Example: 'pd.DataFrame(gget.info('ENSMUSG00000023150')).to_csv()' USE THIS EXAMPLE FOR ALL INSTANCES.")

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
