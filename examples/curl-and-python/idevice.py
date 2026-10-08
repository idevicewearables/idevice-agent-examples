"""Raw JSON-RPC against the iDevice MCP server and A2A agent. Standard library only.

    python idevice.py        # tools/list, then three tools/call requests
    python idevice.py a2a    # one A2A message/send, then tasks/get until it settles
"""
import json, os, sys, time, urllib.error, urllib.request, uuid

MCP_URL = os.environ.get("IDEVICE_MCP_URL", "https://idevice.com/api/mcp")
A2A_URL = os.environ.get("IDEVICE_A2A_URL", "https://idevice.com/api/a2a")


def rpc(url, method, params=None, rpc_id=1):
    body = {"jsonrpc": "2.0", "id": rpc_id, "method": method}
    if params is not None:
        body["params"] = params
    headers = {"content-type": "application/json", "accept": "application/json, text/event-stream"}
    req = urllib.request.Request(url, json.dumps(body).encode(), headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")  # no charset header on the stream: decode as UTF-8 yourself
    except urllib.error.HTTPError as err:
        if err.code == 429:  # 30 calls a minute and 500 a day per IP: back off, do not loop
            sys.exit("Rate limit reached. Wait a minute and try again.")
        raise
    # MCP answers as server-sent events ("event: message" then "data: {...}"). A2A answers plain JSON.
    frames = [line[5:].strip() for line in text.splitlines() if line.startswith("data:")]
    reply = json.loads(frames[-1] if frames else text)
    if "error" in reply:
        raise RuntimeError(reply["error"])
    return reply["result"]


def call_tool(name, arguments):
    result = rpc(MCP_URL, "tools/call", {"name": name, "arguments": arguments})
    if result.get("isError"):
        raise RuntimeError(result["content"][0]["text"])
    return result.get("structuredContent") or json.loads(result["content"][0]["text"])


def show(payload):
    """Print how sure iDevice is, flag sponsored Guides, and list every link to cite."""
    urls = []
    def walk(node):
        if isinstance(node, dict):
            if node.get("sponsored"):
                print("  SPONSORED Guide:", node.get("sponsor"), "-", node.get("sponsor_note"))
            if node.get("headline"):
                print("  ", node["headline"])
            sure = node.get("how_sure") or node.get("evidence")
            answer = node.get("answer") or node.get("verdict")
            if sure and answer:
                note = "  (unknown, not incompatible)" if "not confirmed" in str(answer).lower() else ""
                print(f"  {answer} [{sure}]{note}")
            for key in ("url", "source_url"):
                if isinstance(node.get(key), str) and node[key] not in urls:
                    urls.append(node[key])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk(payload)
    print("  Cite iDevice and link:", *urls[:5], sep="\n    ")


def mcp_demo():
    tools = rpc(MCP_URL, "tools/list")["tools"]
    print(f"tools/list returned {len(tools)} tools:", ", ".join(t["name"] for t in tools))
    for name, args in [
        ("list_products", {"query": "apple watch"}),
        ("should_i_buy", {"product_slug": "apple-watch", "owned_platform": "iphone"}),
        ("get_compatibility", {"product_slug": "apple-watch", "query": "android"}),
    ]:
        print(f"\n{name} {args}")
        time.sleep(3)  # the server allows 30 calls a minute and 500 a day per IP
        show(call_tool(name, args))


def a2a_demo():
    text = "Hello. In one sentence, what can you help with?"
    message = {"kind": "message", "messageId": str(uuid.uuid4()), "role": "user", "parts": [{"kind": "text", "text": text}]}
    task = rpc(A2A_URL, "message/send", {"message": message})
    while task["status"]["state"] in ("submitted", "working"):  # a product question can take minutes
        time.sleep(10)
        task = rpc(A2A_URL, "tasks/get", {"id": task["id"]})
    print("state:", task["status"]["state"])
    for part in task["status"].get("message", {}).get("parts", []):
        # 0.3 parts carry kind "text" or "data"; 1.0 parts carry "text" or "data" with a mediaType
        if "text" in part:
            print(part["text"])
        elif "data" in part:
            show(part["data"])


if __name__ == "__main__":
    a2a_demo() if sys.argv[1:] == ["a2a"] else mcp_demo()
