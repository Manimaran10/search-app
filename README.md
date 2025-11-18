---
title: AI Knowledge Base
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---

# AI Knowledge Base – Vector Search Application

## Overview

This project is an AI-powered knowledge base and semantic search platform. It enables users to upload documents, extract and index their content using embeddings, and perform advanced vector and hybrid (vector + keyword) searches using MongoDB Atlas Vector Search.

## Features

- **Document Upload:** Supports text, PDF, image, and URL uploads.
- **Text Extraction & Chunking:** Extracts and chunks text for efficient indexing.
- **Embeddings:** Uses Sentence Transformers to generate vector embeddings.
- **MongoDB Atlas Integration:** Stores documents and embeddings; supports vector and hybrid search.
- **Semantic Search API:** Fast, relevant search results using vector similarity and keyword fallback.
- **React Frontend:** Simple UI for search and upload.

## Tech Stack

- **Frontend:** React, fetch API
- **Backend:** Python, Flask, PyMongo, Sentence Transformers
- **Database:** MongoDB Atlas (Vector Search enabled)

## Model Used
- Sentence Transformers - all-MiniLM-L6-v2 // A lightweight model providing 384-dimensional embeddings mainly for balanced performance and speed.

## Setup

1. **Clone the repository**
2. **Backend Setup**
   - `cd backend`
   - Create a `.env` file (see `.env.example`)
   - Install dependencies:  
     `python3 -m venv env && source env/bin/activate && pip install -r requirements.txt`
   - Run MongoDB index setup:  
     `python setup_text_index.py`
   - Start backend:  
     `cd src && python app_controller.py`
3. **Frontend Setup**
   - `cd ../`
   - Install dependencies:  
     `npm install`
   - Start frontend:  
     `npm start`
4. **Access the app:**  
   - Frontend: [http://localhost:3000](http://localhost:3000)  
   - Backend API: [http://localhost:5000](http://localhost:5000)

## API Endpoints

- `POST /api/upload` – Upload a document (file or URL)
- `POST /api/query` – Search documents (vector/hybrid search)

## Example Query

```json
POST /api/query
{
  "q": "project roadmap for Q4",
  "filters": {},
  "hybrid": false // true for combined vector and keyword search
}
```

## Hugging Face Spaces Deployment

This application is configured to run on Hugging Face Spaces with the following setup:

### Required Environment Variables

Set these in your Hugging Face Space settings:

```bash
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=search_app
MONGODB_COLLECTION=documents
VECTOR_INDEX_NAME=vector_index
TEXT_INDEX_NAME=text_index
```

### Space Configuration

- **SDK:** Gradio (for Python backend)
- **Python Version:** 3.9+
- **Hardware:** CPU Basic (sufficient for this application)

### Files Structure for Deployment

```
/
├── app.py (Hugging Face entry point)
├── requirements.txt
├── backend/
│   ├── src/
│   │   ├── app_controller.py
│   │   └── services/
│   └── .env
└── frontend/build/ (React build files)
```

### Deployment Steps

1. Create a new Hugging Face Space
2. Set environment variables in Space settings
3. Push your code to the Space repository
4. The app will automatically deploy and be available at your Space URL

## Local Development

### Setup

1. **Clone the repository**
2. **Backend Setup**
   - `cd backend`
   - Create a `.env` file (see `.env.example`)
   - Install dependencies:  
     `python3 -m venv env && source env/bin/activate && pip install -r requirements.txt`
   - Run MongoDB index setup:  
     `python setup_text_index.py`
   - Start backend:  
     `cd src && python app_controller.py`
3. **Frontend Setup**
   - `cd ../`
   - Install dependencies:  
     `npm install`
   - Start frontend:  
     `npm start`
4. **Access the app:**  
   - Frontend: [http://localhost:3000](http://localhost:3000)  
   - Backend API: [http://localhost:5000](http://localhost:5000)

## Notes

- Requires MongoDB Atlas with Vector Search enabled.
- Handles empty results and errors gracefully.
- Designed for easy extension and production deployment.
