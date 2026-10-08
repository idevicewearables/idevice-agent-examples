# OpenAI Agents SDK

`agent.py`: an `Agent` with `MCPServerStreamableHttp` as its MCP server.

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.10 or later
pip install -r requirements.txt
export OPENAI_API_KEY=...        # your own key
python agent.py                  # the agent loop
python agent.py --check          # no model: list tools, call should_i_buy
```

**Tested against the live server (openai-agents 0.23):** the `MCPServerStreamableHttp` connection, `list_tools()` and one `call_tool` for `should_i_buy`.
**Written from the SDK docs only:** `Agent(...)` and `Runner.run(...)`, which need a model key and were not run.
