import streamlit as st
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ─── 기본 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(
    page_title="MCP 웹 인스펙터",
    page_icon="🤖",
    layout="centered",
)

# ─── 글로벌 CSS 스타일 ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* 전체 배경 */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* 카드 공통 스타일 */
.tool-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.tool-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* 카드 헤더 */
.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}

.card-icon {
    font-size: 32px;
    line-height: 1;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}

.card-badge {
    font-size: 11px;
    color: #a0a9c0;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 2px 8px;
    margin-left: 6px;
    font-family: monospace;
}

/* 결과 박스 */
.result-box {
    border-radius: 14px;
    padding: 22px 26px;
    margin-top: 18px;
    font-size: 16px;
    line-height: 1.7;
    animation: fadeIn 0.4s ease;
}

.result-weather {
    background: linear-gradient(135deg, #1a4a7a 0%, #0d2d4e 100%);
    border: 1px solid rgba(100, 180, 255, 0.25);
    color: #e8f4fd;
}

.result-directory {
    background: linear-gradient(135deg, #1a3a2a 0%, #0d2418 100%);
    border: 1px solid rgba(80, 200, 120, 0.25);
    color: #e0f5ea;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    white-space: pre-wrap;
}

.result-calc {
    background: linear-gradient(135deg, #3a1a5a 0%, #200d3a 100%);
    border: 1px solid rgba(180, 100, 255, 0.25);
    color: #f0e8ff;
    text-align: center;
}

.result-calc .calc-expression {
    font-size: 20px;
    color: #c8a8f0;
    margin-bottom: 6px;
}

.result-calc .calc-answer {
    font-size: 42px;
    font-weight: 700;
    color: #e0c8ff;
}

.result-error {
    background: linear-gradient(135deg, #4a1a1a 0%, #2a0a0a 100%);
    border: 1px solid rgba(255, 100, 100, 0.3);
    color: #ffd0d0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Streamlit 위젯 오버라이드 */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-family: 'Inter', sans-serif !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
}

.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 10px !important;
    color: #111111 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: scale(1.02) !important;
}

/* 레이블 색상 */
label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: rgba(255,255,255,0.65) !important;
    font-size: 13px !important;
}

/* 구분선 */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── 윈도우 asyncio 정책 ────────────────────────────────────────────
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ─── MCP 도구 호출 함수 ────────────────────────────────────────────
async def run_mcp_tool(tool_name, args):
    server_params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, args)
            return result.content[0].text

# ─── 헤더 ──────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 40px 0 28px 0;">
    <div style="font-size: 52px; line-height: 1;">🤖</div>
    <h1 style="font-size: 32px; font-weight: 700; color: #ffffff; margin: 12px 0 6px 0;">
        MCP 웹 인스펙터
    </h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 15px; margin: 0;">
        브라우저에서 나만의 MCP 서버 도구를 직접 실험해보세요
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 1. 날씨 조회
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="tool-card">
    <div class="card-header">
        <span class="card-icon">🌤️</span>
        <span class="card-title">날씨 조회</span>
        <span class="card-badge">get_weather</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='margin-top:-16px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        city = st.text_input(
            "도시 이름 (한글 또는 영문, 예: 서울, Tokyo, New York)",
            value="서울",
            key="city_input"
        )
    with col2:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)
        weather_clicked = st.button("🔍 조회", key="weather_btn", use_container_width=True)

if weather_clicked and city:
    with st.spinner("🌍 날씨 정보를 불러오는 중..."):
        try:
            res = asyncio.run(run_mcp_tool("get_weather", {"city": city}))
            st.markdown(f"""
            <div class="result-box result-weather">
                <div style="font-size:13px; color: rgba(255,255,255,0.45); margin-bottom:8px;">📍 검색 도시: {city}</div>
                <div style="font-size:22px; font-weight:600;">{res}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="result-box result-error">⚠️ 오류 발생: {e}</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:24px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 2. 로컬 폴더 조회
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="tool-card">
    <div class="card-header">
        <span class="card-icon">📁</span>
        <span class="card-title">로컬 폴더 조회</span>
        <span class="card-badge">list_directory</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='margin-top:-16px'></div>", unsafe_allow_html=True)
    col3, col4 = st.columns([3, 1])
    with col3:
        path = st.text_input("조회할 폴더 경로", value=".", key="path_input")
    with col4:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)
        dir_clicked = st.button("📂 탐색", key="dir_btn", use_container_width=True)

if dir_clicked and path:
    with st.spinner("📂 폴더 구조 스캔 중..."):
        try:
            res = asyncio.run(run_mcp_tool("list_directory", {"path": path}))
            st.markdown(f"""
            <div class="result-box result-directory">{res}</div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="result-box result-error">⚠️ 오류 발생: {e}</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:24px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 3. 계산기
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="tool-card">
    <div class="card-header">
        <span class="card-icon">🧮</span>
        <span class="card-title">계산기</span>
        <span class="card-badge">calculate</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='margin-top:-16px'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2.5, 1, 2.5, 2])
    with c1:
        a = st.number_input("숫자 A", value=10.0, key="calc_a")
    with c2:
        op = st.selectbox("연산자", ["+", "-", "*", "/"], key="calc_op")
    with c3:
        b = st.number_input("숫자 B", value=5.0, key="calc_b")
    with c4:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)
        calc_clicked = st.button("⚡ 계산", key="calc_btn", use_container_width=True)

if calc_clicked:
    with st.spinner("계산 중..."):
        try:
            res = asyncio.run(run_mcp_tool("calculate", {"a": float(a), "b": float(b), "operator": op}))
            st.markdown(f"""
            <div class="result-box result-calc">
                <div class="calc-expression">{a} {op} {b} =</div>
                <div class="calc-answer">{res}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="result-box result-error">⚠️ 오류 발생: {e}</div>', unsafe_allow_html=True)

# ─── 푸터 ──────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 32px 0 16px 0; color: rgba(255,255,255,0.2); font-size: 13px;">
    🤖 Powered by FastMCP · Built with Streamlit
</div>
""", unsafe_allow_html=True)
