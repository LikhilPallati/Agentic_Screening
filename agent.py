from tools import read_resume_file, fetch_jd_from_url
from schemas import Candidate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Load Tools, these are the functions the AI can "call", LLMs will see their docstrings and decide when to use them.
tools = [read_resume_file, fetch_jd_from_url]

# Initialize the LLM, this is the brain of the agent.
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0) # Alternative for OpenAI
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

# Setup Output Parser, This enforces the structure of the final answer.
parser = PydanticOutputParser(pydantic_object=Candidate)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
     You are an expert technical recruiter. You have access to tools to read resume files, and extract job description from the provided url.
     Extract structured resume info and score fit given a job description.
     Wrap the output in this format and provide no other text\n{format_instructions}
     """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions = parser.get_format_instructions())

# Construct the Agent. Combines the LLM, the Tools, and the Prompt into a reasoning engine.
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the Executor, It calls the Python functions (tools), and feeds the output back to the LLM.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(resume_path: str, jd_url: str):
    
    # Construct the instruction string telling the agent what to do with the inputs.
    user_input = f"""
                Please read the resume located at '{resume_path}'. Then, compare it against the Job Description found at this URL: {jd_url}.
                """

    raw_response = agent_executor.invoke({"input" : user_input})
    response = raw_response['output'][-1]['text']
    structured_response = parser.parse(response)
    response = response.strip().replace("```json", "").replace("```", "")
    print(response)

    return structured_response
