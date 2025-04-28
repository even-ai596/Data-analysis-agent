import time
import pandas as pd
import streamlit as st

# 示例数据
_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit.
"""

# 定义一个生成器函数，流式返回文本和 DataFrame
def stream_data():
    # 流式输出文本（逐词）
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.05)  # 模拟延迟
    
    # 输出一个 DataFrame
    yield pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    
    # 继续输出文本
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.05)

# 按钮触发流式输出
if st.button("开始流式输出"):
    st.write_stream(stream_data)