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

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "agentvault_cloudtrail_logs" {
  bucket = "agentvault-cloudtrail-logs-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = "AgentVault"
    Purpose     = "CloudTrailAuditLogs"
    ManagedBy   = "Terraform"
    Environment = "PortfolioLab"
  }
}

resource "aws_s3_bucket_public_access_block" "agentvault_cloudtrail_logs_block" {
  bucket = aws_s3_bucket.agentvault_cloudtrail_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "agentvault_cloudtrail_logs_policy" {
  bucket = aws_s3_bucket.agentvault_cloudtrail_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.agentvault_cloudtrail_logs.arn
      },
      {
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.agentvault_cloudtrail_logs.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

resource "aws_cloudtrail" "agentvault_trail" {
  name                          = "agentvault-identity-audit-trail"
  s3_bucket_name                = aws_s3_bucket.agentvault_cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = false
  enable_logging                = true

  depends_on = [
    aws_s3_bucket_policy.agentvault_cloudtrail_logs_policy
  ]

  tags = {
    Project     = "AgentVault"
    Purpose     = "AgentIdentityAudit"
    ManagedBy   = "Terraform"
    Environment = "PortfolioLab"
  }
}