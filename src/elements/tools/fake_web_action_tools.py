from typing import Type, Optional, Callable



from langchain_community.tools import HumanInputRun
from elements.models.models import llm
from elements.pydantic_models.tool_input_schemas import SendEmailInputSchema, SearchEngineInputSchema, \
    SearchCustomerInfoInputSchema, CrmLoginInputSchema ,SearchTableInfoSchema3_1,SearchSQLSchema3_1,SearchSQLSchema3_2,SearchTableInfoSchema3_2
from langchain_core.tools import BaseTool
from pydantic import BaseModel
import pandas as pd
import pandasql as psql
en_to_zh_tool_name_dict = {"send_email_tool": "邮件发送工具", "search_engine_tool": "搜索引擎工具",
                           "CRM_system_login_tool": "CRM登录工具",
                           "use_name_to_search_customer_info": "使用姓名搜索CRM内客户信息工具",
                           'run_3_1_sql_tool':'表3_1_sql运行工具',
                           'text_to_3_1_sql':'表3_1_sql查询工具',
                           'run_3_2_sql_tool':'表3_2_sql运行工具',
                           'text_to_3_2_sql':'表3_2_sql查询工具'}

ask_human_tool = HumanInputRun(name="ask_human",description="当你有任何疑问时使用此工具询问用户。你的输入必须是一个向用户询问的问题。")

class FakeSendEmailTool(BaseTool):
    name: str = "send_email_tool"
    description: str = "将一封邮件内容发送到一个邮件地址。"
    args_schema: Type[BaseModel] = SendEmailInputSchema

    def _run(
            self, email_url: str, mail_content: str) -> str:
        """Use the tool."""
        return "成功发送一封邮件到" + email_url + "\n内容为：\n\n" + mail_content

    async def _arun(
            self,
            email_url: str, mail_content: str
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(email_url, mail_content)


class FakeSearchEngineTool(BaseTool):
    name: str = "search_engine_tool"
    description: str = "使用搜索引擎搜索一些相关信息。"
    args_schema: Type[BaseModel] = SearchEngineInputSchema

    def _run(
            self, query: str) -> str:
        """Use the tool."""
        pretend_to_be_search_engine_prompt = \
            f'''假设你是一个万能的搜索引擎，下面是一条用户输入的搜索关键字：
            {query}
            根据这些关键字，回复用户一些相关信息。
            '''
        return llm.invoke(pretend_to_be_search_engine_prompt).content

    async def _arun(
            self,
            query: str
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(query)


class FakeCrmLoginTool(BaseTool):
    name: str = "CRM_system_login_tool"
    description: str = "使用该工具可以通过用户名及密码登录进客户信息管理系统。"
    args_schema: Type[BaseModel] = CrmLoginInputSchema

    def _run(
            self, user_id: str, password: str) -> str:
        """Use the tool."""
        if user_id == "admin" and password == "admin":
            return "成功登陆客户信息管理系统！"
        else:
            return "账户名或密码错误，登录失败！"

    async def _arun(
            self,
            user_id: str, password: str
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(user_id, password)


class FakeSearchCustomerInfoTool(BaseTool):
    name: str = "use_name_to_search_customer_info"
    description: str = "通过客户名称，获取客户信息，包括客户的电子邮件地址。使用前必须先登录客户信息管理系统。"
    args_schema: Type[BaseModel] = SearchCustomerInfoInputSchema

    def _run(
            self, customer_name: str) -> str:
        """Use the tool."""
        customer_info = {
            "姓名": customer_name,
            "email": "yanshengxing@gmail.com"
        }
        return str(customer_info)

    async def _arun(
            self,
            customer_name: str
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(customer_name)
class ToolException(Exception):
    """Custom exception class for tool errors."""
    pass
class FakeSearchSQLInfoTool3_1(BaseTool):
    name: str = "text_to_3_1_sql"
    description: str = "通过一个与表3_1相关的问题，得到sql查询语句"
    args_schema: Type[BaseModel] = SearchSQLSchema3_1
    
    

    def _run(self, query: str) -> str:
        
            file_path = '../test.xlsx'  # 替换为您的Excel文件路径
            fds_tbm_pl_trader_daily = pd.read_excel(file_path)
            
            # 去掉列名的前后空格，避免隐形字符的问题
            fds_tbm_pl_trader_daily.columns = fds_tbm_pl_trader_daily.columns.str.strip()
            
            # 只提取表头（列名）
            table_headers = self.get_table_headers(fds_tbm_pl_trader_daily)
            
            prompt = f'''你是一个顶尖的数据分析专家，非常擅长使用sql语言，从数据表中查询数据回答用户问题。
            以下是一个表字段的相关元数据信息：
            
            {table_headers}
            
            表字段中英文对照如下：
            row_no：大数据技术主键
            bid：业务主键
            trade_date：交易日期
            trader_name：交易员
            biz_type：业务品种
            trade_cnt：交易笔数
            pl_all_cny：总损益-CNY
            data_batch_date：批次日期
            
            接下来用户向你提出了以下问题：
            
            {query}
            
            现在你需要完成以下任务：
            根据用户问题和表格字段，给出一个完整的SQL查询语句。
            
            请严格遵循以下原则：
            1. 请根据表格字段给出完整的SQL查询语句,特别是表格中的字段名称不能遗漏；
            2. 注意不要生成除了sql以外的其他内容；
            3. 表名为:fds_tbm_pl_trader_daily；
            4. 当用户查询某个时间点的数据时，时间格式为'2022-01-05 00:00:00.000000'。
            '''
            
            return llm.invoke(prompt).content
        
       

    def get_table_headers(self, df: pd.DataFrame) -> str:
        # 只提取表头（列名）并转化为文本格式
        table_headers = ", ".join(df.columns)  # 以逗号分隔的列名字符串
        return table_headers

    async def _arun(self, query: str) -> str:
        return self._run(query)


class FakeSearchTableInfoTool3_1(BaseTool):
    name: str = "run_3_1_sql_tool"
    description: str = "3_1_sql运行工具"
    args_schema: Type[BaseModel] = SearchTableInfoSchema3_1

    def __init__(self, handle_tool_error: Optional[Callable[[ToolException], str]] = None):
        super().__init__()
        # 如果没有传入异常处理函数，使用默认打印
        self.handle_tool_error = handle_tool_error or self.default_error_handler

    def default_error_handler(self, exception: ToolException) -> str:
        """默认的错误处理函数，打印异常信息"""
        print("工具调用异常")
        return "工具调用异常"
    def _run(self, sql: str) -> str:
        """
        根据输入的 SQL 查询语句和表格路径，返回查询结果。

        Args:
            sql (str): SQL 查询语句

        Returns:
            str: 查询结果字符串
        """
        fds_tbm_pl_trader_daily = pd.read_excel('../test.xlsx')
        pd.set_option('display.max_rows', None)  # 显示所有行
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.width', None)  # 自动调整宽度
        pd.set_option('display.max_colwidth', None)  # 显示完整的列内容
        

        # 使用 pandasql 执行 SQL 查询，并明确指定 DataFrame 'df' 为 SQL 表名
        result = psql.sqldf(sql, locals())

        
                
        
       
                
        # 调用大语言模型进行处理
        return result
    
    async def _arun(self, sql: str) -> str:
        return self._run(sql)
    
      
class FakeSearchSQLInfoTool3_2(BaseTool):
    name: str = "text_to_3_2_sql"
    description: str = "通过一个与表3_2相关的问题，得到sql查询语句"
    args_schema: Type[BaseModel] = SearchSQLSchema3_2
    
    def _run(self, query: str) -> str:
        file_path = '../test.xlsx'  # 替换为您的Excel文件路径
        sec_bond_info = pd.read_excel(file_path, sheet_name=1)
        
        # 去掉列名的前后空格，避免隐形字符的问题
        sec_bond_info.columns = sec_bond_info.columns.str.strip()
        
        # 只提取表头（列名）
        table_headers = self.get_table_headers(sec_bond_info)
        
        prompt = f'''你是一个顶尖的数据分析专家，非常擅长使用sql语言，从数据表中查询数据回答用户问题。
        以下是一个表字段的相关元数据信息：
        
        {table_headers}
        
        表字段中英文对照如下：
        bid：业务主键
        product_code：产品代码
        src_asset_code：源系统资产代码
        asset_code：资产代码
        isin_code：ISIN代码
        wind_code：万得代码
        bond_short_name：债券简称
        bond_full_name：债券全称
        bond_accounting_class：债券核算分类
        bond_primary_class：债券一级分类
        currency_code：货币代码
        exchange_place：交易场所
        notional：名义本金
        country_code：国家代码
        region_code：行政区划代码
        value_date：起息日期
        maturity_date：到期日期
        listing_date：上市日期
        calendar_code：日历代码
        main_debtor：主要债务人
        bond_custody_org：债券托管机构
        issuer_entity_code：发行人实体代码
        issue_date：发行日期
        issue_amount：发行量
        issue_times：发行次数
        issue_mode：发行方式
        issue_price：发行价格
        issue_yield：发行收益率
        current_price：当前价格
        term_code：期限代码
        term_days：期限天数
        remain_term_days：剩余期限天数
        bond_face_value：债券面值
        latest_face_value：最新面值
        coupon_type：息票类型
        coupon_rate：票面利率
        industry_class_csrc1：行业分类-证监会1
        industry_class_csrc2：行业分类-证监会2
        asset_five_classification：资产五级分类
        is_credit_bond_flag：信用债标志
        
        接下来用户向你提出了以下问题：
        
        {query}
        
        现在你需要完成以下任务：
        根据用户问题和表格字段，给出一个完整的SQL查询语句。
        
        请严格遵循以下原则：
        1. 请根据表格字段给出完整的SQL查询语句,特别是表格中的字段名称不能遗漏；
        2. 注意不要生成除了sql以外的其他内容；
        3. 表名为:sec_bond_info；	
        '''
        
        return llm.invoke(prompt).content
    
    def get_table_headers(self, df: pd.DataFrame) -> str:
        # 只提取表头（列名）并转化为文本格式
        table_headers = ", ".join(df.columns)  # 以逗号分隔的列名字符串
        return table_headers

    async def _arun(self, query: str) -> str:
        return self._run(query)

class FakeSearchTableInfoTool3_2(BaseTool):
    name: str = "run_3_2_sql_tool"
    description: str = "表3_2_sql运行工具"
    args_schema: Type[BaseModel] = SearchTableInfoSchema3_2

    def _run(self, sql: str) -> str:
        """
        根据输入的 SQL 查询语句和表格路径，返回查询结果。

        Args:
            sql (str): SQL 查询语句

        Returns:
            str: 查询结果字符串
        """
        sec_bond_info = pd.read_excel('../test.xlsx', sheet_name=1)

        pd.set_option('display.max_rows', None)  # 显示所有行
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.width', None)  # 自动调整宽度
        pd.set_option('display.max_colwidth', None)  # 显示完整的列内容

        # 使用 pandasql 执行 SQL 查询，并明确指定 DataFrame 'df' 为 SQL 表名
        result = psql.sqldf(sql, locals())
        if 'total_pl_all_cny' in result.columns:
            result['total_pl_all_cny'] = result['total_pl_all_cny'].apply(lambda x: round(x, 2))

        return result
        
        
                
        
       
                
        # 调用大语言模型进行处理
        return result   
    
    async def _arun(self, sql: str) -> str:
        return self._run(sql)