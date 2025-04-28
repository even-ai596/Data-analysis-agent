import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.elements.models.models import qwen_llm
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

@tool 
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two numbers."""
    return first_int * second_int
print(type(multiply))
tools = [multiply]

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent_executor = create_react_agent(qwen_llm, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="你好")]},stream_mode="values", config=config
):  
    print(chunk["messages"][-1])
    if "agent" in chunk:
        if chunk["agent"]["messages"][0].content:
            print(chunk["agent"]["messages"][0].content)
        else:
            print(f"调用工具...{chunk['agent']['messages'][0].additional_kwargs['tool_calls'][0]['function']['name']}")
    elif "tools" in chunk: 
        print(f"调用工具后得到以下信息：\n{chunk['tools']['messages'][0].content}")
    print("----")