# test_create.py

from band.config import load_agent_config

for name in ["my_agent", "erp_validator"]:
    agent_id, api_key = load_agent_config(name)
    print(name)
    print("  ID :", agent_id)
    print("  KEY:", api_key[:20] + "...")