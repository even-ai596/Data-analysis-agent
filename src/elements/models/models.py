from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from langchain_openai import ChatOpenAI
from langchain_community.llms import VLLMOpenAI
# load_dotenv()
from langchain_core.messages import HumanMessage
AZURE_OPENAI_CHAT_API_KEY = os.getenv("AZURE_OPENAI_CHAT_API_KEY","")
AZURE_OPENAI_CHAT_ENDPOINT = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT","")
AZURE_OPENAI_CHAT_API_VERSION = os.getenv("AZURE_OPENAI_CHAT_API_VERSION","")

llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_CHAT_API_KEY,
    azure_endpoint=AZURE_OPENAI_CHAT_ENDPOINT,
    azure_deployment="gpt-4o",
#   base_url = "https://uniaction.openai.azure.com/openai/deployments/gpt-4o"
    api_version=AZURE_OPENAI_CHAT_API_VERSION,
    temperature=0.1,
)



qwen_14B_local = ChatOpenAI(
        base_url="http://222.128.28.85:32701/v1",
        api_key="EMPTY",
        model="Qwen2.5-14B-Instruct-GPTQ-Int4"
)
qwen_local = ChatOpenAI(
        base_url="http://192.168.0.94:8811/v1",
        api_key="EMPTY",
        model="Qwen2.5-0.5B-Instruct"
)
qwen_llm = ChatTongyi(model="qwen2.5-72b-instruct",api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
if __name__ == "__main__":
        
        print(qwen_llm.invoke("什么是langchain？").content)
# 流失输出
        # for chunk in qwen_llm.stream("我喜欢编程。"):
        #     print(chunk)
        
#       res = qwen_llm.stream([HumanMessage(content="hi")], streaming=True)
#       for r in res:
#             print("chat resp:", r.content)
        
      
        
