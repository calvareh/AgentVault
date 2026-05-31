action_risk_levels = {
    "read_cloud_config": "LOW",
    "create_ticket": "LOW",
    "read_logs": "MEDIUM",
    "approve_changes": "MEDIUM",
    "delete_server": "HIGH",
    "modify_iam_policy": "HIGH",
}


def get_action_risk(action):
    return action_risk_levels.get(action, "UNKNOWN")


requests = [
    "create_ticket",
    "read_logs",
    "delete_server",
    "modify_iam_policy",
    "unknown_action",
]

print("\n=== ACTION RISK CLASSIFICATION ===\n")

for action in requests:
    print(f"{action} -> {get_action_risk(action)}")