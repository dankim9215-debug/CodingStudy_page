import streamlit as st
import json
import os

st.set_page_config(page_title="코딩 스터디 관리", layout="wide", initial_sidebar_state="expanded")

# 데이터 디렉토리 생성
os.makedirs("data", exist_ok=True)
os.makedirs("pages", exist_ok=True)

# 사이드바 메뉴
st.sidebar.title("📚 코딩 스터디 관리")
menu = st.sidebar.radio("메뉴", ["🏠 대시보드", "👥 멤버 보기", "⚙️ 목표 관리", "👤 멤버 관리", "🎲 발표 추첨", "💬 자유게시판"])

if menu == "🏠 대시보드":
    with open("pages/dashboard.py", encoding='utf-8') as f:
        exec(f.read())
elif menu == "👥 멤버 보기":
    with open("pages/management.py", encoding='utf-8') as f:
        code = f.read()
        exec(code)
    show_member_detail()
elif menu == "⚙️ 목표 관리":
    with open("pages/management.py", encoding='utf-8') as f:
        code = f.read()
        exec(code)
    show_goal_management()
elif menu == "👤 멤버 관리":
    with open("pages/management.py", encoding='utf-8') as f:
        code = f.read()
        exec(code)
    show_member_management()
elif menu == "🎲 발표 추첨":
    with open("pages/extras.py", encoding='utf-8') as f:
        code = f.read()
        exec(code)
    show_lottery()
elif menu == "💬 자유게시판":
    with open("pages/extras.py", encoding='utf-8') as f:
        code = f.read()
        exec(code)
    show_board()
