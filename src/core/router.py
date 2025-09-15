rom core.tools import call_tool


def route_decision(llm_decision):
if llm_decision["type"] == "tool_call":
name = llm_decision["tool"]
args = llm_decision.get("args", {})
result = call_tool(name, args)
return result
return llm_decision.get("text","Certo.")
