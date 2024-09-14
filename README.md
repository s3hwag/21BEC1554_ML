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


