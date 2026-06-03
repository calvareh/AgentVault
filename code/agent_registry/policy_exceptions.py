approved_exceptions = [
    {
        "agent": "CloudAgent",
        "action": "delete_server",
        "approved_by": "SecurityAgent",
        "duration_hours": 24,
        "status": "APPROVED",
    }
]


def has_approved_exception(agent, action):
    for exception in approved_exceptions:
        if (
            exception["agent"] == agent
            and exception["action"] == action
            and exception["status"] == "APPROVED"
        ):
            return True

    return False


requests = [
    ("CloudAgent", "delete_server"),
    ("FinanceAgent", "delete_server"),
]

print("\n=== POLICY EXCEPTION CHECK ===\n")

for agent, action in requests:
    if has_approved_exception(agent, action):
        print(f"{agent} -> {action} -> EXCEPTION APPROVED")
    else:
        print(f"{agent} -> {action} -> NO EXCEPTION")
    