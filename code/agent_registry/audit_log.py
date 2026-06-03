from datetime import datetime
import json
import os


AUDIT_LOG_FILE = "data/audit_log.jsonl"


def write_audit_event(agent, action, decision):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    audit_event = {
        "timestamp": timestamp,
        "agent": agent,
        "action": action,
        "decision": decision,
    }

    os.makedirs("data", exist_ok=True)

    with open(AUDIT_LOG_FILE, "a") as file:
        file.write(json.dumps(audit_event) + "\n")

    return audit_event


events = [
    ("CloudAgent", "create_ticket", "ALLOWED"),
    ("CloudAgent", "delete_server", "DENIED"),
    ("SecurityAgent", "modify_iam_policy", "APPROVAL REQUIRED"),
]

print("\n=== AUDIT EVENTS WRITTEN ===\n")

for agent, action, decision in events:
    event = write_audit_event(agent, action, decision)
    print(event)