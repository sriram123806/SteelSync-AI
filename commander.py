import json


class Commander:

    # =====================================================
    # AGENT HANDLES
    # =====================================================

    AGENT_HANDLES = {
        "ERP": "@sri123ram2712/steelsync-erp-validator",
        "NORMALIZER": "@sri123ram2712/steelsync-data-normalize",
        "ROUTER": "@sri123ram2712/steelsync-router",

        "ROAD": "@sri123ram2712/steelsync-road-agent",
        "RAIL": "@sri123ram2712/steelsync-rail-agent",
        "PORT": "@sri123ram2712/steelsync-port-agent",

        "INVENTORY": "@sri123ram2712/steelsync-inventory-agen",
        "DEMURRAGE": "@sri123ram2712/steelsync-demurrage-agen",
        "CONSTRAINT": "@sri123ram2712/steelsync-constraint-age",
        "EXCEPTION": "@sri123ram2712/steelsync-exception-agen",
        "SCENARIO": "@sri123ram2712/steelsync-scenario-agent"
    }
    

    NEXT_STAGE = {
        "ERP": "ROUTER",
        "ROUTER": "INVENTORY",
        "INVENTORY": "DEMURRAGE",
        "DEMURRAGE": "SCENARIO",
        "SCENARIO": "COMPLETED"
    }

    # =====================================================
    # WORKFLOW ORDER
    # =====================================================
     
     
    # NEXT_STAGE = {

    #     "ERP": "NORMALIZER",

    #     "NORMALIZER": "ROUTER",

    #     "ROAD": "INVENTORY",
    #     "RAIL": "INVENTORY",
    #     "PORT": "INVENTORY",

    #     "INVENTORY": "DEMURRAGE",

    #     "DEMURRAGE": "CONSTRAINT",

    #     "CONSTRAINT": "EXCEPTION",

    #     "EXCEPTION": "SCENARIO",

    #     "SCENARIO": "COMPLETED"
    # }
      
    # =====================================================
    # IGNORE CHATTER
    # =====================================================

    IGNORE_MESSAGES = [

        "hello",
        "hi",
        "hey",

        "received",
        "acknowledged",
        "acknowledgement",

        "processing",
        "please wait",
        "wait",
        "hold on",

        "assist you",
        "how can i help",

        "activation request",
        "called to action",

        "thank you",
        "thanks"
    ]

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.completed_shipments = set()

    # =====================================================
    # JSON VALIDATION
    # =====================================================

    def is_valid_json(self, text):

        if not text:
            return False

        try:

            obj = json.loads(text)

            return isinstance(obj, dict)

        except Exception:

            return False

    # =====================================================
    # IGNORE NON-WORKFLOW MESSAGES
    # =====================================================

    def should_ignore(self, message):

        if not message:
            return True

        msg = str(message).lower()

        for word in self.IGNORE_MESSAGES:

            if word in msg:
                return True

        return False

    # =====================================================
    # SHIPMENT COMPLETION LOCK
    # =====================================================

    def is_completed(self, shipment_id):

        return shipment_id in self.completed_shipments

    def mark_completed(self, shipment_id):

        self.completed_shipments.add(shipment_id)

    # =====================================================
    # AGENT HELPERS
    # =====================================================

    def get_handle(self, stage):

        return self.AGENT_HANDLES.get(stage)

    def next_stage(self, current_stage):

        return self.NEXT_STAGE.get(current_stage)

    # =====================================================
    # ROUTER DECISION
    # =====================================================

    def select_transport(self, router_json):

        if not isinstance(router_json, dict):
            return "ROAD"

        mode = str(
            router_json.get(
                "transport_mode",
                "ROAD"
            )
        ).upper()

        if mode == "ROAD":
            return "ROAD"

        if mode == "RAIL":
            return "RAIL"

        if mode == "PORT":
            return "PORT"

        return "ROAD"

    # =====================================================
    # WORKFLOW STATUS MESSAGES
    # =====================================================

    def workflow_started(self, shipment_id):

        return (
            f"[WORKFLOW STARTED]\n"
            f"Shipment ID : {shipment_id}"
        )

    def calling_agent(self, stage):

        return (
            f"{self.get_handle(stage)} "
            f"Calling {stage}"
        )

    def output_received(self, stage):

        return (
            f"{stage} Output Received"
        )

    def workflow_completed(self, shipment_id):

        self.mark_completed(shipment_id)

        return (
            "\n"
            "================================\n"
            "WORKFLOW COMPLETED\n"
            f"Shipment : {shipment_id}\n"
            "Final Report Generated\n"
            "================================"
        )

    # =====================================================
    # FINAL REPORT
    # =====================================================

    def generate_final_report(self, shipment_id, memory):

        return f"""
================================

FINAL REPORT

Shipment ID:
{shipment_id}

--------------------------------

ERP Result:
{memory.get("ERP", {})}

--------------------------------

Normalized Data:
{memory.get("NORMALIZER", {})}

--------------------------------

Routing Result:
{memory.get("ROUTER", {})}

--------------------------------

Transport Result:
{memory.get("TRANSPORT", {})}

--------------------------------

Inventory Result:
{memory.get("INVENTORY", {})}

--------------------------------

Demurrage Result:
{memory.get("DEMURRAGE", {})}

--------------------------------

Constraint Result:
{memory.get("CONSTRAINT", {})}

--------------------------------

Exception Result:
{memory.get("EXCEPTION", {})}

--------------------------------

Scenario Result:
{memory.get("SCENARIO", {})}

================================
"""
