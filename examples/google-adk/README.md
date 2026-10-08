# Google ADK

`agent.py`: an `LlmAgent` whose tools come from `McpToolset` with `StreamableHTTPConnectionParams`. It answers "Should I buy the Apple Watch Series 12 now or wait?".
`a2a_client.py`: an ADK agent that delegates to the iDevice A2A agent through `RemoteA2aAgent` and the agent card.

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.10 or later
pip install -r requirements.txt
export GOOGLE_API_KEY=...        # your own Gemini key
python agent.py                  # the agent loop
python agent.py --check          # no model: list tools, call should_i_buy
python a2a_client.py --card      # no model: build the remote agent and read the card
```

**Tested against the live server (google-adk 2.11):** the `McpToolset` connection, `get_tools()` and one `should_i_buy` call through the ADK tool object; `RemoteA2aAgent` reading the agent card.
**Written from the ADK docs only:** the `LlmAgent` loop in `ask()`, the instruction text, and sending a message through `RemoteA2aAgent`. They need a model key and were not run.
