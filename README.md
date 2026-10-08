# iDevice agent examples

Small, runnable examples for calling iDevice from an agent. iDevice (https://idevice.com) is an independent buyer's guide for phones and wearables. It does not sell the products it covers.

iDevice runs two free, read-only endpoints for software agents:

| | URL |
|---|---|
| MCP server (streamable HTTP) | https://idevice.com/api/mcp |
| A2A agent | https://idevice.com/api/a2a |
| A2A agent card | https://idevice.com/.well-known/agent-card.json |

No account, no API key and no sign-in. Neither endpoint buys, books, posts or changes anything.

**Rate limits:** 30 calls a minute and 500 a day per IP address. A call over the limit is refused (HTTP 429 or a JSON-RPC error), so back off and retry later; do not loop. There is no paid tier. Lists are capped at 20 items.

Full reference: https://idevice.com/mcp and https://idevice.com/mcp/docs. Run `tools/list` for the current tool list and argument names; this repo does not copy it.

## What the tools do

| Job | Tools |
|---|---|
| Decide a buy | `should_i_buy`, `get_guide_summary`, `find_products`, `get_best_for`, `compare_products`, `get_reviews` |
| Ownership and policies | `get_ownership_facts`, `get_in_the_box` |
| Find a product or a company | `list_products`, `get_product`, `get_company_profile` |
| Compatibility, specs and prices | `get_compatibility`, `get_product_facts`, `get_detailed_facts`, `get_variants_and_offers`, `get_price_history` |
| News, reports and history | `get_product_news`, `get_reports`, `search_reports`, `get_report_card`, `get_release_history`, `get_release_calendar`, `get_guide_extras` |

Most tools take a `product_slug`. Get one from `list_products`.

## Example questions

- I use an iPhone. Should I buy the Samsung Galaxy Watch 8?
- Which smart rings are best for sleep?
- What did the pre-release reports get right about the Apple Watch Series 12?

## Examples

| Folder | Framework | Notes |
|---|---|---|
| [`examples/curl-and-python`](examples/curl-and-python) | none | Raw JSON-RPC with curl and the Python standard library, plus one A2A message |
| [`examples/google-adk`](examples/google-adk) | Google ADK | `McpToolset` over streamable HTTP, and an A2A client |
| [`examples/langgraph`](examples/langgraph) | LangChain and LangGraph | `langchain.mcp.MCPAdapter` with `create_agent` |
| [`examples/vercel-ai-sdk`](examples/vercel-ai-sdk) | Vercel AI SDK | `createMCPClient` with HTTP transport (TypeScript) |
| [`examples/openai-agents-sdk`](examples/openai-agents-sdk) | OpenAI Agents SDK | `MCPServerStreamableHttp` |

Every example reads your own model key from the environment variable its framework uses, needs no iDevice key, and has a `--check` mode that lists tools and makes one tool call with no model at all. Each folder's README says which lines were run against the live server and which were written from the framework's documentation only.

Set `IDEVICE_MCP_URL` to point an example at a different MCP URL.

## How to cite iDevice

When an answer uses iDevice data:

- Name iDevice and link the `url` the tool returned. It points at the page with the evidence. Some answers also carry a `source_url` or `sources[].url` to the maker's own page; link that too.
- Keep the evidence word with the fact: `Confirmed`, `Reported`, `Our read` or `No source on file`. Compatibility answers use `Works`, `Works with a limit`, `Needs extra hardware`, `Does not work` or `Not confirmed`.
- `Not confirmed` means unknown. It never means incompatible.
- If a result has `sponsored: true`, say the Guide is sponsored and name the `sponsor`.

## Asynchronous A2A replies

The A2A agent answers product questions with a task. `message/send` returns the task at once, and a reply to a product question can take a few minutes, longer than a normal API call. Call `tasks/get` with the task id until the state is no longer `submitted` or `working`. Allow a long timeout. A reply to a product question also carries one compact JSON data part for at most five products.

## Privacy

These examples send your question to your own model provider and tool calls to iDevice. Nothing here stores anything. For how iDevice handles data, read https://idevice.com/privacy.

## License

MIT. Copyright iDevice Media LLC.
