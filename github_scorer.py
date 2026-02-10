from github import Github
from datetime import datetime, timedelta
import pytz
import streamlit as st

def get_token():
    """Streamlit Secrets에서 토큰 가져오기"""
    try:
        return st.secrets["CODING_STUDY_TOKEN"]
    except:
        return None

def get_current_week_friday():
    """현재 주의 금요일 20:00 기준 계산"""
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 현재 요일 (0=월요일, 4=금요일)
    weekday = now.weekday()
    
    # 금요일 20시 이전이면 지난주 금요일, 이후면 이번주 금요일
    if weekday < 4 or (weekday == 4 and now.hour < 20):
        days_to_friday = weekday + 3
        target_friday = now - timedelta(days=days_to_friday)
    else:
        days_to_friday = (4 - weekday) % 7
        if days_to_friday == 0 and now.hour >= 20:
            target_friday = now
        else:
            target_friday = now + timedelta(days=days_to_friday)
    
    return target_friday.replace(hour=20, minute=0, second=0, microsecond=0)

def get_repo_files(token, repo_url, since_date, until_date):
    """기간 내 커밋된 파일 목록 반환"""
    try:
        # token이 없으면 Secrets에서 가져오기
        if not token:
            token = get_token()
        
        g = Github(token)
        repo_name = repo_url.split('github.com/')[-1].rstrip('/')
        repo = g.get_repo(repo_name)
        
        commits = repo.get_commits(since=since_date, until=until_date)
        files = set()
        
        for commit in commits:
            for file in commit.files:
                if file.status in ['added', 'modified']:
                    files.add(file.filename)
        
        return list(files)
    except:
        return []

def calculate_score(file_path):
    """파일 경로로 점수 계산"""
    path = file_path.lower()
    
    # README 파일은 점수 계산 제외
    if 'readme' in path or path.endswith('.md'):
        return 0
    
    # 백준 점수 계산
    baekjoon_scores = {
        '백준/bronze/': 1,
        '백준/silver/': 2,
        '백준/gold/': 3,
        '백준/platinum/': 4,
        '백준/diamond/': 5
    }
    
    # 프로그래머스 점수 계산
    programmers_scores = {
        '프로그래머스/0/': 1,
        '프로그래머스/1/': 2,
        '프로그래머스/2/': 3,
        '프로그래머스/3/': 4,
        '프로그래머스/4/': 5
    }
    
    for pattern, score in {**baekjoon_scores, **programmers_scores}.items():
        if pattern in path:
            return score
    
    return 0

def get_weekly_score(token, repo_url):
    """현재 주의 총점 반환"""
    week_start = get_current_week_friday()
    week_end = week_start + timedelta(days=7) - timedelta(seconds=1)
    
    files = get_repo_files(token, repo_url, week_start, week_end)
    total_score = sum(calculate_score(file_path) for file_path in files)
    
    return total_score, files

def get_file_content(token, repo_url, file_path):
    """파일 내용 가져오기"""
    try:
        # token이 없으면 Secrets에서 가져오기
        if not token:
            token = get_token()
            
        g = Github(token)
        repo_name = repo_url.split('github.com/')[-1].rstrip('/')
        repo = g.get_repo(repo_name)
        file = repo.get_contents(file_path)
        return file.decoded_content.decode('utf-8')
    except:
        return None