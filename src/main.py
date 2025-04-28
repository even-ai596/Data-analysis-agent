from agents.pre_build_react_agent import ysx_react_agent
print("start")
from langchain_core.messages import HumanMessage
import streamlit as st
from elements.tools.fake_web_action_tools import en_to_zh_tool_name_dict,ask_human_tool
# config = {"configurable": {"thread_id": "abcde"}}
# input_message = {"type": "user", "content": "以窦梓瑜为署名发一封邮件给叫蒋励的客户表达你的歉意。"}

# # 有说明书
# for chunk in ysx_agent.stream({"messages": [system_message, input_message]}, stream_mode="values", config=config):
#     chunk["messages"][-1].pretty_print()
# 无说明书
# for chunk in ysx_agent.stream({"messages": [input_message]}, stream_mode="values", config=config):
#     chunk["messages"][-1].pretty_print()
# print(agent.invoke(input_message,config=config).content)
# 有说明书原生react agent
# for chunk in ysx_react_agent.stream({"messages": [input_message]}, stream_mode="values", config=config):
#     chunk["messages"][-1].pretty_print()

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "abcde"}}

    st.set_page_config(page_title="言生行智能体", page_icon="", layout="centered", initial_sidebar_state="auto",
                       menu_items=None)
    st.title("数据分析智能体")
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{
            "role": "assistant",
            "content": "有事吗？",
            "image": None,
        }]
        with st.chat_message("assistant"):
            st.markdown(st.session_state.messages[-1]["content"])
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    if user_input := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": user_input, "image": None})
        with st.chat_message("user"):
            st.markdown(user_input)
        statu_container = st.container(border=True)

        def get_answer_stream():
            last_human_message = HumanMessage(content=user_input)
            print(last_human_message)
            stream = ysx_react_agent.stream({"messages": [last_human_message]},stream_mode="values",config=config)
            # stream = ysx_react_agent.stream({"messages": [last_human_message]},stream_mode="values",config=config)
            for chunk in stream:
                print(chunk["messages"][-1],"---------------------")
                latest_chunk_info = chunk["messages"][-1]
                print(latest_chunk_info.type)
                print("完整对象:", vars(latest_chunk_info))

                if latest_chunk_info.content and latest_chunk_info.type == "ai":
                    yield latest_chunk_info.content
                elif latest_chunk_info.type == "ai" and latest_chunk_info.tool_calls:
                    called_tool_zh_names = [en_to_zh_tool_name_dict[a_tool["name"]] for a_tool in latest_chunk_info.tool_calls]
                    statu_container.markdown("正在使用"+str(called_tool_zh_names))
                elif latest_chunk_info.type == "tool" and latest_chunk_info.content:
                    statu_container.markdown("使用 "+en_to_zh_tool_name_dict[latest_chunk_info.name]+" 后获得了如下信息：\n"+latest_chunk_info.content)
        get_answer_stream()

        answer = st.write_stream(get_answer_stream())
        an_answer_message = {"role": "assistant", "content": answer, "image": None}
        st.session_state.messages.append(an_answer_message)



print("end")