# 코딩 스터디 관리 시스템

Streamlit 기반 코딩 스터디 관리 웹 애플리케이션입니다.

## 주요 기능

- 📊 **대시보드**: 멤버별 주간 점수 및 달성률 확인
- 👥 **멤버 관리**: GitHub 레포지토리 연동 및 그룹 관리
- 🎯 **목표 관리**: 주간 공통 목표 및 그룹별 목표 설정
- 🎲 **발표 추첨**: 주간 발표자 랜덤 선정
- 💬 **자유게시판**: 스터디원 간 소통 공간

## 점수 계산 방식

### 백준
- Bronze: 1점
- Silver: 2점
- Gold: 3점
- Platinum: 4점
- Diamond: 5점

### 프로그래머스
- Level 0: 1점
- Level 1: 2점
- Level 2: 3점
- Level 3: 4점
- Level 4: 5점

**주간 목표**: 20점  
**기준 시간**: 매주 금요일 20:00 (KST)

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 초기 설정

1. `data/members.json`에서 멤버 정보 수정
   - GitHub 레포지토리 URL
   - GitHub Personal Access Token
   - 그룹 (A 또는 B)

2. GitHub Token 발급
   - GitHub Settings → Developer settings → Personal access tokens
   - `repo` 권한 필요

## 디렉토리 구조

```
.
├── app.py                 # 메인 앱
├── github_scorer.py       # GitHub API 및 점수 계산
├── pages/
│   ├── dashboard.py       # 대시보드
│   ├── management.py      # 관리 페이지들
│   └── extras.py          # 추첨 및 게시판
├── data/
│   ├── members.json       # 멤버 정보
│   ├── goals.json         # 목표 정보
│   ├── lottery.json       # 추첨 결과
│   └── board.json         # 게시판 글
└── requirements.txt
```

## 주의사항

- GitHub Token은 절대 공개 레포지토리에 커밋하지 마세요
- 주간 계산은 금요일 20:00 기준으로 자동 처리됩니다
- 발표 추첨 결과는 주간 단위로 고정됩니다
