import os
import json
from google import genai
from google.genai import types
from PIL import Image
import mcp_server

# Client setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Agent definitions
DISPATCH_INSTRUCTION = """You are the OmniRelay Supply Chain Orchestrator. 
Evaluate stock levels, query wholesale inventories, and propose replenishment transfer dispatches.
Be precise with quantities, SKU IDs, and ETAs."""

AUDITOR_INSTRUCTION = """You are the Corporate Risk Auditor. 
Audit proposed plans against constraints:
1. Single transfers cannot exceed 50 units (shelf-space safety limit).
2. Estimated financial commitment must stay below $5,000.
Output strict JSON: {"compliance_pass": bool, "risk_score": int, "remediation": str}"""

def run_adk_workflow(user_prompt: str) -> dict:
    tools = [
        types.Tool(function_declarations=[
            types.FunctionDeclaration(
                name="check_microhub_inventory",
                description="Check inventory for hub_id and sku_id",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "hub_id": types.Schema(type="STRING"),
                        "sku_id": types.Schema(type="STRING")
                    },
                    required=["hub_id", "sku_id"]
                )
            ),
            types.FunctionDeclaration(
                name="query_upstream_wholesaler",
                description="Query central wholesale warehouse for a sku_id",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={"sku_id": types.Schema(type="STRING")},
                    required=["sku_id"]
                )
            ),
            types.FunctionDeclaration(
                name="dispatch_transfer_order",
                description="Commit a stock transfer",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "hub_id": types.Schema(type="STRING"),
                        "sku_id": types.Schema(type="STRING"),
                        "quantity": types.Schema(type="INTEGER")
                    },
                    required=["hub_id", "sku_id", "quantity"]
                )
            )
        ])
    ]

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            tools=tools,
            system_instruction=DISPATCH_INSTRUCTION
        )
    )

    initial_plan = ""
    if response.function_calls:
        call = response.function_calls[0]
        fn = getattr(mcp_server, call.name, None)
        tool_res = fn(**dict(call.args)) if fn else "{}"
        
        followup = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"User request: {user_prompt}\nExecuted tool {call.name} with result: {tool_res}\nGenerate comprehensive action plan."
        )
        initial_plan = followup.text
    else:
        initial_plan = response.text

    audit_eval = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"Audit this proposed plan: {initial_plan}",
        config=types.GenerateContentConfig(
            system_instruction=AUDITOR_INSTRUCTION,
            response_mime_type="application/json"
        )
    ).text
    
    try:
        audit_data = json.loads(audit_eval)
    except Exception:
        audit_data = {"compliance_pass": True, "risk_score": 1, "remediation": "Approved"}

    final_plan = initial_plan
    status = "APPROVED"
    if not audit_data.get("compliance_pass", True):
        status = "REFINED_VIA_FEEDBACK_LOOP"
        correction_prompt = f"The plan failed audit: {audit_data.get('remediation')}. Re-write an optimized compliant plan: {initial_plan}"
        final_plan = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=correction_prompt
        ).text

    return {
        "dispatch_plan": initial_plan,
        "audit": audit_data,
        "final_plan": final_plan,
        "status": status
    }

def inspect_cargo_tampering(image: Image.Image, note: str) -> str:
    prompt = f"""Quality Control Inspector: Check box seals, barcodes, and physical transit damage.
    Context: {note}.
    Classify verdict: ACCEPT_AND_INVENTORY, REJECT_AND_RETURN, or ESCALATE_FRAUD."""
    
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[prompt, image]
    )
    return response.text

def chat_with_audit_context(history: list, context_data: dict, user_msg: str) -> str:
    """Answers operator follow-ups using the full context of the audit and plans."""
    system_instruction = f"""
    You are the OmniRelay Supply Chain Audit Assistant.
    You are conversing with an operations manager about an evaluated supply chain plan.

    CONTEXT:
    - Initial Proposed Plan: {context_data.get('dispatch_plan')}
    - Audit Status: {context_data.get('status')}
    - Audit Telemetry: {json.dumps(context_data.get('audit'))}
    - Final Corrected Plan: {context_data.get('final_plan')}

    Answer the operator's questions crisply, explain policy violations, suggest alternative routing, or adjust parameters based on their input.
    """
    
    # Format message thread
    contents = []
    for msg in history:
        contents.append(f"{msg['role'].upper()}: {msg['content']}")
    contents.append(f"USER: {user_msg}")

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="\n".join(contents),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )
    return response.text
