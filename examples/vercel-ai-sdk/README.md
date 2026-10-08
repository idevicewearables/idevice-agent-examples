# Vercel AI SDK

`agent.ts`: `createMCPClient` from `@ai-sdk/mcp` with the HTTP transport, then `generateText` with the iDevice tools. TypeScript, Node 20 or later.

```bash
npm install
export OPENAI_API_KEY=...        # your own key; set IDEVICE_EXAMPLE_MODEL to change the model
npm start                        # the agent loop
npm run check                    # no model: list tools, run should_i_buy
```

The script closes the MCP client in a `finally` block.

**Tested against the live server (ai 7.0, @ai-sdk/mcp 2.0):** the HTTP transport connection, `tools()`, and one `should_i_buy` call through the tool's `execute`. The whole file also type-checks with `tsc`.
**Written from the AI SDK docs only:** the `generateText` call with `stopWhen: isStepCount(6)`, which type-checks but was not run because it needs a model key.
