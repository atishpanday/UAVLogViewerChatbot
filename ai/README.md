# AI Module for UAV Log Viewer Chatbot

## Overview

This module is part of the UAV Log Viewer Chatbot project, designed to handle data processing, storage, and analysis for UAV log files. It includes components for fetching, storing, and analyzing log data, as well as integrating with external AI services.

## Directory Structure

- **common/**: Contains common utilities and functions used across the project.
- **uavlogs/**: Handles specific operations related to UAV log data.
- **data/**: Manages data operations, including fetching logs, storing vectors, and uploading reference documents.
- **agent/**: Contains the AI agent logic for processing and responding to queries.
- **chatbot/**: Manages chatbot interactions and message handling.
- **.venv/**: Python virtual environment for managing dependencies.

## Key Files

- **main.py**: Entry point for running the AI module.
- **pyproject.toml**: Configuration file for Python project dependencies.
- **fetch_logs.py**: Script for fetching and processing log data.
- **vector_store.py**: Manages vector storage and retrieval.
- **upload_reference_doc.py**: Handles uploading and processing of reference documents.

## Prerequisites

- Python 3.13
- MongoDB
- FastAPI 0.115.12+
- LangChain 0.3.25+
- LangChain Community 0.3.25+
- LangChain OpenAI 0.3.22+
- LangChain Pinecone 0.2.8+
- Motor 3.7.1+
- Pydantic 2.11.5+
- Python-dotenv 1.1.0+
- Uvicorn 0.34.3+

## Installation

1. **Set Up Python Environment**:
   - Create a virtual environment:
     ```bash
     python3.13 -m venv .venv
     ```
   - Activate the virtual environment:
     ```bash
     source .venv/bin/activate
     ```
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configure Environment Variables**:
   - Set up necessary environment variables in `.env` file:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: OpenAI model to use (e.g. "gpt-4o", should be capable of reasoning well)
     - `MONGODB_URI`: MongoDB connection string
     - `PINECONE_API_KEY`: Your Pinecone API key

3. **Upload Reference Documents**:
   - Run the upload script to create vector embeddings:
     ```bash
     python data/upload_reference_doc.py
     ```
   This will process the reference manual, create vector embeddings, and upload them to Pinecone.

## Usage

1. **Run the Main Script**:
   ```bash
   python main.py
   ```

2. **Data Operations**:
   - Use scripts in the `data/` directory for specific data operations like fetching logs or uploading documents.
