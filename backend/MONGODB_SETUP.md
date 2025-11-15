# MongoDB Vector Search Setup Guide

This guide will help you set up MongoDB with vector search capabilities for the AI Knowledge Base application.

## Option 1: MongoDB Atlas (Recommended)

MongoDB Atlas is the cloud-based MongoDB service that includes built-in vector search capabilities.

### 1. Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Sign up for a free account
3. Create a new project

### 2. Create a Cluster

1. Click "Create Cluster"
2. Choose "M0 Sandbox" (free tier)
3. Select a cloud provider and region
4. Click "Create Cluster"

### 3. Configure Network Access

1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Select "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### 4. Create Database User

1. Go to "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create username and password
5. Set role to "Atlas admin" (for development)
6. Click "Add User"

### 5. Get Connection String

1. Go to "Database" → "Connect"
2. Choose "Connect your application"
3. Copy the connection string
4. Replace `<password>` with your user password

### 6. Configure Application

Update your `.env` file:

```env
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
MONGODB_DATABASE=search_app
MONGODB_COLLECTION=documents
```

### 7. Create Vector Search Index

**Important:** Vector search in MongoDB Atlas requires a search index. 

1. Go to your cluster → "Search" tab
2. Click "Create Search Index"
3. Choose "JSON Editor"
4. Use this configuration:

```json
{
  "name": "vector_index",
  "type": "vectorSearch",
  "definition": {
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 384,
        "similarity": "cosine"
      },
      {
        "type": "filter",
        "path": "topic"
      },
      {
        "type": "filter", 
        "path": "team"
      },
      {
        "type": "filter",
        "path": "project"
      }
    ]
  }
}
```

5. Click "Create Search Index"

## Option 2: Local MongoDB (Development Only)

### 1. Install MongoDB Community Edition

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
```

**Start MongoDB:**
```bash
brew services start mongodb/brew/mongodb-community
```

### 2. Configure Application

Update your `.env` file:
```env
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE=search_app
MONGODB_COLLECTION=documents
```

**Note:** Local MongoDB doesn't support vector search. The application will fall back to text search.

## Installation and Testing

### 1. Install Dependencies

```bash
cd backend
./setup.sh
```

### 2. Test the Setup

```bash
python test_mongodb.py
```

### 3. Start the Application

```bash
source env/bin/activate
python src/controllers/app_controller.py
```

## Document Schema

Documents stored in MongoDB have this structure:

```json
{
  "_id": ObjectId("..."),
  "text": "Document content chunk",
  "embedding": [0.1, -0.2, 0.3, ...],  // 384-dimensional vector
  "topic": "automation",
  "project": "Hey Amigo", 
  "team": "Marketing",
  "source": "document.pdf",
  "title": "Document Title",
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

## API Usage

### Search Documents
```bash
curl "http://localhost:5000/api/search?q=artificial intelligence&topk=5&hybrid=true"
```

### Search with Filters
```bash
curl "http://localhost:5000/api/search?q=automation&topic=marketing&team=SEO"
```

### Upload and Index Files
```bash
curl -X POST -F "files=@document.pdf" http://localhost:5000/api/upload
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check network access settings in MongoDB Atlas
   - Verify connection string format

2. **Authentication Failed** 
   - Verify username/password in connection string
   - Check database user permissions

3. **Vector Search Not Working**
   - Ensure vector search index is created in Atlas
   - Index creation can take a few minutes

4. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Activate virtual environment: `source env/bin/activate`

### Getting Help

- MongoDB Atlas Documentation: https://docs.atlas.mongodb.com/
- Vector Search Guide: https://docs.atlas.mongodb.com/atlas-search/vector-search/
- Application Logs: Check console output for detailed error messages

## Performance Tips

1. **Index Optimization**
   - Create appropriate indexes for frequently filtered fields
   - Monitor index usage in Atlas

2. **Chunking Strategy**
   - Adjust chunk size based on your documents
   - Balance between context preservation and search granularity

3. **Embedding Model**
   - Use appropriate model for your domain
   - Consider fine-tuning for better performance
