"""
MongoDB Configuration for Vector Search
"""
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MongoDBConfig:
    """MongoDB configuration class."""
    
    # Connection settings
    connection_string: str = os.getenv(
        "MONGODB_CONNECTION_STRING", 
        "mongodb://localhost:27017"
    )
    database_name: str = os.getenv("MONGODB_DATABASE", "search_app")
    collection_name: str = os.getenv("MONGODB_COLLECTION", "documents")
    
    # Vector search settings
    vector_index_name: str = "vector_index"
    text_index_name: str = "text_index"
    embedding_dimension: int = 384  # for all-MiniLM-L6-v2
    max_limit: int = 100  # Maximum number of results to return
    
    # Connection parameters
    max_pool_size: int = 50
    min_pool_size: int = 5
    max_idle_time_ms: int = 30000
    server_selection_timeout_ms: int = 5000
    
    def get_connection_params(self) -> Dict[str, Any]:
        """Get MongoDB connection parameters."""
        return {
            "maxPoolSize": self.max_pool_size,
            "minPoolSize": self.min_pool_size,
            "maxIdleTimeMS": self.max_idle_time_ms,
            "serverSelectionTimeoutMS": self.server_selection_timeout_ms,
        }
    
    def get_vector_search_index_config(self) -> Dict[str, Any]:
        """Get vector search index configuration for MongoDB Atlas."""
        return {
            "name": self.vector_index_name,
            "type": "vectorSearch",
            "definition": {
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": self.embedding_dimension,
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

# Global configuration instance
mongodb_config = MongoDBConfig()