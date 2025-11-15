#!/usr/bin/env python3
"""
Quick test of QueryService to identify issues
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_query_service():
    try:
        print("🔍 Testing QueryService...")
        
        from src.services.searcher.query_service import QueryService
        print("✅ QueryService imported successfully")
        
        query_service = QueryService()
        print("✅ QueryService initialized successfully")
        
        # Test a simple query
        results = query_service.query("test search", query_filters={}, do_hybrid_search=False)
        print(f"✅ Query executed successfully. Results: {len(results) if results else 0} items")
        
        return True
        
    except Exception as e:
        print(f"❌ QueryService test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_query_service()
