from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from ysx_agent.src.elements.models.models import llm
from ysx_agent.src.elements.states.normal_state import NormalState
from ysx_agent.src.elements.toolkits.fake_web_action_toolkit import FakeWebActionToolkit


memory = MemorySaver()

toolkit = FakeWebActionToolkit()
tools = toolkit.get_tools()

llm_with_tools = llm.bind_tools(tools)

react_web_agent_graph_builder = StateGraph(NormalState)


def chatbot(state: NormalState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

react_web_agent_graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
react_web_agent_graph_builder.add_node("tools", tool_node)

react_web_agent_graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
react_web_agent_graph_builder.add_edge("tools", "chatbot")
react_web_agent_graph_builder.add_edge(START, "chatbot")

react_web_agent_graph_builder.add_edge("chatbot", END)

ysx_agent = react_web_agent_graph_builder.compile(checkpointer=memory)


