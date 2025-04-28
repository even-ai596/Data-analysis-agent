from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.elements.models.models import llm, qwen_llm
"""
messages 
"""
messages = [
    SystemMessage(
        content="You are a helpful assistant! Your name is Bob."
    ),
    HumanMessage(
        content="Hi,I am Alice."
    ),
    AIMessage(
        content="Hi!"
    ),
    HumanMessage(
        content="what did you just say？and what's my and your name?"
    ),
    
]

print(qwen_llm.invoke(messages).content)


"""
memory
"""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph, END

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

workflow.add_edge("model", END)
# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

# 第一次对话
query = "Hi! I'm Bob."
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)

print(output["messages"][-1].content)

# 第二次对话（同一线程）
query = "What's my name?"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
print(output["messages"][-1].content)

# 切换到新线程
config = {"configurable": {"thread_id": "abc234"}}
query = "What's my name?"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
print(output["messages"][-1].content)

# 回到原线程
config = {"configurable": {"thread_id": "abc123"}}
query = "What's my name?"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
print(output["messages"][-1].content)

print(output["messages"])

