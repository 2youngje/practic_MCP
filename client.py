import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    # 실행할 MCP 서버의 파라미터 설정 (현재 파이썬 환경으로 server.py 실행)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )

    print("MCP 서버에 연결 중...")
    
    # stdio(표준 입출력)를 통해 서버와 통신 채널을 엽니다.
    async with stdio_client(server_params) as (read, write):
        # 세션 생성 및 초기화
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("서버에 성공적으로 연결되었습니다!\n")

            # 1. 서버가 제공하는 도구 목록 가져오기
            tools_response = await session.list_tools()
            print("=== 🛠️ 사용 가능한 도구 목록 ===")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # 2. 'echo' 도구 실행해보기
            print("\n=== 🚀 'echo' 도구 실행 테스트 ===")
            test_message = "반갑습니다! MCP 첫 테스트입니다."
            print(f"보내는 메시지: {test_message}")
            result = await session.call_tool("echo", {"message": test_message})
            print(f"서버 응답: {result.content[0].text}")

            # 3. 'calculate' 도구 실행해보기
            print("\n=== 🧮 'calculate' 도구 실행 테스트 ===")
            calc_args = {"a": 15.5, "b": 4.5, "operator": "+"}
            print(f"계산 요청: {calc_args['a']} {calc_args['operator']} {calc_args['b']}")
            calc_result = await session.call_tool("calculate", calc_args)
            print(f"계산 결과: {calc_result.content[0].text}")

            # 4. 'get_weather' 도구 실행해보기 (실시간 URL Fetch)
            print("\n=== 🌤️ 'get_weather' 도구 실행 테스트 ===")
            weather_args = {"city": "Seoul"}
            print(f"날씨 조회 요청: {weather_args['city']}")
            weather_result = await session.call_tool("get_weather", weather_args)
            print(f"조회 결과: {weather_result.content[0].text}")

            # 5. 'list_directory' 도구 실행해보기 (로컬 파일 시스템 접근)
            print("\n=== 📁 'list_directory' 도구 실행 테스트 ===")
            dir_args = {"path": "."}
            print(f"디렉토리 조회 요청: {dir_args['path']}")
            dir_result = await session.call_tool("list_directory", dir_args)
            print(f"조회 결과:\n{dir_result.content[0].text}")

            # 6. 리소스 및 프롬프트 목록 가져오기 테스트
            resources = await session.list_resources()
            print(f"\n=== 📦 사용 가능한 리소스: {len(resources.resources)}개 ===")
            
            prompts = await session.list_prompts()
            print(f"=== 💬 사용 가능한 프롬프트: {len(prompts.prompts)}개 ===")

if __name__ == "__main__":
    # 윈도우 환경 asyncio 관련 오류 방지
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(run())
