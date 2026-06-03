output "cloud_agent_role_name" {
  value = aws_iam_role.agentvault_cloud_agent_role.name
}

output "cloud_agent_role_arn" {
  value = aws_iam_role.agentvault_cloud_agent_role.arn
}