#!/usr/bin/env python3
"""
Test script for MongoDB Vector Search functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.db_handler.mongodb_handler import MongoDBHandler
from src.services.models.embedding_model import EmbeddingModel
from src.services.indexer.indexer import TextIndexer
from src.services.searcher.query_service import QueryService

def test_embedding_model():
    """Test the embedding model."""
    print("🧠 Testing Embedding Model...")
    
    try:
        model = EmbeddingModel()
        
        # Test encoding
        texts = ["This is a test document", "Another sample text"]
        embeddings = model.encode(texts)
        
        print(f"✅ Embedding model working. Dimension: {len(embeddings[0])}")
        return True
    except Exception as e:
        print(f"❌ Embedding model failed: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection."""
    print("🗄️  Testing MongoDB Connection...")
    
    try:
        handler = MongoDBHandler()
        stats = handler.get_collection_stats()
        print(f"✅ MongoDB connected. Documents: {stats.get('document_count', 0)}")
        handler.close_connection()
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running and connection string is correct")
        return False

def test_indexing():
    """Test document indexing."""
    print("📚 Testing Document Indexing...")
    
    try:
        indexer = TextIndexer()
        
        # Test with sample text
        sample_text = """
        This is a sample document about artificial intelligence and machine learning.
        It discusses various AI techniques and their applications in business processes.
        The document covers topics like natural language processing and computer vision.
        """
        
        result = indexer.process(sample_text, source="test_document.txt")
        
        if result.get('success'):
            print(f"✅ Indexing successful. Indexed {result.get('inserted_count', 0)} chunks")
            return True
        else:
            print(f"❌ Indexing failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Indexing failed: {e}")
        return False

def test_search():
    """Test vector search functionality."""
    print("🔍 Testing Vector Search...")
    
    try:
        query_service = QueryService()
        
        # Test search
        results = query_service.query("artificial intelligence", topk=3)
        
        print(f"✅ Search successful. Found {len(results)} results")
        
        if results:
            print("   Sample result:")
            sample = results[0]
            print(f"   - Content: {sample.get('content', '')[:100]}...")
            print(f"   - Topic: {sample.get('categories', {}).get('topic', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔬 MongoDB Vector Search Integration Tests")
    print("=" * 50)
    
    tests = [
        test_embedding_model,
        test_mongodb_connection,
        test_indexing,
        test_search
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB Vector Search is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check configuration and dependencies.")
        print("   Run ./setup.sh to install dependencies and configure MongoDB.")

if __name__ == "__main__":
    main()
