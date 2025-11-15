#!/bin/bash

# Setup script for MongoDB Vector Search backend

echo "🔧 Setting up AI Knowledge Base Backend with MongoDB Vector Search"
echo "=================================================================="

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv env
fi

echo "🔄 Activating virtual environment..."
source env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "ℹ️  Please edit .env file with your MongoDB connection details"
fi

# Create uploads directory
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir -p uploads
fi

# Check if MongoDB is running (local installation)
echo "🔍 Checking MongoDB status..."
if command -v mongod &> /dev/null; then
    if pgrep mongod > /dev/null; then
        echo "✅ MongoDB is running"
    else
        echo "⚠️  MongoDB is installed but not running"
        echo "   To start MongoDB: brew services start mongodb/brew/mongodb-community"
    fi
else
    echo "⚠️  MongoDB not found locally"
    echo "   Install with: brew install mongodb/brew/mongodb-community"
    echo "   Or use MongoDB Atlas (cloud): https://www.mongodb.com/atlas"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure MongoDB connection in .env file"
echo "2. Start the application: python src/controllers/app_controller.py"
echo ""
echo "For MongoDB Atlas (recommended):"
echo "1. Create account at https://www.mongodb.com/atlas"
echo "2. Create a cluster and get connection string"
echo "3. Update MONGODB_CONNECTION_STRING in .env"
echo "4. Create vector search index (see documentation)"
echo ""
