# 21BEC1554_ML

# Document Retrieval System for Chat Applications

This project is a backend document retrieval system designed for chat applications to use as context during inference with Large Language Models (LLMs). The system retrieves relevant documents from a database based on user queries, caches frequently accessed results for faster retrieval, and enforces rate-limiting to control the number of API requests.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Caching](#caching)
9. [Rate Limiting](#rate-limiting)
10. [Background Scraping Task](#background-scraping-task)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Contributing](#contributing)
14. [License](#license)

## Project Overview

The document retrieval system is designed to provide relevant documents based on user queries. It is built using FastAPI, PostgreSQL, Redis, and Docker. The system supports:
- Efficient document retrieval using similarity-based search.
- Rate limiting to control API usage.
- Caching for faster retrieval.
- A background task for scraping new documents.

## Features

- **Document Storage and Retrieval**: Stores documents in a PostgreSQL database and retrieves them using similarity-based search.
- **Caching**: Uses Redis for caching frequently accessed documents to improve retrieval speed.
- **Rate Limiting**: Enforces rate limits to prevent abuse of API resources.
- **Background Web Scraping**: Periodically scrapes new documents from the web to keep the document database up to date.
- **API Endpoints**: Provides RESTful API endpoints for searching documents, checking API health, and managing user requests.
- **Dockerized Application**: The entire application and its dependencies are containerized using Docker and Docker Compose for easy deployment.

## Architecture

The project consists of the following components:

1. **FastAPI Application (`main.py`)**: Handles API requests and responses, and includes middleware for logging and rate limiting.
2. **Database Models (`models.py`)**: Defines SQLAlchemy models for the PostgreSQL database to store documents and user data.
3. **Text Encoder (`encoder.py`)**: Encodes documents and queries into vectors for similarity-based retrieval.
4. **Web Scraper (`scraper.py`)**: Scrapes web articles and stores them in the database.
5. **Caching System (`cache.py`)**: Uses Redis to cache documents and search results for faster access.
6. **Search Logic (`search.py`)**: Contains the logic for searching documents based on user queries.
7. **Rate Limiting (`rate_limit.py`)**: Implements rate-limiting functionality to control user access.
8. **Logging (`logger.py`)**: Provides logging for API requests and errors.
9. **Database Setup (`create_tables.py`)**: Initializes the database schema by creating tables.
10. **Docker and Docker Compose**: Dockerizes the application and manages multi-container setups.

## Installation

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- Redis
- PostgreSQL


### Clone the Repository

```bash
git clone https://github.com/s3hwag/document_retrieval_system.git
cd document_retrieval_system
```

## Set Up Python Virtual Environment

### Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
## Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Set Up Docker
### Build the Docker image:
```bash
docker build -t fastapi-app
```
### Start the services using Docker Compose:
```bash
docker-compose up --build
```
## Environment Variables
### Create a .env file in the root directory and add the following environment variables:

```env
DATABASE_URL=postgresql://yourusername:yourpassword@db:5432/document_retrieval
REDIS_URL=redis://redis:6379
SCRAPER_INTERVAL=3600  # Run scraper every hour
```
## Running the Application
### To run the application locally:

### Start the Docker containers:
```bash
docker-compose up --build
```
### The FastAPI application will be available at http://localhost:8000.

### To stop the containers, press Ctrl+C and run:
```bash
docker-compose down
```
## API Endpoints
### 1. Health Check
Endpoint: /health
Method: GET
Description: Checks if the API is active.
Response:
json
Copy code
{"status": "API is active"}
2. Search Documents
Endpoint: /search
Method: GET
Parameters:
query (str): The search query.
top_k (int): Number of top results to return. (Default: 5)
threshold (float): Similarity score threshold. (Default: 0.5)
user_id (str): User identifier.
Description: Searches for documents based on the provided query and returns the top results.
Response:
json
Copy code
{"results": [...]}
3. Retrieve User Details
Endpoint: /users/{user_id}
Method: GET
Parameters: user_id (str) - The ID of the user to retrieve.
Description: Retrieves user details from the database based on user_id.
Caching
Backend: Redis
Purpose: Caches frequently accessed documents to speed up retrieval.
Invalidation Strategy: Implement a Least Recently Used (LRU) policy for cache invalidation to manage the cache size and ensure data consistency.
Rate Limiting
Strategy: Limits each user to a maximum of 5 requests. Exceeding the limit returns an HTTP 429 status code.
Implementation: Rate limiting is managed through the rate_limit.py script using database tracking.
Background Scraping Task
Scraper: Defined in scraper.py.
Function: Scrapes new articles periodically (every hour by default) and stores them in the database.
Trigger: Runs in a separate thread when the server starts.
Testing
Unit Tests: Test individual components, such as encoders, search functions, and database models.
Integration Tests: Test interactions between components like API endpoints, database connections, and caching.
Performance Tests: Ensure the application can handle a high volume of requests.
To run tests:
bash
Copy code
pytest tests/
Deployment
Docker Deployment: The application is containerized for easy deployment across different environments.
CI/CD Integration: Use GitHub Actions, GitLab CI, or Jenkins for continuous integration and deployment.
Cloud Platforms: Deploy on cloud platforms like AWS (ECS, EKS), Azure (AKS), or Google Cloud (GKE).


