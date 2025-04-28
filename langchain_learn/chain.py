import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../"))
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.elements.models.models import llm,qwen_llm

"""
from_template 
"""
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

chain = prompt | qwen_llm | StrOutputParser()
analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

composed_chain = {"joke": chain} | analysis_prompt | qwen_llm| StrOutputParser()
print(chain.invoke({"topic": "hello"}))
print(composed_chain.invoke({"topic": "hello"}))


"""
from_messages 1
"""

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
print(prompt_template.invoke({"language": "Italian", "text": "hi!"}))

chain = prompt_template | llm
print(chain.invoke({"language": "Italian", "text": "hi!"}).content)

# or

prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
print((prompt))
print(llm.invoke(prompt).content)

"""
from_messages 2
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | qwen_llm
print(chain.invoke(
    {
        "input_language": "English",
        "output_language": "chinese",
        "input": "I love programming.",
    }
).content)



