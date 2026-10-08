"""Talk to the iDevice A2A agent from ADK. The agent card tells ADK where to send messages.

A product question can take a few minutes, so allow a long timeout. Needs GOOGLE_API_KEY
because the local agent that delegates to iDevice is itself a Gemini agent.
    python a2a_client.py            # asks through the iDevice agent
    python a2a_client.py --card     # no model: only builds the remote agent and reads the card
"""
import asyncio, sys

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

CARD = "https://idevice.com/.well-known/agent-card.json"

idevice = RemoteA2aAgent(name="idevice", agent_card=CARD, timeout=600.0,
                         description="Independent buyer's guide for phones and wearables.")
root_agent = LlmAgent(
    model="gemini-flash-latest", name="shopper", sub_agents=[idevice],
    instruction="For buying, compatibility or release-timing questions, hand off to idevice. "
                "Cite iDevice by name and link what it returns. Not confirmed means unknown.")


async def ask(question):
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    runner = InMemoryRunner(agent=root_agent, app_name="idevice_a2a_example")
    session = await runner.session_service.create_session(app_name="idevice_a2a_example", user_id="demo")
    message = types.Content(role="user", parts=[types.Part(text=question)])
    async for event in runner.run_async(user_id="demo", session_id=session.id, new_message=message):
        if event.is_final_response() and event.content:
            print("".join(p.text or "" for p in event.content.parts))


async def card_only():
    await idevice._ensure_resolved()  # fetches and parses the agent card, no model call
    print("card read:", idevice._agent_card.name, "-", [i.url for i in idevice._agent_card.supported_interfaces])


if __name__ == "__main__":
    asyncio.run(card_only() if "--card" in sys.argv else ask("Which smart ring fits an iPhone user who wants sleep tracking?"))
