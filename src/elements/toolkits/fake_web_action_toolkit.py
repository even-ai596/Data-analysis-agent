from langchain_core.tools import BaseToolkit
from elements.tools.fake_web_action_tools import *

class FakeWebActionToolkit(BaseToolkit):
    instruction:str = \
    '''这个工具包用来进行数据分析。一般来说使用步骤如下：  
    1、用户查询与表格相关的信息时，可以使用表格内容相关的问题来查询，你在得到用户问题后，结合表格给出sql语句,；
    2、当你使用了sql查询工具后，请你将该工具输出的sql语句输入到sql运行工具中以查询表格信息；
    3、注意你需要根据表字段信息和用户输入来决定使用text_to_3_2_sql还是text_to_3_1_sql工具，不要使用错工具；
    4、如果用户的输入包括了大数据技术主键、业务主键、交易日期、交易员、业务品种、交易笔数、总损益-CNY、批次日期等，你就使用text_to_3_1_sql工具；
    5、如果用户的输入包括了、业务主键、产品代码、源系统资产代码、资产代码、ISIN代码等且不涉及到大数据技术主键、交易日期、交易员、业务品种、交易笔数、总损益-CNY、批次日期等，你就使用text_to_3_2_sql工具；
    6、使用sql运行工具后，你可以得到表格信息，然后将表格信息完整返回给用户，对于每一个字段，你都必须精确地给用户。如果需要返回的表格信息过多，你可以仅展示一部分，并向用户询问更具体的需求；
    7、当你使用了sql查询工具后如果有两个sql语句，你要执行一个sql语句后再执行另一个sql语句，不要同时执行两个sql语句。
    '''

    def get_tools(self):
        return [FakeSearchSQLInfoTool3_1(),FakeSearchTableInfoTool3_1(),FakeSearchSQLInfoTool3_2(),FakeSearchTableInfoTool3_2()]



