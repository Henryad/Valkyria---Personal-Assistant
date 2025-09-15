import json, os
MEM_PATH = "memory.json"


def load_mem():
if os.path.exists(MEM_PATH):
return json.load(open(MEM_PATH,"r",encoding="utf-8"))
return {}


def save_mem(d):
json.dump(d, open(MEM_PATH,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
