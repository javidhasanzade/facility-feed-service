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
```

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

3. Automatically Create & Populate the Database
An SQL file (init_db.sql) is included to create the facility table and populate it with 100 sample rows.

You don't need to do anything manually — the SQL file is mounted into the database container and will run automatically on first startup.

Make sure this volume is included in docker-compose.yml:
```bash
volumes:
  - ./init_db.sql:/docker-entrypoint-initdb.d/init_db.sql

```

4. 🚀 How to Run the Service Locally
✅ Run with Docker Compose
```bash
docker-compose up --build
```
This will:

Start a local PostgreSQL database container (db)
Wait until the DB is ready
Start the Python application
Fetch data from the DB
Transform it using the selected strategy
Generate gzip-compressed JSON feed and metadata files
Upload them to AWS S3
Log progress and errors to the console in structured JSON format

5. 🧠 Explanation of the Approach
🧱 Architecture
src/config.py: Central config using pydantic-settings
src/database.py: Async chunked data fetching via asyncpg
src/feeds/: Strategy Pattern for supporting multiple feed types
src/file_manager.py: Writes gzip-compressed .json feed files + metadata
src/s3_uploader.py: Async S3 upload with aioboto3
src/logger.py: Structured JSON logging
src/main.py: Main orchestrator

🧩 Feed Type Strategy Pattern
feeds/base.py: Abstract FeedTransformer interface
feeds/reserve_with_google.py: Feed transformer implementation
feeds/factory.py: Factory to return the correct transformer based on FEED_NAME
➡️ Easily extend the service to support other feed formats by creating a new transformer and adding it to the factory.

* Alternatively I could use Dependency injection

6. 🧪 Testing
Unit tests cover:
Config
Transformation logic
File generation
S3 upload logic
Uses pytest, pytest-asyncio, and mocking via monkeypatch
Run tests with:
```bash
docker-compose run --rm app pytest
```

7. 🔁 CI/CD Pipeline (GitHub Actions)
```bash
.github/workflows/ci-cd.yml
```
✅ What It Does:
Install Dependencies
Sets up Python environment and installs project + test dependencies.

Linting & Static Checks
Uses flake8 to ensure your code follows clean Python style and conventions.

Run Unit Tests
Executes all tests with pytest and reports failures immediately.

Build Docker Image
Builds the Docker image for the application using the Dockerfile in the root directory.

Push to AWS ECR
The pipeline will push the image to your AWS Elastic Container Registry (ECR), making it ready for deployment on ECS Fargate.

🔐 Secrets Required (set in GitHub repo settings):
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REPOSITORY

🚀 Deployment
Once the image is pushed to AWS ECR, it can be:

Triggered manually
Pulled automatically by an ECS Fargate scheduled task configured in your infrastructure
Logged via AWS CloudWatch for observability

✅ To Trigger CI/CD:
Every time you push to main, the GitHub Actions workflow will:
```bash
# Behind the scenes
flake8 .
pytest
docker build .
docker push <your-ecr-repo>
```