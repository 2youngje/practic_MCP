# 🤖 실전 MCP 연습 프로젝트 (Practice MCP)

이 저장소는 **Model Context Protocol (MCP)** 서버 및 클라이언트를 직접 구현하고 실험해보기 위한 실습 프로젝트입니다. LLM(대형 언어 모델)이 내 컴퓨터의 로컬 환경이나 외부 API와 통신할 수 있도록 다양한 도구(Tool), 리소스(Resource), 프롬프트(Prompt)를 제공합니다.

---

## ✨ 프로젝트 주요 기능

### 🛠️ 제공하는 도구 (Tools)
외부 모델이 이 서버에 접속하면 아래의 4가지 기능을 사용할 수 있습니다:

| 도구 | 설명 |
|---|---|
| `echo(message)` | 전달받은 메시지를 그대로 반환하는 기본 테스트 도구 |
| `get_weather(city)` | 특정 도시의 실시간 날씨 조회 — **한글/영문 모두 지원** (예: 서울, Tokyo) |
| `list_directory(path)` | 로컬 PC의 특정 폴더 내 파일 목록을 조회하여 LLM에게 파일 시스템 접근 권한 부여 |
| `calculate(a, b, operator)` | 간단한 사칙연산 (+, -, *, /) 수행 |

### 📦 리소스 (Resources)
- **`config://app/settings`**: 서버가 가상으로 제공하는 앱 설정 JSON 데이터 (다크모드, 버전 정보 등)

### 💬 프롬프트 템플릿 (Prompts)
- **`greet_user(name)`**: LLM에게 사용자 이름을 전달하며 친근한 인사와 도구 사용법 안내를 요청하는 프롬프트 템플릿

---

## 🖥️ 웹 인스펙터 UI

Streamlit 기반의 웹 인스펙터로 브라우저에서 바로 MCP 도구를 테스트할 수 있습니다.

- 🌌 **다크 유리(Glassmorphism) 테마 — 보랏빛 그라데이션 배경**
- 각 도구가 **반투명 카드** 형태로 구분되어 한눈에 파악 가능
- 호버/클릭 시 **부드러운 애니메이션** 효과 적용
- 결과 박스가 도구별로 색상이 다르게 표시됨:
  - 🌤️ **날씨**: 파란 계열
  - 📁 **폴더 조회**: 초록 계열
  - 🧮 **계산기**: 보라 계열 (수식 + 결과 크게 표시)

---

## 📁 파일 구조

```
practice_MCP/
├── server.py        # FastMCP 서버 — 도구/리소스/프롬프트 정의 및 구동
├── client.py        # 터미널 기반 기본 클라이언트 예제
├── web_client.py    # Streamlit 웹 인스펙터 (글래스모피즘 UI)
├── mcp.json         # VS Code / Claude 데스크톱 등 외부 연동 설정 파일
├── .gitignore       # 가상환경, 캐시 등 불필요한 파일 깃 제외 설정
└── README.md        # 프로젝트 문서
```

---

## 🚀 설치 및 시작하기

### 1. 패키지 준비
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows PowerShell 기준)
.venv\Scripts\Activate.ps1

# 필수 패키지 설치
pip install mcp streamlit httpx
```

### 2. 실행

**터미널에서 텍스트 기반 테스트 (`client.py`)**
```bash
python client.py
```
> 도구 목록, 날씨 조회, 계산기 결과 등이 터미널에 텍스트로 출력됩니다.

**브라우저에서 UI 기반 테스트 (`web_client.py`)**
```bash
streamlit run web_client.py
```
> 브라우저에서 **http://localhost:8501** 으로 접속하면 글래스모피즘 디자인의 웹 인스펙터가 열립니다.

---

## 📝 업데이트 내역

| 날짜 | 내용 |
|---|---|
| 2026-03-31 | 웹 인스펙터 UI 전면 리디자인 (글래스모피즘 + 다크 테마) |
| 2026-03-31 | 날씨 조회 한글 도시명 지원 추가 (URL 인코딩 처리) |
| 2026-03-31 | 초기 프로젝트 생성 (서버, 클라이언트, 웹 인스펙터) |

---

💡 *이 저장소는 **MCP(Model Context Protocol)** 생태계의 작동 원리를 파악하고, 나만의 AI 환경을 더 똑똑하게 확장하기 위한 연습 목적으로 만들어졌습니다.*
