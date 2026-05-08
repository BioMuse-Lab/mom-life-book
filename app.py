from git import Repo
import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="妈妈的书", layout="wide")

# --- 基础配置：确保文件夹存在 ---
folders = ["冬日降临","儿童时代","她的少女时代","游荡时期","初入婚姻","阳台日记", "往事回响", "家味传承"]
for f in folders:
    os.makedirs(f"content/{f}", exist_ok=True)

# --- 侧边栏：功能切换 ---
st.sidebar.title("📖 共创书房")
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
    st.write("可以在这里选一个分类，写字或者传照片。")
    
    with st.form("upload_form", clear_on_submit=True):
        selected_folder = st.selectbox("这篇内容属于：", folders)
        title = st.text_input("给这篇内容起个小标题（比如：今天的生菜）")
        content_text = st.text_area("想说的话（如果用语音输入法，直接点键盘上的话筒按钮说话就好）", height=200)
        uploaded_pic = st.file_uploader("传一张照片（可选）", type=['png', 'jpg', 'jpeg'])
        # --- 新增语音上传接口 ---
        uploaded_audio = st.file_uploader("录一段话发给我（可选）", type=['mp3', 'wav', 'm4a', 'aac'])
        
        submit = st.form_submit_button("提交到书里")
        
        if submit:
            if not content_text and not uploaded_pic and not uploaded_audio:
                st.warning("总得写点什么、传张照片或者录段音吧~")
            else:
                # --- A. 原有的文件保存逻辑 (保持你现在的代码不变) ---
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                file_name = f"{timestamp}_{title}.md"
                file_path = f"content/{selected_folder}/{file_name}"
                
                # (此处为你之前写的保存文字、图片、音频到本地文件夹的代码)
                # ... [保持不变] ...

                # --- B. 【核心改动】Git 同步逻辑 ---
                try:
                    from git import Repo
                    
                    # 1. 从 Secrets 读取配置
                    token = st.secrets["GITHUB_TOKEN"]
                    user = st.secrets["GITHUB_USER"]
                    repo_name = st.secrets["GITHUB_REPO"]
                    
                    # 2. 构造带权限的远程地址
                    remote_url = f"https://{user}:{token}@github.com/{user}/{repo_name}.git"
                    
                    # 3. 初始化仓库
                    repo = Repo(".")
                    
                    # 4. 设置 Git 用户信息（Streamlit 服务器环境需要）
                    repo.config_writer().set_value("user", "name", user).release()
                    repo.config_writer().set_value("user", "email", "action@github.com").release()

                    # 5. 重新配置远程仓库地址（确保带上 Token）
                    if 'origin' in [r.name for r in repo.remotes]:
                        repo.delete_remote('origin')
                    origin = repo.create_remote('origin', remote_url)

                    # 6. 执行添加、提交和推送
                    repo.git.add(A=True)  # 添加所有新文件
                    repo.index.commit(f"妈妈更新了章节：{selected_folder} - {title}")
                    origin.push('main')  # ！！！请确认你的分支名是 main 还是 master

                    st.success("✨ 太棒了！内容已成功同步到 GitHub 仓库。")
                    
                except Exception as e:
                    st.error(f"本地保存成功，但同步到 GitHub 失败：{e}")
                    st.info("建议检查：1. Secrets 里的名字是否写对；2. 分支名是否为 main。")
