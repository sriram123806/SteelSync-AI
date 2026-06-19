
import json

from workflow_memory import (
    get_workflow,
    update_stage,
    complete_workflow,
    is_completed
)


class Gatekeeper:

    # =====================================================
    # EXPECTED AGENTS
    # =====================================================

    EXPECTED_AGENT = {

        "ERP": "steelsync-erp-validator",

        "NORMALIZER": "steelsync-data-normalize",

        "ROUTER": "steelsync-router",

        "ROAD": "steelsync-road-agent",

        "RAIL": "steelsync-rail-agent",

        "PORT": "steelsync-port-agent",

        "INVENTORY": "steelsync-inventory-agen",

        "DEMURRAGE": "steelsync-demurrage-agen",

        "CONSTRAINT": "steelsync-constraint-age",

        "EXCEPTION": "steelsync-exception-agen",

        "SCENARIO": "steelsync-scenario-agent"
    }

    # =====================================================
    # IGNORE CHATTER
    # =====================================================

    IGNORE_WORDS = [

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

        "thank you",
        "thanks",

        "activation request",
        "called to action"
    ]

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.processed_messages = set()

    # =====================================================
    # WORKFLOW CHECK
    # =====================================================

    def workflow_allowed(self, shipment_id):

        if shipment_id is None:
            return False

        workflow = get_workflow(shipment_id)

        if workflow is None:
            return False

        if is_completed(shipment_id):
            return False

        return True

    # =====================================================
    # DUPLICATE MESSAGE PROTECTION
    # =====================================================

    def already_processed(self, message_id):

        if not message_id:
            return False

        if message_id in self.processed_messages:
            return True

        self.processed_messages.add(message_id)

        return False

    # =====================================================
    # IGNORE NON-WORKFLOW CHAT
    # =====================================================

    def should_ignore(self, message):

        if not message:
            return True

        msg = str(message).lower()

        for word in self.IGNORE_WORDS:

            if word in msg:
                return True

        return False

    # =====================================================
    # STRICT JSON VALIDATION
    # =====================================================

    def valid_json(self, message):

        if not message:
            return False

        try:

            data = json.loads(message)

            return isinstance(data, dict)

        except Exception:

            return False

    # =====================================================
    # EXPECTED AGENT CHECK
    # =====================================================

    def allow_response(
        self,
        shipment_id,
        sender
    ):

        workflow = get_workflow(shipment_id)

        if workflow is None:
            return False

        waiting_for = workflow.get(
            "waiting_for"
        )

        if waiting_for is None:
            return False

        expected_agent = self.EXPECTED_AGENT.get(
            waiting_for
        )

        if expected_agent is None:
            return False

        sender = str(sender).lower()

        # DEBUG
        print("WAITING FOR :", waiting_for)
        print("EXPECTED    :", expected_agent)
        print("SENDER      :", sender)


        return expected_agent in sender

    # =====================================================
    # STAGE TRANSITION
    # =====================================================

    def move_to_next_stage(
        self,
        shipment_id,
        next_stage
    ):

        update_stage(
            shipment_id,
            next_stage
        )

    # =====================================================
    # WORKFLOW COMPLETE
    # =====================================================

    def finish_workflow(
        self,
        shipment_id
    ):

        complete_workflow(
            shipment_id
        )

    # =====================================================
    # MASTER VALIDATION
    # =====================================================

    def validate_agent_response(
        self,
        shipment_id,
        sender,
        message,
        message_id
    ):
        print("\n===== DEBUG START =====")
        print("shipment_id =", shipment_id)
        print("sender      =", sender)
        print("message_id  =", message_id)
        # Workflow exists and active

        if not self.workflow_allowed(
            shipment_id
        ):
            return False

        # Prevent duplicate processing

        if self.already_processed(
            message_id
        ):
            return False

        # Ignore greetings/chatter

        if self.should_ignore(
            message
        ):
            return False

        # Verify correct agent

        if not self.allow_response(
            shipment_id,
            sender
        ):
            return False

        # Must be valid JSON

        if not self.valid_json(
            message
        ):
            return False

        return True

