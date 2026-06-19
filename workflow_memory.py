
from datetime import datetime


# =====================================================
# GLOBAL MEMORY
# =====================================================

workflow_memory = {}


# =====================================================
# CREATE WORKFLOW
# =====================================================

def create_workflow(
    shipment_id,
    shipment_data
):

    workflow_memory[shipment_id] = {

        "shipment_id": shipment_id,

        "status": "ACTIVE",

        "current_stage": "ERP",

        "waiting_for": "ERP",

        "shipment_data": shipment_data,

        "outputs": {},

        "processed_messages": set(),

        "final_report": None,

        "created_at": datetime.utcnow().isoformat(),

        "completed_at": None
    }

    return True


# =====================================================
# GET WORKFLOW
# =====================================================

def get_workflow(shipment_id):

    return workflow_memory.get(shipment_id)


# =====================================================
# SAVE OUTPUT
# =====================================================

def save_output(
    shipment_id,
    stage,
    output
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    workflow["outputs"][stage] = output

    return True


# =====================================================
# GET OUTPUT
# =====================================================

def get_output(
    shipment_id,
    stage
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return None

    return workflow["outputs"].get(stage)


# =====================================================
# GET ALL OUTPUTS
# =====================================================

def get_all_outputs(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return {}

    return workflow["outputs"]


# =====================================================
# UPDATE STAGE
# =====================================================

def update_stage(
    shipment_id,
    next_stage
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    workflow["current_stage"] = next_stage

    workflow["waiting_for"] = next_stage

    return True


# =====================================================
# CURRENT STAGE
# =====================================================

def get_current_stage(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return None

    return workflow["current_stage"]


# =====================================================
# WAITING FOR
# =====================================================

def get_waiting_for(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return None

    return workflow["waiting_for"]


# =====================================================
# MESSAGE DEDUPLICATION
# =====================================================

def message_already_processed(
    shipment_id,
    message_id
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    return (
        message_id
        in workflow["processed_messages"]
    )


def mark_message_processed(
    shipment_id,
    message_id
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    workflow["processed_messages"].add(
        message_id
    )

    return True


# =====================================================
# FINAL REPORT
# =====================================================

def save_final_report(
    shipment_id,
    report
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    workflow["final_report"] = report

    return True


def get_final_report(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return None

    return workflow["final_report"]


# =====================================================
# COMPLETE WORKFLOW
# =====================================================

def complete_workflow(
    shipment_id
):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    workflow["status"] = "COMPLETED"

    workflow["waiting_for"] = None

    workflow["completed_at"] = (
        datetime.utcnow().isoformat()
    )

    return True


# =====================================================
# COMPLETION CHECK
# =====================================================

def is_completed(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:
        return False

    return workflow["status"] == "COMPLETED"


# =====================================================
# WORKFLOW LOCK
# =====================================================

def workflow_locked(shipment_id):

    return is_completed(shipment_id)


# =====================================================
# DELETE WORKFLOW
# =====================================================

def delete_workflow(shipment_id):

    if shipment_id in workflow_memory:

        del workflow_memory[shipment_id]

        return True

    return False


# =====================================================
# RESET MEMORY
# =====================================================

def reset_memory():

    workflow_memory.clear()


# =====================================================
# DEBUG VIEW
# =====================================================

def print_workflow(shipment_id):

    workflow = get_workflow(shipment_id)

    if workflow is None:

        print(
            f"Workflow {shipment_id} not found"
        )

        return

    print(workflow)


# =====================================================
# LIST ACTIVE WORKFLOWS
# =====================================================

def active_workflows():

    return list(
        workflow_memory.keys()
    )
