from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from src.elements.models.models import llm,qwen_llm
import json
# @tool  取消注释关键字传参报错
# def multiply(first_int: int, second_int: int) -> int:
#     """Multiply two numbers."""
#     return first_int * second_int

# # print(multiply.name)
# llm_with_tools = llm.bind_tools([multiply])

# msg = llm_with_tools.invoke("6的8倍")
# print(msg)
# print((msg.additional_kwargs["tool_calls"][0]["function"]["arguments"]  ) )

# print(multiply(**json.loads(msg.additional_kwargs["tool_calls"][0]["function"]["arguments"])))

# from langchain_community.chat_models.tongyi import ChatTongyi
# from langchain_core.messages import HumanMessage, SystemMessage

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "当你想知道现在的时间时非常有用。",
#             "parameters": {},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_weather",
#             "description": "当你想查询指定城市的天气时非常有用。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "城市或县区，比如北京市、杭州市、余杭区等。",
#                     }
#                 },
#             },
#             "required": ["location"],
#         },
#     },
# ]

# messages = [
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="What is the weather like in San Francisco?"),
# ]

# llm_kwargs = {"tools": tools, "result_format": "message"}
# ai_message = qwen_llm.bind(**llm_kwargs).invoke(messages)
# print(ai_message)





from langchain_core.tools import tool
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from langchain_core.messages import HumanMessage,ToolMessage

from src.elements.models.models import llm,qwen_llm
import json
@tool 
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two numbers."""
    return first_int * second_int

# print(multiply.name)
llm_with_tools = qwen_llm.bind_tools([multiply])
messages =[
    HumanMessage(content="6的8倍是多少"),
]
ai_msg = llm_with_tools.invoke(messages)
print(([ai_msg][0]))  # 输出结果\
print(type(HumanMessage(content="6的8倍是多少")))
messages.append(ai_msg)  # 将工具调用的消息添加到消息列表中
# 自动处理工具调用流程
print(ai_msg.tool_calls)  # 输出结果
tool_call = ai_msg.tool_calls[0]
tool_msg = multiply.invoke(tool_call["args"])  # 自动解析参数
messages.append(ToolMessage(content=(tool_msg),tool_call_id=tool_call["id"]))  # 将工具调用的消息添加到消息列表中
print(messages)  # 输出结果
print(qwen_llm.invoke(messages).content) # 输出结果


