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

def evaluate_compliance_status(agent):
    sensitive_permissions = {"modify_iam_policy", "approve_changes"}

    has_cloud_identity = "cloud_identity" in agent
    has_permissions_profile = "cloud_permissions_profile" in agent
    has_sensitive_permissions = bool(
        sensitive_permissions.intersection(set(agent["permissions"]))
    )

    if agent["status"] == "INACTIVE" and has_cloud_identity:
        return "NON-COMPLIANT"

    if has_cloud_identity and not has_permissions_profile:
        return "NON-COMPLIANT"

    if agent["risk_level"] == "HIGH" or has_sensitive_permissions:
        return "REVIEW REQUIRED"

    return "COMPLIANT"

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
    if agent["status"] == "INACTIVE"
]

compliant_count = 0
review_required_count = 0
non_compliant_count = 0

for agent in registered_agents:
    compliance_status = evaluate_compliance_status(agent)

    if compliance_status == "COMPLIANT":
        compliant_count += 1
    elif compliance_status == "REVIEW REQUIRED":
        review_required_count += 1
    elif compliance_status == "NON-COMPLIANT":
        non_compliant_count += 1

governance_score = round(
    (compliant_count / registered_agent_count) * 100,
    1
)

st.subheader("Governance Summary")

col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

col1.metric("Registered Agents", registered_agent_count)
col2.metric("Active Agents", active_agent_count)
col3.metric("Allowed", decision_counts.get("ALLOWED", 0))
col4.metric("Denied", decision_counts.get("DENIED", 0))
col5.metric("Approval Required", decision_counts.get("APPROVAL REQUIRED", 0))
col6.metric("Compliant", compliant_count)
col7.metric("Review Required", review_required_count)
col8.metric("Non-Compliant", non_compliant_count)
col9.metric("Governance Score", f"{governance_score}%")

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
        "Status": agent["status"],
        "Compliance Status": evaluate_compliance_status(agent),
        "Permissions Profile": agent.get("cloud_permissions_profile", "N/A"),
        "Cloud Provider": agent.get("cloud_identity", {}).get("provider", "N/A"),
        "Cloud Role": agent.get("cloud_identity", {}).get("role_name", "N/A"),
        "Managed By": agent.get("cloud_identity", {}).get("managed_by", "N/A"),
        "Permissions": ", ".join(agent["permissions"]),
    }
    for agent in registered_agents
]
st.dataframe(agent_inventory, use_container_width=True)

st.subheader("Inactive Agents")

if inactive_agents:
    st.warning(
    "The following registered agents are currently inactive and cannot request access."
)

    inactive_agent_table = [
        {
            "Agent ID": agent["agent_id"],
            "Name": agent["name"],
            "Role": agent["role"],
            "Risk Level": agent["risk_level"],
            "Status": agent["status"],
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

st.subheader("Compliance Summary")

compliance_summary = {}

for agent in registered_agents:
    status = evaluate_compliance_status(agent)
    compliance_summary[status] = compliance_summary.get(status, 0) + 1

compliance_chart_data = [
    {"Compliance Status": status, "Agent Count": count}
    for status, count in compliance_summary.items()
]

st.bar_chart(
    compliance_chart_data,
    x="Compliance Status",
    y="Agent Count"
)

st.subheader("Agent Risk Summary")

st.bar_chart(risk_chart_data, x="Risk Level", y="Agent Count")

st.subheader("Audit Events")

st.dataframe(events, use_container_width=True)