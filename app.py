import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="妈妈的书", layout="wide")

# --- 基础配置：确保文件夹存在 ---
folders = ["冬日降临","儿童时代","她的少女时代","游荡时期","初入婚姻","阳台日记", "往事回响", "家味传承"]
for f in folders:
    os.makedirs(f"content/{f}", exist_ok=True)

# --- 侧边栏：功能切换 ---
st.sidebar.title("📖 共创书书房")
mode = st.sidebar.radio("选择操作", ["阅读书籍", "提交新内容"])

# --- 模式 1：阅读书籍 ---
if mode == "阅读书籍":
    st.sidebar.markdown("---")
    # 将原来的 selectbox 换成 radio，章节就会全部平铺显示在左侧
    category = st.sidebar.radio("📚 目录索引", folders)
    
    st.title(f"《给妈妈的一本书》")
    st.caption(f"当前章节：{category}")
    
    path = f"content/{category}"
    files = sorted([f for f in os.listdir(path) if f.endswith('.md')], reverse=True)
    
    if not files:
        st.info("这一章还没有内容，去『提交新内容』里写第一篇吧！")
    else:
        for file in files:
            with open(f"{path}/{file}", "r", encoding="utf-8") as f:
                st.markdown(f.read())
                st.divider()

# --- 模式 2：提交新内容（这是给妈妈用的接口） ---
elif mode == "提交新内容":
    st.title("✍️ 记录今天的生活")
    st.write("妈，你可以在这里选一个分类，写字或者传照片。")
    
    with st.form("upload_form", clear_on_submit=True):
        selected_folder = st.selectbox("这篇内容属于：", folders)
        title = st.text_input("给这篇内容起个小标题（比如：今天的生菜）")
        content_text = st.text_area("想说的话（如果用语音输入法，直接点键盘上的话筒按钮说话就好）", height=200)
        uploaded_pic = st.file_uploader("传一张照片（可选）", type=['png', 'jpg', 'jpeg'])
        
        submit = st.form_submit_button("提交到书里")
        
        if submit:
            if not content_text and not uploaded_pic:
                st.warning("总得写点什么或者传张照片吧~")
            else:
                # 生成文件名：日期_标题.md
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                file_name = f"{timestamp}_{title}.md"
                file_path = f"content/{selected_folder}/{file_name}"
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"### {title}\n")
                    f.write(f"*记录时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
                    f.write(f"{content_text}\n\n")
                    # 如果有照片，这里可以扩展保存逻辑
                
                st.success("提交成功！刷新『阅读书籍』页面就能看到了。")
