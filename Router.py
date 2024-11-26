from typing import Any

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from code import agent_executor
from Readcsv import csv_agent_executor
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

load_dotenv()
def python_agent_executor_wrapper(original : str) -> dict[str, Any]:
    return agent_executor.invoke(input={"input" : original})


tools = [
    Tool(
        name="Python Agent",
        func=python_agent_executor_wrapper,
        description="자연어를 파이썬 코드로 변환하고 실행하여 코드 실행결과를 반환할 때 유용해.  입력으로 코드를 받지 않아."
    ),
    Tool(
        name="CSV Agent",
        func=csv_agent_executor,
        description="개발자들에 대한 정보를 참조하고싶을때 유용해."
    )
]

base_prompt = hub.pull("langchain-ai/react-agent-template")
promps = base_prompt.partial(instructions="")

control_agent = create_react_agent(
    prompt=promps,
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=tools,
)

control_agent_executor = AgentExecutor(agent=control_agent, tools=tools, verbose=True)

input_query = "개발자들이 애용하는 기술스택 알려줘"

res = control_agent_executor.invoke(input={"input": input_query})

print(res['output'])