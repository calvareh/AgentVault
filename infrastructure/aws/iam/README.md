# AgentVault AWS IAM Integration

This Terraform module creates AWS IAM roles that represent AgentVault-managed autonomous AI agents.

## Purpose

The goal is to demonstrate how AgentVault can map non-human agent identities to real AWS IAM roles using least-privilege cloud security controls.

## Current Scope

- Create IAM role for CloudAgent
- Tag IAM resources for governance
- Export IAM role name and ARN for future AgentVault dashboard integration

## Cost Note

IAM roles do not incur AWS charges.