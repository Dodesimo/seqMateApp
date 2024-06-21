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

