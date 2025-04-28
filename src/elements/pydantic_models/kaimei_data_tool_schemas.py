from pydantic import BaseModel, Field
from typing import List, Dict,Any

class FindProperTablesInputSchema(BaseModel):
    a_question:str = Field(description="一个问题")
    table_info: Dict[str,Any] = Field(description="一系列表的信息，从这一系列表当中选择有助于回答上述问题的表。")