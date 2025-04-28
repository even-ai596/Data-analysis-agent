from langchain_core.tools import BaseTool
def web_work_flow_wrapper(web_work_flow_id:str) -> BaseTool:
    # 传入一个web工作流的ID,返回一个tool，目标是让LLM可以调用web工作流并获得调用结果。
    # TODO
    # 1、根据web工作流的ID，获取该web工作流的名称，描述作为tool的名称与描述(注：openAI tool calling不支持tool name为非英文)

    # 2、获取web工作流具体内容，解析其所需输入参数并动态转化生成tool输入args_schema

    # 3、实现tool的核心运行逻辑_run与其异步调用_arun，需要考虑定义/如何获取web工作流的输出结果。web工作流执行中断本身也可为一种结果，大模型可
    # 分析该结果随机应变做出下一步决断。思考：任何web工作流是否可引入中断机制？web工作流工具的入参传入断点和断点继续执行所需信息后可以继续执行。
    pass

def api_wrapper(api_id:str) -> BaseTool:
    # 传入一个RestfulAPI的id，获取其名称，描述，入参出参信息后，动态封装成一个工具
    # TODO
    pass

