variable "region" { default = "us-east-1" }
variable "ml_bucket_name" { description = "Unique S3 bucket name" }
variable "repo_prefix" { description = "ECR repo prefix, e.g. demo" default = "demo" }
