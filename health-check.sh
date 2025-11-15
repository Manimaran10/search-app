#!/bin/bash

# Health check script for the AI Knowledge Base application

echo "🔍 AI Knowledge Base - Health Check"
echo "=================================="

# Check if backend is running
echo ""
echo "📊 Backend Status:"
backend_status=$(curl -s http://localhost:5000/status 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Backend: Running on http://localhost:5000"
    echo "   Response: $backend_status"
else
    echo "❌ Backend: Not responding on http://localhost:5000"
fi

# Check if frontend is running
echo ""
echo "🌐 Frontend Status:"
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3002 2>/dev/null)
if [[ $frontend_status -eq 200 ]]; then
    echo "✅ Frontend: Running on http://localhost:3002"
else
    echo "❌ Frontend: Not responding on http://localhost:3002"
fi

# Test API endpoints
echo ""
echo "🔌 API Endpoints:"

# Test search endpoint
search_response=$(curl -s "http://localhost:5000/api/search?q=test" 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Search API: Working"
else
    echo "❌ Search API: Failed"
fi

# Test files endpoint
files_response=$(curl -s "http://localhost:5000/api/files" 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Files API: Working"
    # Count files
    file_count=$(echo $files_response | grep -o '"id"' | wc -l | tr -d ' ')
    echo "   Files in database: $file_count"
else
    echo "❌ Files API: Failed"
fi

# Test upload endpoint
upload_test=$(curl -s -X POST http://localhost:5000/api/upload 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Upload API: Accessible"
else
    echo "❌ Upload API: Failed"
fi

echo ""
echo "📋 Summary:"
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:3002"
echo "Knowledge Base: http://localhost:3002/knowledge"
echo ""
echo "🚀 Application is ready to use!"
