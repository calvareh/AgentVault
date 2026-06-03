import json


def load_agents():
    with open("data/agents.json", "r") as file:
        return json.load(file)


agents = load_agents()

print("\n=== AGENT REGISTRY ===\n")

for agent in agents:
    print(
        f"{agent['role']} "
        f"({agent['agent_id']})"
    )