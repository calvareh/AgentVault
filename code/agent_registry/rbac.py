class Agent:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions


def is_allowed(agent, action):
    return action in agent.permissions


cloud_agent = Agent(
    "CloudAgent",
    ["read_cloud_config", "create_ticket"]
)

security_agent = Agent(
    "SecurityAgent",
    ["read_logs", "approve_changes"]
)

requests = [
    (cloud_agent, "create_ticket"),
    (cloud_agent, "delete_server"),
    (security_agent, "approve_changes"),
    (security_agent, "delete_server"),
]

print("\n=== RBAC PERMISSION CHECKS ===\n")

for agent, action in requests:
    decision = "ALLOWED" if is_allowed(agent, action) else "DENIED"
    print(f"{agent.name} -> {action} -> {decision}")