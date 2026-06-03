import json


RISK_LEVEL_SCORES = {
    "LOW": 20,
    "MEDIUM": 50,
    "HIGH": 80,
}


def load_agents():
    with open("data/agents.json", "r") as file:
        return json.load(file)


def calculate_agent_risk_score(agent):
    base_score = RISK_LEVEL_SCORES.get(agent["risk_level"], 0)
    permission_score = len(agent["permissions"]) * 5

    return min(base_score + permission_score, 100)


agents = load_agents()

print("\n=== AGENT RISK SCORING ===\n")

for agent in agents:
    score = calculate_agent_risk_score(agent)
    print(f"{agent['role']} -> Risk Score: {score}")