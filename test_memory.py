# test_memory.py

from workflow_memory import *

create_workflow(
    "TEST001",
    {"cargo":"steel"}
)

print(get_workflow("TEST001"))

update_stage(
    "TEST001",
    "ROUTER"
)

print(get_workflow("TEST001"))

complete_workflow(
    "TEST001"
)

print(is_completed("TEST001"))