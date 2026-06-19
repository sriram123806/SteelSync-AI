import json

from workflow_memory import (
    create_workflow,
    get_workflow,
    save_output,
    save_final_report,
    mark_message_processed,
    is_completed
)

from gatekeeper import Gatekeeper
from commander import Commander


# =====================================================
# GLOBALS
# =====================================================

gatekeeper = Gatekeeper()
commander = Commander()


# =====================================================
# NEW SHIPMENT
# =====================================================

def process_new_shipment(shipment):

    shipment_id = shipment.get("shipment_id")

    if not shipment_id:
        print("[ERROR] shipment_id missing")
        return

    if is_completed(shipment_id):
        print(f"[LOCKED] {shipment_id}")
        return

    workflow = get_workflow(shipment_id)

    if workflow is not None:
        print(f"[EXISTS] {shipment_id}")
        return

    create_workflow(
        shipment_id,
        shipment
    )

    print(
        commander.workflow_started(
            shipment_id
        )
    )

    print(
        commander.calling_agent(
            "ERP"
        )
    )


# =====================================================
# PROCESS AGENT RESPONSE
# =====================================================

def process_agent_response(
    shipment_id,
    sender,
    message,
    message_id
):

    workflow = get_workflow(
        shipment_id
    )

    if workflow is None:
        print("[ERROR] Workflow not found")
        return

    if is_completed(shipment_id):
        print(f"[COMPLETED] {shipment_id}")
        return

    # -------------------------------------------------
    # GATEKEEPER VALIDATION
    # -------------------------------------------------
    print(f"[ACCEPTED] {sender}")
    # if not gatekeeper.validate_agent_response(
    #     shipment_id,
    #     sender,
    #     message,
    #     message_id
    # ):
    #     print(f"[REJECTED] {sender}")
    #     return

    # print(f"[ACCEPTED] {sender}")

    # -------------------------------------------------
    # MARK MESSAGE PROCESSED
    # -------------------------------------------------

    mark_message_processed(
        shipment_id,
        message_id
    )

    # -------------------------------------------------
    # PARSE JSON
    # -------------------------------------------------

    try:

        output_json = json.loads(
            message
        )

    except Exception:

        print("[INVALID JSON]")
        return

    # -------------------------------------------------
    # CURRENT STAGE
    # -------------------------------------------------

    current_stage = workflow[
        "current_stage"
    ]

    # -------------------------------------------------
    # SAVE OUTPUT
    # -------------------------------------------------

    save_output(
        shipment_id,
        current_stage,
        output_json
    )

    print(
        commander.output_received(
            current_stage
        )
    )

    # -------------------------------------------------
    # NEXT STAGE
    # -------------------------------------------------

    next_stage = commander.next_stage(
        current_stage
    )

    # -------------------------------------------------
    # WORKFLOW COMPLETE
    # -------------------------------------------------

    if next_stage == "COMPLETED":

        report = (
            commander.generate_final_report(
                shipment_id,
                workflow["outputs"]
            )
        )

        save_final_report(
            shipment_id,
            report
        )

        print(report)

        gatekeeper.finish_workflow(
            shipment_id
        )

        print(
            commander.workflow_completed(
                shipment_id
            )
        )

        return

    # -------------------------------------------------
    # MOVE TO NEXT STAGE
    # -------------------------------------------------

    gatekeeper.move_to_next_stage(
        shipment_id,
        next_stage
    )

    print(
        commander.calling_agent(
            next_stage
        )
    )


# =====================================================
# LOCAL TEST
# =====================================================

if __name__ == "__main__":

    shipment = {

        "shipment_id": "TEST001",

        "origin": "Chennai",

        "destination": "Mumbai",

        "cargo_type": "Steel Coils",

        "weight_kg": 25000,

        "container_count": 2
    }

    process_new_shipment(
        shipment
    )