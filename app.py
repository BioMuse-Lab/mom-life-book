import streamlit as st
import os

st.set_page_config(page_title="妈妈的书", layout="wide")

# 侧边栏：书的导航
st.sidebar.title("📖 共创书书房")
category = st.sidebar.selectbox("选择章节", ["最新动态", "阳台日记", "旧时光", "传家菜"])

st.title("给妈妈的一本书：[书名待定]")
st.info("这是一本由我和妈妈共同创作的生命叙事。妈妈口述，我负责整理。")

# 模拟读取 content 文件夹下的内容
def load_content(folder):
    files = sorted(os.listdir(f"content/{folder}"), reverse=True)
    for file in files:
        with open(f"content/{folder}/{file}", "r", encoding="utf-8") as f:
            st.markdown(f.read())
            st.divider()

# 页面逻辑
if category == "最新动态":
    st.subheader("🍃 最近更新")
    # 这里可以展示所有文件夹里最新的 5 条记录
else:
    load_content(category)
