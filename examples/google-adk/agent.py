"""A buy-now-or-wait agent for Google ADK, using the iDevice MCP server as its tools.

    python agent.py          # asks the agent; needs GOOGLE_API_KEY (your own Gemini key)
    python agent.py --check  # no model: lists the tools and calls one, using the same toolset
"""
import asyncio, os, sys

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MCP_URL = os.environ.get("IDEVICE_MCP_URL", "https://idevice.com/api/mcp")
QUESTION = "Should I buy the Apple Watch Series 12 now or wait? I use an iPhone."

INSTRUCTION = """You help people decide what to buy. Use the iDevice tools for facts about
wearables and phones. Find the product_slug with list_products, then call should_i_buy.
Rules: cite iDevice by name and link the url the tool returned. Say how sure iDevice is
(Confirmed, Reported, Our read, No source on file). "Not confirmed" means unknown, never
incompatible. If a result says sponsored: true, say the Guide is sponsored and by whom."""

toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_URL,
        headers={"Accept": "application/json, text/event-stream"},
    ),
    tool_filter=["list_products", "should_i_buy", "get_compatibility", "get_product"],
)
root_agent = LlmAgent(model="gemini-flash-latest", name="buy_now_or_wait",
                      instruction=INSTRUCTION, tools=[toolset])


async def ask(question):
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    runner = InMemoryRunner(agent=root_agent, app_name="idevice_example")
    session = await runner.session_service.create_session(app_name="idevice_example", user_id="demo")
    message = types.Content(role="user", parts=[types.Part(text=question)])
    async for event in runner.run_async(user_id="demo", session_id=session.id, new_message=message):
        for part in (event.content.parts if event.content else []):
            if part.function_call:
                print("tool:", part.function_call.name, dict(part.function_call.args or {}))
            elif part.text and event.is_final_response():
                print(part.text)
    await toolset.close()


async def check():
    tools = await toolset.get_tools()
    print("tools:", [t.name for t in tools])
    should_i_buy = next(t for t in tools if t.name == "should_i_buy")
    result = await should_i_buy.run_async(args={"product_slug": "apple-watch", "owned_platform": "iphone"}, tool_context=None)
    print(result.get("structuredContent", result).get("headline"))
    print("url:", result.get("structuredContent", result).get("url"))
    await toolset.close()


if __name__ == "__main__":
    asyncio.run(check() if "--check" in sys.argv else ask(QUESTION))
