# test_erp.py

from band.config import load_agent_config

agent_id, api_key = load_agent_config("erp_validator")

print("ERP Agent ID:", agent_id)
print("ERP API Key:", api_key[:15] + "...")