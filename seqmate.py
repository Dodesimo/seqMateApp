# Helper functions for the back end.
import glob
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
import os


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
        outputs.append(agentExecutor.invoke({"input":prompt})['output'])

    return outputs

#To do for flask frontend: display graphs.
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
        prompt = ("Using cutadapt and the Bash command line through the subprocess command, could you remove low quality regions and adapters of FASTA file "
                  f"{f}"
                  "Use an appropriate nucleotide sequence. Make edits and save your results in a new file within the /Users/devam/PycharmProjects/seqMateFrontEnd/edits folder"
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

def indexGenomeHISAT(agentExecutor):
    names = []
    for file in glob.glob("/Users/devam/PycharmProjects/seqMateFrontEnd/uploads/*.fa"):
        names.append(file)

    prompt = ("You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')' "
              "Run the commands that create a HISAT index from "
              f"{names[0]}")

    output = agentExecutor.invoke({"input":prompt})['output']
    return output

def genomeAlignmentFASTQ(agentExecutor):
    files = fetchFASTQNames()

    prompts = []

    genome = getGenome()[0]

    for f in files:
        prompt = (
            "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')' "
            "Using the ht2 file formats for the genome at hand, align the "
            f"{f} with it. "
            f"The genome index is {genome}'. "
            "Produce a SAM file with the alignment outputs  in the edits folder")

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs

def samBamConversion(agentExecutor):
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = (
            "You are in a environment wtih HISAT installed. The CONDA environment is 'seqmate.' First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
            f"Use Pysam to convert SAM file {f} to BAM file. Store these files in the edits folder")

        prompts.append(prompt)

    outputs = []

    for prompt in prompts:
        outputs.append(agentExecutor.invoke({"input": prompt})['output'])

    return outputs

def getGenomeAnnotations(agent):
    files = fetchFASTQNames()

    prompts = []

    for f in files:
        prompt = ("You are in a environment wtih HISAT and featureCounts installed. "
                  "The CONDA environment is 'seqmate.' "
                  "First, do 'os.system('pyenv local miniforge3-22.11.1-4/envs/seqmate')'"
                  "Using wget, download JUST the genome annotation file (with extension .gtf) for /Users/devam/PycharmProjects/SeqMate/data/mus_musculus_genome.fa and unzip it.")