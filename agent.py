from tools import read_resume_file, fetch_jd_from_url
from schemas import Candidate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

tools = [read_resume_file, fetch_jd_from_url]

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

parser = PydanticOutputParser(pydantic_object=Candidate)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
     You are an expert technical recruiter. You have access to tools to read resume files, and extract job description from the provided url.
     Extract structured resume info and score fit given a job description.
     Wrap the output in this format and provide no other text\n{format_instructions}
     """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions = parser.get_format_instructions())

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(resume_path: str, jd_url: str):

    user_input = f"""
                Please read the resume located at '{resume_path}'. Then, compare it against the Job Description found at this URL: {jd_url}.
                """

    raw_response = agent_executor.invoke({"input" : user_input})

    response = raw_response['output'][-1]['text']

    structured_response = parser.parse(response)

    response = response.strip().replace("```json", "").replace("```", "")

    print(response)

    return structured_response