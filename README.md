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

## Notes

- Requires MongoDB Atlas with Vector Search enabled.
- Handles empty results and errors gracefully.
- Designed for easy extension and production deployment.
