import streamlit as st
import json
import random
from datetime import datetime, timedelta
import pytz

def get_current_week():
    """금요일 20:00 기준 주차 계산"""
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 금요일(4) 20:00 기준
    weekday = now.weekday()
    if weekday < 4 or (weekday == 4 and now.hour < 20):
        days_to_friday = weekday + 3
        friday = now - timedelta(days=days_to_friday)
    else:
        days_to_friday = (4 - weekday) % 7
        if days_to_friday == 0 and now.hour >= 20:
            friday = now
        else:
            friday = now + timedelta(days=days_to_friday)
    
    return friday.strftime("%Y-%W")

def show_lottery():
    st.title("🎲 발표 대상자 추첨")
    
    with open('data/members.json', 'r', encoding='utf-8') as f:
        members = json.load(f)
    
    with open('data/lottery.json', 'r', encoding='utf-8') as f:
        lottery_data = json.load(f)
    
    if not members:
        st.warning("등록된 멤버가 없습니다.")
        return
    
    current_week = get_current_week()
    member_names = [m['name'] for m in members]
    
    col1, col2 = st.columns(2)
    with col1:
        python_count = st.number_input("파이썬 인원수", min_value=0, max_value=len(members), value=1)
    with col2:
        sql_count = st.number_input("SQL 인원수", min_value=0, max_value=len(members), value=1)
    
    # 기존 추첨 결과 표시
    if current_week in lottery_data:
        st.success(f"✅ 이번 주 추첨 결과 (주차: {current_week})")
        result = lottery_data[current_week]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🐍 파이썬 발표자")
            for name in result.get('python', []):
                st.write(f"- {name}")
        
        with col2:
            st.subheader("🗄️ SQL 발표자")
            for name in result.get('sql', []):
                st.write(f"- {name}")
        
        st.divider()
        if st.button("🔄 재추첨하기"):
            del lottery_data[current_week]
            with open('data/lottery.json', 'w', encoding='utf-8') as f:
                json.dump(lottery_data, f, ensure_ascii=False, indent=2)
            st.rerun()
    else:
        if st.button("🎲 추첨하기"):
            total_count = python_count + sql_count
            if total_count > len(members):
                st.error("선택 인원이 전체 멤버 수보다 많습니다!")
            else:
                selected = random.sample(member_names, total_count)
                python_members = selected[:python_count]
                sql_members = selected[python_count:total_count]
                
                lottery_data[current_week] = {
                    'python': python_members,
                    'sql': sql_members,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open('data/lottery.json', 'w', encoding='utf-8') as f:
                    json.dump(lottery_data, f, ensure_ascii=False, indent=2)
                st.rerun()

def show_board():
    st.title("💬 자유게시판")
    
    with open('data/board.json', 'r', encoding='utf-8') as f:
        board_data = json.load(f)
    
    # 게시글 작성
    with st.expander("✍️ 새 게시글 작성"):
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            author = st.text_input("작성자")
            
            if st.form_submit_button("게시"):
                if title and content and author:
                    new_post = {
                        'id': len(board_data) + 1,
                        'title': title,
                        'content': content,
                        'author': author,
                        'timestamp': datetime.now().isoformat()
                    }
                    board_data.insert(0, new_post)
                    with open('data/board.json', 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    st.success("게시글이 작성되었습니다!")
                    st.rerun()
    
    st.divider()
    
    # 게시글 목록
    if not board_data:
        st.info("아직 게시글이 없습니다.")
    else:
        for i, post in enumerate(board_data):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.subheader(post['title'])
                st.write(f"👤 {post['author']} | 🕐 {post['timestamp'][:19]}")
                st.write(post['content'])
            with col2:
                if st.button("🗑️ 삭제", key=f"del_post_{post['id']}"):
                    board_data.pop(i)
                    with open('data/board.json', 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    st.rerun()
            st.divider()
