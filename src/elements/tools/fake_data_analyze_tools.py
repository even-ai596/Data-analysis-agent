from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel
from ysx_agent.src.elements.models.models import llm
from ysx_agent.src.elements.pydantic_models.kaimei_data_tool_schemas import *
from ysx_agent.src.elements.prompts.kaimei_data_analyze_prompts.Gpt4o.prompts import *
from langchain_core.output_parsers import PydanticOutputParser

class FindProperTablesTool(BaseTool):
    name: str = "find_proper_tables"
    description: str = "分析一个问题和众多候选表的信息，选择能够用于回答该问题的表。"
    args_schema: Type[BaseModel] = FindProperTablesInputSchema

    def _run(
            self, a_question: str,table_info: Dict[str,Any]) -> str:
        """Use the tool."""
        input_prompt = FIND_PROPER_TABLE_PROMPT.format(table_info=str(table_info), a_question=a_question)
        model_output = llm.invoke(input_prompt=input_prompt).content

        return ["13375869204","15482239485","15844434566"]

    async def _arun(
            self,
            a_question: str,
            table_info: Dict[str, Any]
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(a_question,table_info)

class GenerateSqlTool(BaseTool):
    pass

class CheckSqlTool(BaseTool):
    pass

