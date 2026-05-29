# Chat with Documents Agent

## Overview

This project is a Retrieval-Augmented Generation (RAG) system built using LangGraph, ChromaDB, and Mistral AI. The application can answer questions from a custom knowledge base and perform mathematical calculations using a calculator tool. The calculator is also exposed through an MCP server.

## Features

* Document ingestion and chunking
* Vector embeddings using Mistral Embeddings
* ChromaDB vector storage
* Similarity-based document retrieval
* LangGraph workflow orchestration
* Conditional routing between RAG and calculator paths
* Source citations with filename and chunk index
* Calculator tool
* MCP server exposing the calculator tool

## Project Structure

```text
.
├── data
├── src
│   ├── graphs
│   ├── ingestion
│   ├── rag
│   └── tools
├── vectorstore
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_api_key_here
```

## Running the Project

### Step 1: Create the Vector Database

```bash
python -m src.ingestion.ingest
```

### Step 2: Start the Chat Application

```bash
python -m src.main
```

### Step 3: Start the MCP Server

```bash
python -m src.tools.mcp_server
```

## Example Queries

### RAG Queries

```text
What is LangGraph?
What is Machine Learning?
What is Python?
```

### Calculator Queries

```text
25*40
100/4
10+20
50-15
```

## Workflow

```text
START
  ↓
Router
 ├── RAG Path
 │     ↓
 │  Retrieve
 │     ↓
 │  Answer
 │
 └── Calculator Path
       ↓
   Calculator
       ↓
      END
```

## Source Attribution

Answers generated from retrieved documents include source citations in the following format:

```text
Sources:
- langgraph_basics.txt | chunk 0
- langgraph_basics.txt | chunk 2
```

## Technologies Used

* Python
* LangGraph
* LangChain
* ChromaDB
* Mistral AI
* MCP (Model Context Protocol)

## Author

Tanishq Khandelwal
