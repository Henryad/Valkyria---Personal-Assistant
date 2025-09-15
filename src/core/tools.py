import yaml
def tool_mh_color(name: str, cor: str=None, r:int=None, g:int=None, b:int=None) -> str:
name = _alias(name)
c = _find_mh(name)
if not c: return f"MagicHome '{name}' não encontrado."
if cor:
rgb = COLOR_PTBR.get(cor.lower())
if not rgb: return f"Cor '{cor}' não reconhecida."
c.set_color_rgb(*rgb); return f"Cor de '{name}' → {cor}"
c.set_color_rgb(r,g,b); return f"Cor de '{name}' → rgb({r},{g},{b})"


# ===== Outlook =====
from core.outlook_calendar import get_upcoming_events, format_events_brief


def tool_outlook_agenda(dias:int=7, n:int=10) -> str:
evs = get_upcoming_events(days_ahead=dias, max_events=n)
return format_events_brief(evs)


# ===== Registro =====
TOOLS.update({
"tuya_on": {"desc":"Liga uma lâmpada Tuya.","params":{"name":"str"},"fn": tool_tuya_on},
"tuya_off": {"desc":"Desliga uma lâmpada Tuya.","params":{"name":"str"},"fn": tool_tuya_off},
"tuya_brightness": {"desc":"Ajusta brilho (1-100) Tuya.","params":{"name":"str","value":"int"},"fn": tool_tuya_brightness},
"tuya_color": {"desc":"Define cor RGB (Tuya).","params":{"name":"str","r":"int","g":"int","b":"int"},"fn": tool_tuya_color},
"tuya_color_name": {"desc":"Define cor por nome (Tuya).","params":{"name":"str","cor":"str"},"fn": tool_tuya_color_name},


"mh_on": {"desc":"Liga uma fita MagicHome.","params":{"name":"str"},"fn": tool_mh_on},
"mh_off": {"desc":"Desliga uma fita MagicHome.","params":{"name":"str"},"fn": tool_mh_off},
"mh_brightness": {"desc":"Ajusta brilho (1-100) MagicHome.","params":{"name":"str","value":"int"},"fn": tool_mh_brightness},
"mh_color": {"desc":"Define cor por nome OU RGB (MagicHome).","params":{"name":"str","cor":"str","r":"int","g":"int","b":"int"},"fn": tool_mh_color},


"open_app": TOOLS["open_app"],
"what_time_is_it": TOOLS["what_time_is_it"],
"outlook_agenda": {"desc":"Agenda (Outlook Desktop).","params":{"dias":"int","n":"int"},"fn": tool_outlook_agenda},
})


def call_tool(name, args):
t = TOOLS.get(name)
if not t: return f"Ferramenta '{name}' não encontrada."
params = t.get("params", {})
# chamada simples
return t["fn"](**args) if params else t["fn"]()


def spec_for_llm():
return {
"tools": [
{"name":"open_app","description": TOOLS["open_app"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
{"name":"what_time_is_it","description": TOOLS["what_time_is_it"]["desc"],
"parameters":{"type":"object","properties":{}}},
{"name":"tuya_on","description": TOOLS["tuya_on"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
{"name":"tuya_off","description": TOOLS["tuya_off"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
{"name":"tuya_brightness","description": TOOLS["tuya_brightness"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"},"value":{"type":"integer","minimum":1,"maximum":100}},"required":["name","value"]}},
{"name":"tuya_color","description": TOOLS["tuya_color"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"},"r":{"type":"integer"},"g":{"type":"integer"},"b":{"type":"integer"}},"required":["name","r","g","b"]}},
{"name":"tuya_color_name","description": TOOLS["tuya_color_name"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"},"cor":{"type":"string"}},"required":["name","cor"]}},
{"name":"mh_on","description": TOOLS["mh_on"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
{"name":"mh_off","description": TOOLS["mh_off"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
{"name":"mh_brightness","description": TOOLS["mh_brightness"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"},"value":{"type":"integer","minimum":1,"maximum":100}},"required":["name","value"]}},
{"name":"mh_color","description": TOOLS["mh_color"]["desc"],
"parameters":{"type":"object","properties":{"name":{"type":"string"},"cor":{"type":"string"},"r":{"type":"integer"},"g":{"type":"integer"},"b":{"type":"integer"}}}},
{"name":"outlook_agenda","description": TOOLS["outlook_agenda"]["desc"],
"parameters":{"type":"object","properties":{"dias":{"type":"integer","default":7},"n":{"type":"integer","default":10}}}}
]
}
