Patel Data Ingestion Pipeline

Production-ready document ingestion platform built on the Patel Platform Service Template (PPST) for transforming unstructured documents into AI-ready knowledge using OpenAI embeddings, PostgreSQL, and pgvector.

Executive Summary

The Patel Data Ingestion Pipeline is a production-ready backend service responsible for transforming raw, unstructured documents into structured, searchable, and AI-ready knowledge.

Built on the Patel Platform Service Template (PPST), the service provides a standardized ingestion framework that automates the complete document processing lifecycle while maintaining consistency, scalability, and extensibility.

The pipeline performs the following operations:

Document upload
Metadata management
Text extraction
Text chunking
OpenAI embedding generation
Vector persistence using PostgreSQL + pgvector
Document lifecycle management

The resulting knowledge can be consumed by Retrieval-Augmented Generation (RAG) systems, semantic search engines, enterprise AI assistants, analytics platforms, and intelligent backend services.

Rather than functioning as a standalone application, the Data Ingestion Pipeline serves as a reusable platform component within the Patel Engineering ecosystem, providing a consistent foundation for downstream AI services.

Problem Statement

Organizations generate enormous amounts of unstructured information through documents, reports, manuals, emails, spreadsheets, PDFs, web pages, and other digital assets.

Although these documents contain valuable business knowledge, they are difficult for software applications and Large Language Models (LLMs) to consume directly.

Without a standardized ingestion process, organizations often experience:

Duplicate and inconsistent information
Manual document processing
Poor search quality
Inconsistent indexing
Difficult onboarding of new document formats
Limited scalability
Minimal observability
Poor document lifecycle management

As AI adoption grows, these challenges become increasingly significant because Retrieval-Augmented Generation (RAG) depends on clean, structured, searchable knowledge.

The Patel Data Ingestion Pipeline addresses these challenges by providing a repeatable, automated, and extensible ingestion workflow that transforms raw documents into structured vectorized knowledge suitable for enterprise AI applications.

Architecture Overview

The pipeline follows Clean Architecture and separates responsibilities into well-defined layers.

                FastAPI API
                     │
                     ▼
            Application Services
                     │
                     ▼
             Domain Layer
                     │
                     ▼
      Repository / Infrastructure
                     │
                     ▼
 PostgreSQL + pgvector + OpenAI

Major architectural principles include:

Clean Architecture
Dependency Injection
Repository Pattern
Service Layer
Event-driven document lifecycle
Global exception handling
Centralized logging
OpenAPI-first development
Technology Stack
Category	Technology
Language	Python 3.13
Framework	FastAPI
ORM	SQLAlchemy
Database	PostgreSQL
Vector Store	pgvector
AI	OpenAI Embeddings
Validation	Pydantic
Documentation	OpenAPI 3.1 / Swagger
Architecture	Clean Architecture
Dependency Injection	PPST Container
Logging	Python Logging
Containerization	Docker
Version Control	Git / GitHub
System Architecture Diagram
                    Client
                      │
                      ▼
               FastAPI REST API
                      │
                      ▼
               Upload Service
                      │
                      ▼
             Document Service
                      │
                      ▼
            Ingestion Service
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
 Text Extraction   Chunking   Embeddings
        │                           │
        └─────────────┬─────────────┘
                      ▼
           PostgreSQL + pgvector
                      │
                      ▼
          AI-ready Searchable Knowledge
Project Structure
app/
│
├── api/
│   └── v1/
│       └── routes/
│
├── application/
│   ├── contracts/
│   ├── document/
│   ├── ingestion/
│   └── extraction/
│
├── bootstrap/
│
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── handlers.py
│   └── logging.py
│
├── domain/
│
├── events/
│
├── infrastructure/
│   ├── db/
│   ├── repositories/
│   ├── vector/
│   └── logging/
│
└── main.py
Features

Current capabilities include:

Document metadata management
Automatic document upload
Temporary file management
Text extraction
Text chunking
OpenAI embedding generation
PostgreSQL vector persistence
pgvector integration
Global exception handling
Structured logging
Repository pattern
Dependency injection
OpenAPI documentation
Health monitoring
Document lifecycle management
API Endpoints
Method	Endpoint	Description
GET	/health	Service health check
POST	/documents	Create document metadata
GET	/documents	Retrieve all documents
GET	/documents/{id}	Retrieve document
DELETE	/documents/{id}	Delete document
POST	/documents/upload	Upload and ingest document
POST	/documents/ingest	Ingest raw text
Document Lifecycle
Document Created
        │
        ▼
UPLOADED
        │
        ▼
Text Extraction
        │
        ▼
Chunking
        │
        ▼
Embedding Generation
        │
        ▼
Vector Persistence
        │
        ▼
COMPLETED

Future asynchronous processing:

UPLOADED
     │
     ▼
QUEUED
     │
     ▼
PROCESSING
     │
     ▼
COMPLETED
Future Roadmap
v0.2
Extractor Factory
TXT support
Markdown support
PDF support
DOCX support
HTML support
CSV support
JSON support
v0.3
Retrieval Service
Semantic Search
Top-K Similarity Search
Query Embeddings
Ranking
v1.0
Azure Blob Storage
Azure Queue Storage
Background Workers
Asynchronous Processing
Azure Container Apps
Azure Monitor
Production Deployment
Getting Started

Clone the repository:

git clone https://github.com/AzurePatel42/patel-data-ingestion-pipeline-ppst.git

cd patel-data-ingestion-pipeline-ppst

Create a virtual environment:

python -m venv .venv

Activate the environment:

Windows

.venv\Scripts\activate

Linux/macOS

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure your environment variables:

OPENAI_API_KEY=your_api_key
DATABASE_URL=postgresql://...
Running Locally

Start PostgreSQL (with pgvector enabled), then launch the application:

uvicorn app.main:app --reload

Open:

http://localhost:8000/docs

Swagger UI provides the interactive OpenAPI documentation.

Testing

Run the test suite:

pytest

Recommended test coverage includes:

Document Service
Upload Service
Ingestion Service
Repository Layer
API Endpoints
Exception Handling
Document Lifecycle
Vector Persistence
License

This project is licensed under the MIT License.

See the LICENSE file for additional information.