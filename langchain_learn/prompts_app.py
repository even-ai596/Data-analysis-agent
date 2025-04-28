# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from src.elements.models.models import llm,qwen_llm
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# prompt_template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "你是一个海盗，说话像海盗一样",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
# workflow = StateGraph(state_schema=MessagesState)


# def call_model(state: MessagesState):
#     prompt = prompt_template.invoke(state)
#     response = llm.invoke(prompt)
#     return {"messages": response}


# workflow.add_edge(START, "model")
# workflow.add_node("model", call_model)

# memory = MemorySaver()
# app = workflow.compile(checkpointer=memory)

# config = {"configurable": {"thread_id": "abc345"}}
# query = "你好，我是Jim."

# input_messages = [HumanMessage(query)]
# output = app.invoke({"messages": input_messages}, config)
# output["messages"][-1].pretty_print()

# query = "我是谁"

# input_messages = [HumanMessage(query)]
# output = app.invoke({"messages": input_messages}, config)
# output["messages"][-1].pretty_print()




# """
# 加入language
# """
# from typing import Sequence
# from langchain_core.messages import BaseMessage
# from langgraph.graph.message import add_messages
# from typing_extensions import Annotated, TypedDict
# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from src.elements.models.models import llm,qwen_llm
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# class State(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]
#     language: str


# workflow = StateGraph(state_schema=State)

# prompt_template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
# def call_model(state: State):
#     prompt = prompt_template.invoke(state)
    
#     response = llm.invoke(prompt)
    
#     return {"messages": [response]}
    


# workflow.add_edge(START, "model")
# workflow.add_node("model", call_model)

# memory = MemorySaver()
# app = workflow.compile(checkpointer=memory)


# config = {"configurable": {"thread_id": "abc456"}}
# query = "Hi I'm Todd, please tell me a joke."
# language = "Chinese"    

# input_messages = [HumanMessage(query)]
# # # 非流式输出
# # output = app.invoke(
# #     {"messages": input_messages, "language": language},
# #     config,
# # )
# # output["messages"][-1].pretty_print()
# # print(output)
# # 流式输出
# for chunk, metadata in app.stream(
#     {"messages": input_messages, "language": language},
#     config,
#     stream_mode="messages",
# ):
#     if isinstance(chunk, AIMessage):  # Filter to just model responses
#         print(chunk.content,end="")


"""
trimming
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, trim_messages
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Sequence ,Annotated,TypedDict
from langgraph.graph import START, MessagesState, StateGraph
from src.elements.models.models import llm,qwen_llm
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


workflow = StateGraph(state_schema=State)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
trimmer = trim_messages(
    max_tokens=35,
    strategy="last",
    token_counter=qwen_llm,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    HumanMessage(content="hi! I'm bob", additional_kwargs={}, response_metadata={}),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

print(type(trimmer.invoke(messages)))

workflow = StateGraph(state_schema=State)


def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    print((prompt),"asss")
    response = qwen_llm.invoke(prompt)
    return {"messages": [response]}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc567"}}
query = "What is my name?"
query = "What math problem did I ask?"
language = "english"

input_messages = messages + [HumanMessage(query)]
output = app.invoke(
    {"messages": input_messages, "language": language},
    config,
)
output["messages"][-1].pretty_print()
print(output)