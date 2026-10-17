⚡ OmniRelay AI: Autonomous Multimodal Supply Chain Agent
OmniRelay AI is an autonomous, self-correcting supply chain orchestrator designed to solve a critical operational bottleneck in rapid urban commerce: local fulfillment hubs running out of high-velocity inventory while human dispatchers navigate tight shelf constraints, strict budget policies, and return-fraud risks.
Built with Google ADK (google-adk), Google GenAI SDK (Gemini Flash), and the Model Context Protocol (FastMCP), OmniRelay AI automates inventory checks, plans optimal mid-mile transfers, audits operations against corporate risk guardrails, and uses multimodal computer vision to inspect returned packages for broken seals.
🌟 Hackathon Evaluation Highlights
 * Google ADK & GenAI SDK Integration: Leverages Gemini Flash for rapid multi-agent reasoning, tool dispatch, and autonomous plan evaluation.
 * Model Context Protocol (FastMCP): Decoupled, production-ready tool architecture connecting simulated wholesale distribution databases with urban micro-fulfillment hubs.
 * Multimodal Computer Vision: Directly analyzes package and cargo photographs to detect broken tamper-evident seals and transit crushing.
 * Closed Evaluator-Optimizer Feedback Loop: A built-in policy critic flags capacity and financial violations, automatically self-correcting transfer plans before displaying them side-by-side.
 * In-Dialog Conversational Assistant: Allows warehouse leads and dispatchers to query the plan, negotiate batches, or ask follow-up questions within the audit modal.
 * Zero-Friction GCP Execution: Runs natively within Google Cloud Shell without external infrastructure dependencies.
🔄 Schematic Agentic Workflow
+-----------------------------------------------------------------------+
|                1. CLIENT LAYER: GCP Cloud Shell / Streamlit UI        |
+-----------------------------------------------------------------------+
     |                                                      |
     | Natural Language Prompt                              | Package Image
     v                                                      v
+-------------------------------+       +-------------------------------+
|  Dispatch Orchestrator Agent  |       |   Multimodal QA Inspector     |
|     (Google ADK & Gemini)     |       |       (Gemini Flash)          |
+-------------------------------+       +-------------------------------+
     |
     | (Tool Calls)
     v
+-----------------------------------------------------------------------+
|                    3. FAST-MCP TOOL SERVICES                          |
|  * check_microhub_inventory()                                         |
|  * query_upstream_wholesaler()                                        |
|  * dispatch_transfer_order()                                          |
+-----------------------------------------------------------------------+
     |
     | Real-time Telemetry & Catalog Data
     v
+-------------------------------+
|   Initial Action Plan Draft   |
+-------------------------------+
     |
     v
+-----------------------------------------------------------------------+
|              4. EVALUATOR-OPTIMIZER FEEDBACK LOOP                     |
|                                                                       |
|                   [ Risk & Capital Auditor ]                          |
|                                |                                      |
|                                v                                      |
|                    { Policy Check Passes? }                           |
|                     /                    \                            |
|          [ YES: Compliant ]        [ NO: Breach (>50 units / >$5k) ]  |
|                  |                               |                    |
|                  |                               v                    |
|                  |                  [ Auto-Refinement Engine ]        |
|                  \                               /                    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|              5. INTERACTIVE REVIEW MODAL (@st.dialog)                 |
|                                                                       |
|   [ Initial Plan ]               vs.            [ Corrected Plan ]    |
|                                                                       |
|   -----------------------------------------------------------------   |
|   [ In-Dialog Chat Assistant: Live Negotiation & Batch Adjustment ]   |
+-----------------------------------------------------------------------+

🏗️ How the Multi-Agent System Operates
 * Perception & Natural Language Intent: The operator specifies an operational requirement (e.g., handling unexpected stock depletion or planning emergency transfers).
 * MCP Tool Invocations: The Dispatch Agent calls standard MCP tools to query live inventory, evaluate burn rates, and verify wholesale availability.
 * Plan Formulation: An initial operational dispatch plan is generated, detailing proposed transfer counts, unit costs, and logistics ETAs.
 * Policy Audit (The Feedback Loop): The Auditor Agent reviews the proposed action against operational rules (e.g., maximum 50 units per urban hub shelf, maximum $5,000 capital commitment).
 * Self-Correction & Side-by-Side Presentation: If a violation occurs, the agent automatically restructures the transfer into compliant phases and displays both the original and corrected plans side-by-side in an interactive dialog window.
 * Contextual In-Dialog Interaction: The operator can converse with the AI directly inside the modal to ask why specific rules were triggered or request customized delivery intervals.
 * Multimodal Package QA: In parallel, intake workers upload photos of return parcels or incoming shipments to detect structural punctures, torn security tape, or barcode tampering.
🚀 Quickstart: Running in Google Cloud Shell
1. Clone & Set Up the Environment
git clone <YOUR_GITHUB_REPO_URL>
cd omnirelay-ai

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Configure the Gemini API Key
export GEMINI_API_KEY="your-gemini-api-key"

3. Launch the Application
streamlit run app.py \
  --server.port=8080 \
  --server.address=0.0.0.0 \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false

In Google Cloud Shell, click the Web Preview icon in the upper-right corner and select Preview on port 8080.
🧪 Demonstration & Test Scenarios
Test 1: Evaluator-Optimizer Feedback Loop (Self-Correction)
 * Input Prompt:
   We have an urgent enterprise demand surge. Dispatch 150 units of SKU-SSD-1TB to HUB-METRO-EAST immediately.

 * What to Observe:
   * The Dispatch Agent initially attempts to move 150 units ($16,500 total).
   * The Auditor flags the plan for exceeding the 50-unit physical shelf limit and the $5,000 capital limit.
   * The dialog opens with a side-by-side comparison: the initial plan on the left and the self-corrected, compliant phased plan on the right.
Test 2: In-Dialog Contextual Conversation
 * Action: Inside the review dialog, use the chat input at the bottom.
 * Sample Queries:
   * "Why did the original transfer plan fail corporate policy?"
   * "Can you adjust this into 3 delivery waves across today and tomorrow?"
 * What to Observe: The assistant responds strictly within the context of the audit score, financial thresholds, and proposed plans shown above.
Test 3: Multimodal Cargo Inspection & Tamper QA
 * Action: Upload an image of a shipping box, pallet, or retail packaging in the right panel and click Inspect Cargo.
 * What to Observe: The vision engine analyzes physical surfaces and tape lines, delivering a structured report with seal status, packaging integrity, and an actionable verdict (ACCEPT_AND_INVENTORY, REJECT_AND_RETURN, or ESCALATE_FRAUD).
