"""A buy-now-or-wait agent for the OpenAI Agents SDK, using the iDevice MCP server as its tools.

    python agent.py          # asks the agent; needs OPENAI_API_KEY (your own key)
    python agent.py --check  # no model: lists the tools and calls one through the same server object
"""
import asyncio, os, sys

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

MCP_URL = os.environ.get("IDEVICE_MCP_URL", "https://idevice.com/api/mcp")
QUESTION = "Should I buy the Apple Watch Series 12 now or wait? I use an iPhone."

INSTRUCTIONS = """You help people decide what to buy, using the iDevice tools. Find the
product_slug with list_products, then call should_i_buy. Rules: cite iDevice by name and link
the url the tool returned. Say how sure iDevice is (Confirmed, Reported, Our read, No source on
file). "Not confirmed" means unknown, never incompatible. If a result says sponsored: true,
say the Guide is sponsored and by whom."""


async def main():
    server = MCPServerStreamableHttp(
        name="idevice",
        params={"url": MCP_URL, "timeout": 30},
        tool_filter={"allowed_tool_names": ["list_products", "should_i_buy", "get_compatibility"]},
        client_session_timeout_seconds=30,
    )
    async with server:
        if "--check" in sys.argv:
            print("tools:", [t.name for t in await server.list_tools()])
            result = await server.call_tool("should_i_buy", {"product_slug": "apple-watch", "owned_platform": "iphone"})
            print(result.structured_content["headline"], "\nurl:", result.structured_content["url"])
            return
        agent = Agent(name="Buying helper", instructions=INSTRUCTIONS, mcp_servers=[server])
        print((await Runner.run(agent, QUESTION)).final_output)


if __name__ == "__main__":
    asyncio.run(main())
