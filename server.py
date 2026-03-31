import os
import urllib.request
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("HelloWorld")

@mcp.tool()
def echo(message: str) -> str:
    """
    메시지를 받아서 그대로 반환(Echo)하는 도구입니다.
    
    Args:
        message (str): 메아리칠 메시지 내용
    """
    return f"ECHO: {message}"

@mcp.tool()
def get_weather(city: str) -> str:
    """
    특정 도시의 현재 실시간 날씨 정보를 조회합니다. LLM이 실시간 외부 데이터를 가져오는 대표적인 예시입니다.
    
    Args:
        city (str): 영문 도시 이름 (예: Seoul, London)
    """
    try:
        import urllib.parse
        # 한글 도시 이름도 인식할 수 있도록 URL 인코딩 적용
        encoded_city = urllib.parse.quote(city)
        url = f"https://wttr.in/{encoded_city}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            return f"🌍 {city} 기상 상태: {desc}, 🌡️ 온도: {temp}°C"
    except Exception as e:
        return f"날씨 조회 실패: {e}"

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """
    로컬 PC의 특정 폴더 내 파일 목록을 조회합니다. LLM이 내 컴퓨터의 파일 시스템을 읽을 수 있게 해주는 기능입니다.
    
    Args:
        path (str): 조회할 폴더의 경로 (기본값: 서버가 실행된 현재 폴더 '.')
    """
    try:
        items = os.listdir(path)
        return f"📁 '{path}' 폴더의 구조:\n" + "\n".join(f"  - {item}" for item in items)
    except Exception as e:
        return f"폴더 조회 실패: {e}"

@mcp.tool()
def calculate(a: float, b: float, operator: str) -> str:
    """
    간단한 사칙연산을 수행하는 도구입니다.
    
    Args:
        a (float): 첫 번째 숫자
        b (float): 두 번째 숫자
        operator (str): 연산자 (+, -, *, / 중 하나)
    """
    try:
        if operator == "+": return str(a + b)
        elif operator == "-": return str(a - b)
        elif operator == "*": return str(a * b)
        elif operator == "/": return str(a / b)
        else: return "지원하지 않는 연산자입니다."
    except Exception as e:
        return f"에러 발생: {e}"

# --- 2. 리소스(Resource) 추가: 서버가 가진 정적 데이터 ---
@mcp.resource("config://app/settings")
def get_settings() -> str:
    """가상의 앱 설정 정보를 제공하는 리소스입니다."""
    return '{"theme": "dark", "version": "1.0.0", "mcp_enabled": true}'

# --- 3. 프롬프트(Prompt) 추가: LLM을 위한 템플릿 제공 ---
@mcp.prompt()
def greet_user(name: str) -> str:
    """
    사용자에게 인사를 건넬 때 사용하는 프롬프트 템플릿입니다.
    
    Args:
        name (str): 사용자 이름
    """
    return f"사용자 이름은 {name}입니다. 이 사용자에게 친근하고 재미있게 인사해 주시고, 제가 제공하는 도구들(Echo, Calculator)을 어떻게 사용할 수 있는지 설명해 주세요."

if __name__ == "__main__":
    import asyncio
    
    # 윈도우 환경에서 asyncio 이벤트 루프 정책 설정 (필요시)
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    mcp.run()
