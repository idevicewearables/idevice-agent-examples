# LangChain and LangGraph

`agent.py`: a small shopping agent. `langchain.mcp.MCPAdapter` turns the iDevice tools into LangChain tools and `langchain.agents.create_agent` (built on LangGraph) runs the loop. This uses the `mcp` extra of the `langchain` package. The older `langchain-mcp-adapters` repository is archived. `langchain.mcp` is marked beta and prints a warning on import.

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.10 or later
pip install -r requirements.txt
export OPENAI_API_KEY=...        # your own key; set IDEVICE_EXAMPLE_MODEL to change the model
python agent.py                  # the agent loop
python agent.py --check          # no model: list tools, call should_i_buy
```

The transport is named (`StreamableHttpTransport`) so the connection is streamable HTTP and not guessed from the URL.

**Tested against the live server (langchain 1.4, fastmcp 4.0):** the adapter connection, tool listing and one `should_i_buy` call with `ainvoke`.
**Written from the LangChain docs only:** `create_agent(...)` and the `ainvoke` agent loop, the prompt, and the default model string. They need a model key and were not run.
