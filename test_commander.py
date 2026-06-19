from commander import Commander

c = Commander()

print(c.workflow_started("TEST001"))

print(c.calling_agent("ERP"))

print(c.next_stage("ERP"))
print(c.next_stage("ROUTER"))
print(c.next_stage("INVENTORY"))
print(c.next_stage("DEMURRAGE"))
print(c.next_stage("SCENARIO"))