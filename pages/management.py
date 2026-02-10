import streamlit as st
import json
import os
from github_scorer import get_file_content, get_weekly_score, calculate_score

def show_goal_management():
    st.title("⚙️ 목표 관리")
    
    with open('data/goals.json', 'r', encoding='utf-8') as f:
        goals = json.load(f)
    
    # 주간 공통 목표
    st.subheader("📌 주간 공통 목표")
    with st.form("weekly_goal"):
        title = st.text_input("제목")
        link = st.text_input("링크 (선택)")
        if st.form_submit_button("추가"):
            goals['weekly_goals'].append({"title": title, "link": link})
            with open('data/goals.json', 'w', encoding='utf-8') as f:
                json.dump(goals, f, ensure_ascii=False, indent=2)
            st.success("추가되었습니다!")
            st.rerun()
    
    for i, goal in enumerate(goals['weekly_goals']):
        col1, col2, col3 = st.columns([3, 3, 1])
        with col1:
            st.write(goal['title'])
        with col2:
            st.write(goal['link'] if goal['link'] else "-")
        with col3:
            if st.button("삭제", key=f"del_w_{i}"):
                goals['weekly_goals'].pop(i)
                with open('data/goals.json', 'w', encoding='utf-8') as f:
                    json.dump(goals, f, ensure_ascii=False, indent=2)
                st.rerun()
    
    st.divider()
    
    # 그룹별 목표
    for group_key, group_name in [("A", "A"), ("B", "B")]:
        st.subheader(f"🎯 그룹 {group_name} 목표")
        with st.form(f"group_{group_key}_goal"):
            title = st.text_input("제목", key=f"title_{group_key}")
            link = st.text_input("링크 (선택)", key=f"link_{group_key}")
            if st.form_submit_button("추가", key=f"submit_{group_key}"):
                goals['group_goals'][group_key].append({"title": title, "link": link})
                with open('data/goals.json', 'w', encoding='utf-8') as f:
                    json.dump(goals, f, ensure_ascii=False, indent=2)
                st.success("추가되었습니다!")
                st.rerun()
        
        for i, goal in enumerate(goals['group_goals'][group_key]):
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                st.write(goal['title'])
            with col2:
                st.write(goal['link'] if goal['link'] else "-")
            with col3:
                if st.button("삭제", key=f"del_{group_key}_{i}"):
                    goals['group_goals'][group_key].pop(i)
                    with open('data/goals.json', 'w', encoding='utf-8') as f:
                        json.dump(goals, f, ensure_ascii=False, indent=2)
                    st.rerun()

def show_member_management():
    st.title("👤 멤버 관리")
    
    with open('data/members.json', 'r', encoding='utf-8') as f:
        members = json.load(f)
    
    # 멤버 추가
    st.subheader("➕ 멤버 추가")
    with st.form("add_member"):
        name = st.text_input("이름")
        repo_url = st.text_input("GitHub 레포 URL (예: https://github.com/user/repo)")
        group = st.selectbox("그룹", ["A", "B"])
        token = st.text_input("GitHub Token", type="password")
        if st.form_submit_button("추가"):
            members.append({
                "name": name,
                "repo_url": repo_url,
                "group": group,
                "token": token
            })
            with open('data/members.json', 'w', encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=2)
            st.success("추가되었습니다!")
            st.rerun()
    
    st.divider()
    
    # 멤버 목록
    st.subheader("📋 멤버 목록")
    for i, member in enumerate(members):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 1, 1])
        with col1:
            st.write(f"**{member['name']}**")
        with col2:
            st.write(member['repo_url'])
        with col3:
            # 그룹 변경
            new_group = st.selectbox("그룹", ["A", "B"], 
                                     index=0 if member['group'] == "A" else 1,
                                     key=f"group_{i}")
            if new_group != member['group']:
                members[i]['group'] = new_group
                with open('data/members.json', 'w', encoding='utf-8') as f:
                    json.dump(members, f, ensure_ascii=False, indent=2)
                st.rerun()
        with col4:
            st.write("🔑" if member.get('token') else "❌")
        with col5:
            if st.button("삭제", key=f"del_m_{i}"):
                members.pop(i)
                with open('data/members.json', 'w', encoding='utf-8') as f:
                    json.dump(members, f, ensure_ascii=False, indent=2)
                st.rerun()

def show_member_detail():
    st.title("👥 멤버 상세 보기")
    
    with open('data/members.json', 'r', encoding='utf-8') as f:
        members = json.load(f)
    
    if not members:
        st.warning("등록된 멤버가 없습니다.")
        return
    
    # 멤버 선택
    member_names = [m['name'] for m in members]
    selected_name = st.selectbox("멤버 선택", member_names)
    
    selected_member = next(m for m in members if m['name'] == selected_name)
    
    st.subheader(f"📊 {selected_name}님의 이번 주 활동")
    
    # 로딩 표시와 함께 점수 계산
    with st.spinner('GitHub에서 데이터를 불러오는 중...'):
        score, files = get_weekly_score(selected_member['token'], selected_member['repo_url'])
    
    st.metric("이번 주 점수", f"{score}점")
    
    # 점수가 있는 파일만 필터링
    scored_files = [(f, calculate_score(f)) for f in files if calculate_score(f) > 0]
    
    if not scored_files:
        st.info("이번 주에 점수가 계산된 파일이 없습니다.")
        return
    
    st.subheader("📁 점수 계산된 파일 목록")
    
    for file_path, file_score in scored_files:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.write(file_path)
        with col2:
            st.write(f"{file_score}점")
        with col3:
            if st.button("코드 보기", key=f"view_{file_path}"):
                st.session_state.viewing_file = file_path
                st.session_state.viewing_member = selected_member
    
    # 코드 보기
    if hasattr(st.session_state, 'viewing_file'):
        st.divider()
        st.subheader(f"📄 {st.session_state.viewing_file}")
        
        # README와 코드 파일 경로
        file_dir = '/'.join(st.session_state.viewing_file.split('/')[:-1])
        readme_path = f"{file_dir}/README.md"
        code_path = st.session_state.viewing_file
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📖 README.md**")
            with st.spinner('README 불러오는 중...'):
                readme_content = get_file_content(
                    st.session_state.viewing_member['token'],
                    st.session_state.viewing_member['repo_url'],
                    readme_path
                )
            if readme_content:
                st.markdown(readme_content, unsafe_allow_html=True)
            else:
                st.info("README.md 파일이 없습니다.")
        
        with col2:
            st.markdown("**💻 코드 파일**")
            with st.spinner('코드 불러오는 중...'):
                code_content = get_file_content(
                    st.session_state.viewing_member['token'],
                    st.session_state.viewing_member['repo_url'],
                    code_path
                )
            if code_content:
                ext = code_path.split('.')[-1]
                st.code(code_content, language=ext if ext in ['py', 'java', 'cpp', 'js', 'sql'] else 'python')
            else:
                st.error("파일을 불러올 수 없습니다.")
