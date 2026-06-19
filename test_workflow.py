# test_workflow.py

from main import (
    process_new_shipment,
    process_agent_response
)

shipment = {
    "shipment_id":"TEST001",
    "origin":"Chennai",
    "destination":"Mumbai",
    "cargo_type":"Steel",
    "weight_kg":25000
}

process_new_shipment(shipment)

process_agent_response(
    "TEST001",
    "steelsync-erp-validator",
    '{"shipment_id":"TEST001","status":"passed"}',
    "msg1"
)

process_agent_response(
    "TEST001",
    "steelsync-router",
    '{"shipment_id":"TEST001","transport_mode":"ROAD","status":"completed"}',
    "msg2"
)

process_agent_response(
    "TEST001",
    "steelsync-inventory-agen",
    '{"shipment_id":"TEST001","inventory_status":"AVAILABLE","status":"completed"}',
    "msg3"
)

process_agent_response(
    "TEST001",
    "steelsync-demurrage-agen",
    '{"shipment_id":"TEST001","demurrage_risk":"LOW","status":"completed"}',
    "msg4"
)

process_agent_response(
    "TEST001",
    "steelsync-scenario-agent",
    '{"shipment_id":"TEST001","best_case":"On Time","expected_case":"Minor Delay","worst_case":"Major Delay","status":"completed"}',
    "msg5"
)