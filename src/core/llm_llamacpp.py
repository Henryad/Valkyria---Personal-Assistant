from llama_cpp import Llama
import json


SYSTEM_PROMPT = """Você é a **Valkyria** (Val), assistente pessoal do Henry.
Fale curto, objetivo, em PT-BR. Use um tom confiante e gentil.
Se precisar executar uma ação, chame uma ferramenta em JSON válido:
{"tool":"NOME","args":{...}}
Responda com texto normal se não precisar de ferramenta.
Confirme ações perigosas antes de executar.
Respeite preferências do Henry quando conhecidas.
"""


class LocalLLM:
def __init__(self, model_path, n_ctx=4096, n_threads=6, temperature=0.4):
self.llm = Llama(model_path=model_path, n_ctx=n_ctx, n_threads=n_threads, verbose=False)
self.temperature = temperature


def decide(self, user_text, tools_schema):
prompt = (
f"<|system|>\n{SYSTEM_PROMPT}\n"
f"Ferramentas disponíveis:\n{json.dumps(tools_schema, ensure_ascii=False)}\n</|system|>\n"
f"<|user|>\n{user_text}\n</|user|>\n<|assistant|>\n"
)
out = self.llm(prompt, max_tokens=256, temperature=self.temperature, stop=["</|assistant|>", "<|user|>"])
text = out["choices"][0]["text"].strip()
try:
data = json.loads(text)
if isinstance(data, dict) and "tool" in data:
return {"type":"tool_call","tool":data["tool"],"args":data.get("args",{})}
except Exception:
pass
return {"type":"message","text":text}
