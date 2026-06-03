agent_lifecycle_status = {
    "SecurityAgent": "ACTIVE",
    "CloudAgent": "ACTIVE",
    "FinanceAgent": "INACTIVE",
    "IdentityAgent": "ACTIVE",
    "ComplianceAgent": "ACTIVE",
}


def is_agent_active(agent):
    return agent_lifecycle_status.get(agent) == "ACTIVE"


requests = [
    "SecurityAgent",
    "CloudAgent",
    "FinanceAgent",
    "UnknownAgent",
]

print("\n=== AGENT LIFECYCLE STATUS CHECK ===\n")

for agent in requests:
    status = agent_lifecycle_status.get(agent, "NOT REGISTERED")
    access_status = "CAN REQUEST ACCESS" if is_agent_active(agent) else "ACCESS BLOCKED"

    print(f"{agent} -> {status} -> {access_status}")