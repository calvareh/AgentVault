agents = {
    "CloudAgent": ["read_cloud_config", "create_ticket"],
    "SecurityAgent": ["read_logs", "approve_changes", "modify_iam_policy"],
}

action_risk = {
    "create_ticket": "LOW",
    "read_logs": "MEDIUM",
    "delete_server": "HIGH",
    "modify_iam_policy": "HIGH",
}


def evaluate_request(agent_name, action):
    permissions = agents.get(agent_name, [])
    risk = action_risk.get(action, "UNKNOWN")

    if action not in permissions:
        return "DENIED"

    if risk == "HIGH":
        return "APPROVAL REQUIRED"

    return "ALLOWED"


requests = [
    ("CloudAgent", "create_ticket"),
    ("CloudAgent", "delete_server"),
    ("SecurityAgent", "read_logs"),
    ("SecurityAgent", "modify_iam_policy"),
]

print("\n=== POLICY ENGINE DECISIONS ===\n")

for agent, action in requests:
    print(f"{agent} -> {action} -> {evaluate_request(agent, action)}")