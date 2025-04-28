# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langgraph.checkpoint.memory import MemorySaver
from elements.models.models import llm,qwen_llm,qwen_14B_local,qwen_local
from elements.toolkits.fake_web_action_toolkit import FakeWebActionToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

memory = MemorySaver()

toolkit = FakeWebActionToolkit()
tools = toolkit.get_tools()

system_prompt = SystemMessage(toolkit.instruction)

ysx_react_agent = create_react_agent(model=qwen_llm,tools=tools,state_modifier=system_prompt,checkpointer=memory)

