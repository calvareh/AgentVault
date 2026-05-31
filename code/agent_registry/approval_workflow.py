high_risk_actions = [
    "delete_server",
    "modify_iam_policy",
]


def requires_approval(action):
    return action in high_risk_actions


requests = [
    "create_ticket",
    "read_logs",
    "delete_server",
    "modify_iam_policy",
]

print("\n=== APPROVAL WORKFLOW CHECK ===\n")

for action in requests:
    decision = "APPROVAL REQUIRED" if requires_approval(action) else "NO APPROVAL NEEDED"
    print(f"{action} -> {decision}")