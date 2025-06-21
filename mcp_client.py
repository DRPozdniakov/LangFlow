from agents.mcp import MCPServerStdio
import asyncio
import os
from dotenv import load_dotenv

from agents import Agent, Runner, trace


load_dotenv(override=True)
cwd = os.getcwd()

servers = {
    "screenshot": {"command": "uv", "args": ["run", "screenshot_mcp_server.py"], "cwd": cwd},
    "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", cwd+"/data/"]}
}

async def main():
    for name, config in servers.items():
        async with MCPServerStdio(params=config, client_session_timeout_seconds=60) as server:
            tools = await server.list_tools()
            print(f"{name}: {len(tools)} tools")
            for tool in tools:
                print(f"  - {tool.name}")

            agent = Agent(
                name="Screen_Sharing", 
                instructions="You are an expert testing MCP tools design by the newbee", 
                model="gpt-4.1-mini",
                mcp_servers=[server]
                )
            
            with trace("investigate"):
                result = await Runner.run(agent, "Make a screenshot and confirm that information is received. Can you describe the screenshot in detail? And can you try to save screenshot as a png file? Make unique name for file. Save it in the data folder.")
                print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())