import band

print("band.Agent exists:", hasattr(band, "Agent"))

try:
    from band.adapters import LangGraphAdapter
    print("LangGraphAdapter: OK")
except Exception as e:
    print("LangGraphAdapter ERROR:", e)

try:
    from band.config import load_agent_config
    print("load_agent_config: OK")
except Exception as e:
    print("load_agent_config ERROR:", e)