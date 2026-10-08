# curl and Python (no framework)

Raw JSON-RPC against the MCP server, and one A2A message. Standard library only, Python 3.9 or later.

```bash
python idevice.py        # tools/list, then tools/call for list_products, should_i_buy, get_compatibility
python idevice.py a2a    # message/send hello, then tasks/get until the task settles
```

The MCP server answers as server-sent events, so the reply body has `event: message` and `data: {...}` lines. `idevice.py` reads the last `data:` line and decodes the body as UTF-8 explicitly, because the stream declares no charset. The A2A endpoint answers plain JSON.

curl equivalent of `tools/list`:

```bash
curl -s -X POST https://idevice.com/api/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

The script prints the evidence word for each fact, marks `Not confirmed` as unknown, prints `sponsored` Guides, and lists the links to cite.

Needs no model key and no iDevice key.

**Tested against the live server:** `tools/list`, `tools/call` for three tools, A2A `message/send` with a short hello (it completed in the same call) and `tasks/get` on the finished task.
**Written from the A2A spec only:** the polling loop for a task that is still `working`, and the JSON data part of a product reply. A product question was not sent, so that data part was never seen here.
