terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "ml_artifacts" {
  bucket = var.ml_bucket_name
}

resource "aws_ecr_repository" "gateway" { name = "${var.repo_prefix}/gateway" }
resource "aws_ecr_repository" "ml"      { name = "${var.repo_prefix}/ml-service" }
resource "aws_ecr_repository" "orders"  { name = "${var.repo_prefix}/orders-service" }
