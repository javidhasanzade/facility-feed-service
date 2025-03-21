# Facility Feed Service

## Overview

The Facility Feed Service is an asynchronous Python service that:
- Fetches facility data from a PostgreSQL database in memory-efficient chunks.
- Transforms the data into a structured JSON feed format (with up to 100 records per file).
- Generates a metadata file that describes the feed files.
- Compresses the files with gzip and uploads them to an AWS S3 bucket.
- Is containerized with Docker and deployed on AWS ECS Fargate as a scheduled task (using CloudWatch Events/EventBridge).
- Includes a CI/CD pipeline (using GitHub Actions) for linting, testing, building, and deploying the Docker image.

## Setup Instructions

### Prerequisites
- [Python 3.9](https://www.python.org/downloads/)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- An AWS account with permissions to create an S3 bucket, ECS clusters, and IAM roles.
- PostgreSQL (either locally or using Docker Compose).

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/javidhasanzade/facility-feed-service.git
cd facility-feed-service


### Environment Configuration
1. Create a `.env` file in the project root with your environment-specific settings. For example:

   ```dotenv
   DATABASE_URL=postgres://user:password@localhost:5432/mydb
   AWS_REGION=your-aws-region
   S3_BUCKET=your-s3-bucket
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   CHUNK_SIZE=100
   FEED_NAME=reservewithgoogle.entity

2. Ensure that your AWS credentials have the necessary permissions and that your PostgreSQL database is accessible.