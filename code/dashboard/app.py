import json
from pathlib import Path
from collections import Counter

import streamlit as st

AGENT_REGISTRY_PATH = Path("data/agents.json")
AUDIT_LOG_PATH = Path("data/agentvault_engine_audit.jsonl")

RISK_LEVEL_SCORES = {
    "LOW": 20,
    "MEDIUM": 50,
    "HIGH": 80,
}


def calculate_agent_risk_score(agent):
    base_score = RISK_LEVEL_SCORES.get(agent["risk_level"], 0)
    permission_score = len(agent["permissions"]) * 5

    return min(base_score + permission_score, 100)

st.set_page_config(
    page_title="AgentVault Dashboard",
    layout="wide"
)

st.title("AgentVault Security Dashboard")
st.caption("AI Agent Identity Governance, Policy Decisions, and Audit Visibility")

if not AUDIT_LOG_PATH.exists():
    st.warning("No audit log found. Run the AgentVault decision engine first.")
    st.stop()

events = []

with open(AUDIT_LOG_PATH, "r") as file:
    for line in file:
        events.append(json.loads(line))

decision_counts = Counter(event["decision"] for event in events)
with open(AGENT_REGISTRY_PATH, "r") as file:
    registered_agents = json.load(file)

registered_agent_count = len(registered_agents)
active_agent_count = len(set(event["agent"] for event in events))

active_agent_roles = set(event["agent"] for event in events)

inactive_agents = [
    agent for agent in registered_agents
    if agent["role"] not in active_agent_roles
]

st.subheader("Governance Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Registered Agents", registered_agent_count)
col2.metric("Active Agents", active_agent_count)
col3.metric("Allowed", decision_counts.get("ALLOWED", 0))
col4.metric("Denied", decision_counts.get("DENIED", 0))
col5.metric("Approval Required", decision_counts.get("APPROVAL REQUIRED", 0))

st.subheader("Decision Distribution")

chart_data = [
    {"decision": decision, "count": count}
    for decision, count in decision_counts.items()
]

st.bar_chart(chart_data, x="decision", y="count")

st.subheader("Registered Agent Inventory")

agent_inventory = [
    {
        "Agent ID": agent["agent_id"],
        "Name": agent["name"],
        "Role": agent["role"],
        "Risk Level": agent["risk_level"],
        "Risk Score": calculate_agent_risk_score(agent),
        "Permissions": ", ".join(agent["permissions"]),
    }
    for agent in registered_agents
]

st.dataframe(agent_inventory, use_container_width=True)

st.subheader("Inactive Agents")

if inactive_agents:
    st.warning("The following registered agents have no audit activity yet:")

    inactive_agent_table = [
        {
            "Agent ID": agent["agent_id"],
            "Name": agent["name"],
            "Role": agent["role"],
            "Risk Level": agent["risk_level"],
        }
        for agent in inactive_agents
    ]

    st.dataframe(inactive_agent_table, use_container_width=True)
else:
    st.success("All registered agents have audit activity.")

st.subheader("Agent Risk Summary")

risk_summary = {}

for agent in registered_agents:
    risk = agent["risk_level"]
    risk_summary[risk] = risk_summary.get(risk, 0) + 1

risk_chart_data = [
    {"Risk Level": risk, "Agent Count": count}
    for risk, count in risk_summary.items()
]

st.subheader("High Risk Agents")

high_risk_agents = [
    {
        "Agent ID": agent["agent_id"],
        "Role": agent["role"],
        "Risk Score": calculate_agent_risk_score(agent),
    }
    for agent in registered_agents
    if calculate_agent_risk_score(agent) >= 80
]

if high_risk_agents:
    st.warning(
        f"{len(high_risk_agents)} high-risk agents require enhanced governance oversight."
    )

    st.dataframe(
        high_risk_agents,
        use_container_width=True
    )
else:
    st.success("No high-risk agents detected.")

st.bar_chart(risk_chart_data, x="Risk Level", y="Agent Count")

st.subheader("Audit Events")

st.dataframe(events, use_container_width=True)