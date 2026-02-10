import streamlit as st
import json
from github_scorer import get_weekly_score

st.title("📊 코딩 스터디 대시보드")

# 데이터 로드
with open('data/goals.json', 'r', encoding='utf-8') as f:
    goals = json.load(f)

with open('data/members.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

# 주간 목표 표시
st.subheader("🎯 이번 주 공통 목표")
for goal in goals['weekly_goals']:
    if goal['link']:
        st.markdown(f"- [{goal['title']}]({goal['link']})")
    else:
        st.markdown(f"- {goal['title']}")

st.divider()

# 그룹 필터
group_filter = st.selectbox("그룹 선택", ["전체", "A", "B"])

# 로딩 표시와 함께 멤버 점수 계산
with st.spinner('GitHub에서 멤버들의 점수를 계산하는 중...'):
    member_scores = []
    for member in members:
        if group_filter == "전체" or member['group'] == group_filter:
            score, files = get_weekly_score(member['token'], member['repo_url'])
            member_scores.append({
                'name': member['name'],
                'group': member['group'],
                'score': score,
                'achievement_rate': (score / 20) * 100,
                'shortage': max(0, 20 - score)
            })

# 점수순 정렬
member_scores.sort(key=lambda x: x['score'], reverse=True)

# 1등 멤버 강조
if member_scores and member_scores[0]['score'] > 0:
    top_member = member_scores[0]
    st.success(f"👑 1등: {top_member['name']} ({top_member['group']}그룹) - {top_member['score']}점")
    st.balloons()

# 멤버별 현황
st.subheader("📈 멤버별 현황")
for member in member_scores:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        crown = "👑 " if member == member_scores[0] and member['score'] > 0 else ""
        st.write(f"{crown}**{member['name']}** ({member['group']}그룹)")
        st.progress(min(member['achievement_rate'] / 100, 1.0))
    
    with col2:
        st.metric("현재 점수", f"{member['score']}점")
    
    with col3:
        if member['shortage'] > 0:
            st.metric("달성률", f"{member['achievement_rate']:.1f}%", f"-{member['shortage']}점")
        else:
            st.metric("달성률", f"{member['achievement_rate']:.1f}%", "목표 달성!")
