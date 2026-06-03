import json
from pathlib import Path
from collections import Counter

import streamlit as st

AGENT_REGISTRY_PATH = Path("data/agents.json")
AUDIT_LOG_PATH = Path("data/agentvault_engine_audit.jsonl")

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
        "Permissions": ", ".join(agent["permissions"]),
    }
    for agent in registered_agents
]

st.dataframe(agent_inventory)

st.subheader("Audit Events")

st.dataframe(events)