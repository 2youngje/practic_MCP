import streamlit as st
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 기본 페이지 설정
st.set_page_config(page_title="MCP 웹 인스펙터", layout="centered")

st.title("🌐 나만의 MCP 웹 테스트 화면")
st.markdown("CMD가 아닌 인터넷 브라우저에서 버튼을 클릭해 직접 MCP 도구(Tool)들을 테스트해 보세요!")

# 윈도우 환경 asyncio 관련 오류 방지
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 백그라운드에서 server.py를 호출하여 도구 실행
async def run_mcp_tool(tool_name, args):
    server_params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, args)
            return result.content[0].text

st.divider()

# 1. 날씨 조회 컴포넌트
st.subheader("🌤️ 날씨 조회 (get_weather)")
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("조회할 도시 영문명 (예: Seoul, Tokyo, New York)", "Seoul", label_visibility="collapsed")
with col2:
    weather_clicked = st.button("날씨 조회", use_container_width=True)

if weather_clicked:
    with st.spinner("날씨 정보 가져오는 중..."):
        try:
            # asyncio.run을 통해 MCP 서버와 비동기 통신
            res = asyncio.run(run_mcp_tool("get_weather", {"city": city}))
            st.markdown(f"""
            <div style="background-color: #2e3b4e; padding: 25px; border-radius: 15px; text-align: center; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="color: #ffffff; margin: 0; font-size: 28px;">{res}</h2>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"실행 오류: {e}")

st.divider()

# 2. 로컬 디렉토리 조회 컴포넌트
st.subheader("📁 로컬 폴더 조회 (list_directory)")
col3, col4 = st.columns([3, 1])
with col3:
    path = st.text_input("파일 리스트를 조회할 폴더 경로", ".", label_visibility="collapsed")
with col4:
    if st.button("폴더 읽기", use_container_width=True):
        with st.spinner("폴더 구조 스캔 중..."):
            try:
                res = asyncio.run(run_mcp_tool("list_directory", {"path": path}))
                st.code(res, language="markdown")
            except Exception as e:
                st.error(f"실행 오류: {e}")

st.divider()

# 3. 계산기 컴포넌트
st.subheader("🧮 계산기 (calculate)")
calc_col1, calc_col2, calc_col3, calc_col4 = st.columns([2, 1, 2, 2])
with calc_col1:
    a = st.number_input("숫자 A", value=10.0, label_visibility="collapsed")
with calc_col2:
    op = st.selectbox("연산자", ["+", "-", "*", "/"], label_visibility="collapsed")
with calc_col3:
    b = st.number_input("숫자 B", value=5.0, label_visibility="collapsed")
with calc_col4:
    if st.button("계산하기", use_container_width=True):
        with st.spinner("계산 중..."):
            try:
                res = asyncio.run(run_mcp_tool("calculate", {"a": float(a), "b": float(b), "operator": op}))
                st.info(f"결과: {res}")
            except Exception as e:
                st.error(f"실행 오류: {e}")
