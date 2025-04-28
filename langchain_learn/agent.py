from langchain_community.tools.tavily_search import TavilySearchResults
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.elements.models.models import llm
from langchain_core.messages import HumanMessage


search = TavilySearchResults(max_results=2)
# search_results = search.invoke("what is the weather in SF")
# print(search_results) # ToolMessage
# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.
tools = [search]

# model_with_tools = llm.bind_tools(tools)

# response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])

# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob!")]}, config
):
    print(chunk["agent"]["messages"][0].content)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats my name?")]}, config
):
    print(chunk)
    print("----")