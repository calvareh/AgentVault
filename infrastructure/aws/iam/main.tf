terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "agentvault_cloud_agent_role" {
  name = "agentvault-cloud-agent-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project     = "AgentVault"
    AgentName   = "CloudAgent"
    ManagedBy   = "Terraform"
    Environment = "PortfolioLab"
  }
}

resource "aws_iam_policy" "cloud_agent_read_only_policy" {
  name        = "agentvault-cloud-agent-read-only-policy"
  description = "Least-privilege read-only permissions for the AgentVault CloudAgent."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudInventoryReadOnly"
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeVpcs",
          "ec2:DescribeSubnets",
          "iam:GetRole",
          "iam:ListAttachedRolePolicies"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Project     = "AgentVault"
    AgentName   = "CloudAgent"
    ManagedBy   = "Terraform"
    Environment = "PortfolioLab"
    Control     = "LeastPrivilege"
  }
}

resource "aws_iam_role_policy_attachment" "cloud_agent_read_only_attachment" {
  role       = aws_iam_role.agentvault_cloud_agent_role.name
  policy_arn = aws_iam_policy.cloud_agent_read_only_policy.arn
}