#`````````
#Variables
#`````````
variable "project_name" {
  type        = string
  default     = "devopslab3"
  description = "Project name. Affects names."
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Region to deploy."
}

#`````````
#ECR
#`````````

resource "aws_ecr_repository" "lambda_ecr" {
  name = "${var.project_name}-lambda"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  

}

resource "aws_ecr_lifecycle_policy" "ecr_policy" {
  repository = aws_ecr_repository.lambda_ecr.name
  policy = <<EOF
  {
    "rules": [
      {
        "rulePriority": 1,
        "description": "Keep only 1 image",
        "selection": {
          "tagStatus": "any",
          "countType": "imageCountMoreThan",
          "countNumber": 1
        },
        "action": {
          "type": "expire"
        }
      }
    ]
  }
  EOF
}

output "ecr_uri" {
  value = aws_ecr_repository.lambda_ecr.repository_url
}

output "ecr_name" {
  value = aws_ecr_repository.lambda_ecr.name
}