# test_gatekeeper.py

from gatekeeper import Gatekeeper

g = Gatekeeper()

msg = """
{
 "shipment_id":"TEST001",
 "status":"completed"
}
"""

print(
    g.valid_json(msg)
)