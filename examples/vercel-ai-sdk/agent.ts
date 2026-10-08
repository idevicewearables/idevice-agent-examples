// A buy-now-or-wait script for the Vercel AI SDK, using the iDevice MCP server over HTTP.
//   npm start         asks the model; needs OPENAI_API_KEY (your own key)
//   npm run check     no model: lists the tools and runs one through the same MCP client
import { createMCPClient } from "@ai-sdk/mcp";
import { openai } from "@ai-sdk/openai";
import { generateText, isStepCount } from "ai";

const MCP_URL = process.env.IDEVICE_MCP_URL ?? "https://idevice.com/api/mcp";
const MODEL = process.env.IDEVICE_EXAMPLE_MODEL ?? "gpt-4.1-mini"; // any OpenAI chat model
const QUESTION = "Should I buy the Apple Watch Series 12 now or wait? I use an iPhone.";

const SYSTEM = `You help people decide what to buy, using the iDevice tools. Find the product_slug
with list_products, then call should_i_buy. Rules: cite iDevice by name and link the url the
tool returned. Say how sure iDevice is (Confirmed, Reported, Our read, No source on file).
"Not confirmed" means unknown, never incompatible. If a result says sponsored: true, say the
Guide is sponsored and by whom.`;

const mcp = await createMCPClient({ transport: { type: "http", url: MCP_URL } });
try {
  const all = await mcp.tools();
  const names = ["list_products", "should_i_buy", "get_compatibility", "find_products"];
  const tools = Object.fromEntries(Object.entries(all).filter(([name]) => names.includes(name)));

  if (process.argv.includes("--check")) {
    console.log("tools:", Object.keys(tools));
    const result: any = await tools.should_i_buy.execute!(
      { product_slug: "apple-watch", owned_platform: "iphone" },
      { toolCallId: "check", messages: [], context: {} },
    );
    const payload = result.structuredContent ?? JSON.parse(result.content[0].text);
    console.log(payload.headline);
    console.log("url:", payload.url);
  } else {
    const { text, steps } = await generateText({
      model: openai(MODEL),
      system: SYSTEM,
      tools,
      stopWhen: isStepCount(6),
      prompt: QUESTION,
    });
    for (const step of steps) for (const call of step.toolCalls) console.log("tool:", call.toolName, call.input);
    console.log(text);
  }
} finally {
  await mcp.close();
}
