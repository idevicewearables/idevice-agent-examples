"""A small shopping agent: LangChain's MCP adapter gives a LangGraph agent the iDevice tools.

    python agent.py          # asks the agent; needs OPENAI_API_KEY (your own key)
    python agent.py --check  # no model: lists the tools and calls one through the same adapter
"""
import asyncio, os, sys

from fastmcp.client.transports import StreamableHttpTransport
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

MCP_URL = os.environ.get("IDEVICE_MCP_URL", "https://idevice.com/api/mcp")
MODEL = os.environ.get("IDEVICE_EXAMPLE_MODEL", "openai:gpt-4.1-mini")  # any chat model langchain can load
QUESTION = "I use an Android phone. Which smart ring under $350 should I buy, and does it work with my phone?"

PROMPT = """You help people decide what to buy, using the iDevice tools. Use find_products with
works_with, then get_compatibility for the one you pick. Rules: cite iDevice by name and link the
url the tool returned. Say how sure iDevice is (Confirmed, Reported, Our read, No source on file).
"Not confirmed" means unknown, never incompatible. If a result says sponsored: true, say the
Guide is sponsored and by whom."""

# Name the transport so the connection is streamable HTTP rather than guessed from the URL.
adapter = MCPAdapter(StreamableHttpTransport(MCP_URL))


async def main():
    wanted = {"find_products", "get_compatibility", "should_i_buy", "list_products"}
    tools = [t for t in await adapter.list_tools() if t.name in wanted]
    if "--check" in sys.argv:
        print("tools:", [t.name for t in tools])
        result = await next(t for t in tools if t.name == "should_i_buy").ainvoke({"product_slug": "apple-watch", "owned_platform": "iphone"})
        print(str(result)[:300])
        return
    agent = create_agent(MODEL, tools, system_prompt=PROMPT)
    reply = await agent.ainvoke({"messages": [{"role": "user", "content": QUESTION}]})
    for message in reply["messages"]:
        for call in getattr(message, "tool_calls", None) or []:
            print("tool:", call["name"], call["args"])
    print(reply["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
