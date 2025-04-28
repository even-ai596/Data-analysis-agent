from pydantic import BaseModel, Field

class SendEmailInputSchema(BaseModel):
    email_url: str = Field(description="接收你要发送的电子邮件的电子邮件地址")
    mail_content: str = Field(description="你要发送的电子邮件的内容")

class SearchEngineInputSchema(BaseModel):
    query: str = Field(description="使用搜索引擎搜索信息时所使用的关键字")

class CrmLoginInputSchema(BaseModel):
    user_id: str = Field(description="登录客户信息系统时使用的用户名")
    password: str = Field(description="登录客户信息系统时使用的用户名对应的用户密码")

class SearchCustomerInfoInputSchema(BaseModel):
    customer_name: str = Field(description="使用客户信息系统搜索客户详细信息时所需的客户名称")
    

    
    
class SearchSQLSchema3_1(BaseModel):
    query: str = Field(description="一个与表格内容相关的问题")

class SearchTableInfoSchema3_1(BaseModel):
    sql: str = Field(description="sql语句")

class SearchSQLSchema3_2(BaseModel):
    query: str = Field(description="一个与表格内容相关的问题")
    
class SearchTableInfoSchema3_2(BaseModel):
    sql: str = Field(description="sql语句")
    
 
    