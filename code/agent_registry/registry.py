class Agent:
    def __init__(self, agent_id, name, role, permissions, risk_level):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.permissions = permissions
        self.risk_level = risk_level

    def __str__(self):
        return (
            f"Agent(id={self.agent_id}, "
            f"name={self.name}, "
            f"role={self.role}, "
            f"risk={self.risk_level})"
        )


agents = [
    Agent(
        "SEC-001",
        "Security Review Agent",
        "SecurityAgent",
        ["read_logs", "approve_changes", "review_policy"],
        "HIGH"
    ),
    Agent(
        "CLD-001",
        "Cloud Operations Agent",
        "CloudAgent",
        ["read_cloud_config", "create_ticket"],
        "MEDIUM"
    ),
    Agent(
        "FIN-001",
        "Finance Analysis Agent",
        "FinanceAgent",
        ["read_reports"],
        "LOW"
    ),
    Agent(
        "IAM-001",
        "Identity Governance Agent",
        "IdentityAgent",
        ["review_access", "certify_access", "read_identity_data"],
        "HIGH"
    ),
    Agent(
        "CMP-001",
        "Compliance Monitoring Agent",
        "ComplianceAgent",
        ["read_audit_logs", "generate_reports", "check_controls"],
        "MEDIUM"
    )
]

for agent in agents:
    print(agent)