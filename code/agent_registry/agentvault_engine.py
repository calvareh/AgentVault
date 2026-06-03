from datetime import datetime
import json
import os


AUDIT_LOG_FILE = "data/agentvault_engine_audit.jsonl"

agents = {
    "CloudAgent": ["read_cloud_config", "create_ticket"],
    "SecurityAgent": ["read_logs", "approve_changes", "modify_iam_policy"],
    "FinanceAgent": ["read_reports"],
    "IdentityAgent": ["review_access", "certify_access", "read_identity_data"],
    "ComplianceAgent": ["read_audit_logs", "generate_reports", "check_controls"],
}

action_risk = {
    "create_ticket": "LOW",
    "read_cloud_config": "LOW",
    "read_reports": "LOW",
    "read_logs": "MEDIUM",
    "approve_changes": "MEDIUM",
    "review_access": "MEDIUM",
    "generate_reports": "MEDIUM",
    "delete_server": "HIGH",
    "modify_iam_policy": "HIGH",
}


def evaluate_request(agent_name, action):
    permissions = agents.get(agent_name, [])
    risk = action_risk.get(action, "UNKNOWN")

    if action not in permissions:
        return risk, "DENIED"

    if risk == "HIGH":
        return risk, "APPROVAL REQUIRED"

    return risk, "ALLOWED"


def write_audit_event(agent, action, risk, decision):
    os.makedirs("data", exist_ok=True)

    audit_event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "action": action,
        "risk": risk,
        "decision": decision,
    }

    with open(AUDIT_LOG_FILE, "a") as file:
        file.write(json.dumps(audit_event) + "\n")

    return audit_event


requests = [
    ("CloudAgent", "create_ticket"),
    ("CloudAgent", "delete_server"),
    ("SecurityAgent", "read_logs"),
    ("SecurityAgent", "modify_iam_policy"),
    ("IdentityAgent", "review_access"),
    ("ComplianceAgent", "generate_reports"),
]

print("\n=== AGENTVAULT DECISION ENGINE ===\n")

for agent, action in requests:
    risk, decision = evaluate_request(agent, action)
    write_audit_event(agent, action, risk, decision)

    print(f"{agent} -> {action}")
    print(f"Risk: {risk}")
    print(f"Decision: {decision}\n")

print("Audit events written successfully.")