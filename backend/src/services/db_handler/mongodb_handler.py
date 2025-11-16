"""
MongoDB Handler for Vector Search and Document Storage
"""
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import numpy as np
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure, DuplicateKeyError
from bson import ObjectId
from .config import mongodb_config

logger = logging.getLogger(__name__)

class MongoDBHandler:
    """MongoDB handler with vector search capabilities."""
    
    def __init__(self, config=None):
        self.config = config or mongodb_config
        self._client = None
        self._database = None
        self._collection = None
        self.connect()
    
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            self._client = MongoClient(
                self.config.connection_string,
                **self.config.get_connection_params()
            )
            # Test connection
            self._client.admin.command('ping')
            
            self._database = self._client[self.config.database_name]
            self._collection = self._database[self.config.collection_name]
            
            # Ensure indexes
            self._ensure_indexes()
            
            logger.info(f"Connected to MongoDB: {self.config.database_name}.{self.config.collection_name}")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    def _ensure_indexes(self):
        """Create necessary indexes for efficient querying."""
        try:
            # Create indexes for filtering
            index_specs = [
                [("topic", ASCENDING)],
                [("project", ASCENDING)],
                [("team", ASCENDING)],
                [("source", ASCENDING)],
                [("created_at", DESCENDING)],
                [("topic", ASCENDING), ("project", ASCENDING)],
                [("team", ASCENDING), ("project", ASCENDING)]
            ]
            
            for spec in index_specs:
                try:
                    self._collection.create_index(spec, background=True)
                except DuplicateKeyError:
                    pass  # Index already exists
            
            # Create text search index for fallback
            try:
                text_index = [("content", "text"), ("title", "text")]
                self._collection.create_index(text_index, background=True)
                logger.info("Text search index created")
            except DuplicateKeyError:
                pass  # Index already exists
            except Exception as e:
                logger.warning(f"Could not create text search index: {e}")
                    
            logger.info("MongoDB indexes ensured")
            
        except Exception as e:
            logger.warning(f"Failed to create some indexes: {e}")
    
    def insert_document(self, document: Dict[str, Any]) -> str:
        """Insert a single document."""
        try:
            # Add metadata
            document['created_at'] = datetime.utcnow()
            document['updated_at'] = datetime.utcnow()
            
            result = self._collection.insert_one(document)
            logger.info(f"Document inserted with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise
    
    def insert_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents."""
        try:
            # Add metadata to all documents
            for doc in documents:
                doc['created_at'] = datetime.utcnow()
                doc['updated_at'] = datetime.utcnow()
            
            result = self._collection.insert_many(documents)
            inserted_ids = [str(id) for id in result.inserted_ids]
            logger.info(f"Inserted {len(inserted_ids)} documents")
            return inserted_ids
            
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")
            raise
    
    def vector_search(
        self, 
        query_vector: Union[List[float], np.ndarray],
        query_text: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        topk: int = 10,
        alpha: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform vector search with optional hybrid search.
        
        Args:
            query_vector: The query embedding vector
            query_text: Optional text for hybrid search
            filters: MongoDB query filters
            topk: Number of results to return
            alpha: Weight for hybrid search (0.0 = pure vector, 1.0 = pure text)
        """
        try:
            # Ensure query_vector is a list
            if isinstance(query_vector, np.ndarray):
                query_vector = query_vector.tolist()
            
            # Limit topk
            topk = min(topk, self.config.max_limit)
            
            # Build aggregation pipeline for vector search
            pipeline = []
            
            # Vector search stage (Atlas Vector Search)
            vector_search_stage = {
                "$vectorSearch": {
                    "index": self.config.vector_index_name,
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": min(topk * 10, 1000),
                    "limit": topk
                }
            }
            
            # Add filters if provided
            if filters:
                vector_search_stage["$vectorSearch"]["filter"] = self._build_filters(filters)
            
            pipeline.append(vector_search_stage)
            
            # Add metadata fields
            pipeline.append({
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"}
                }
            })
            
            # Project fields
            pipeline.append({
                "$project": {
                    "text": 1,
                    "topic": 1,
                    "project": 1,
                    "team": 1,
                    "source": 1,
                    "title": {"$ifNull": ["$title", "Untitled"]},
                    "created_at": 1,
                    "score": 1
                }
            })
            
            # Execute search
            results = list(self._collection.aggregate(pipeline))
            
            # If hybrid search is requested and we have query_text
            if query_text and alpha > 0:
                results = self._hybrid_search(results, query_text, alpha)
            
            logger.info(f"Vector search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            # Fallback to text search if vector search fails
            return self._text_search_fallback(query_text, filters, topk)
    
    def _hybrid_search(self, vector_results: List[Dict], query_text: str, alpha: float) -> List[Dict]:
        """Combine vector search with text search for hybrid results."""
        try:
            # Perform text search
            text_pipeline = [
                {
                    "$search": {
                        "index": "text_index",  # You'll need to create this
                        "text": {
                            "query": query_text,
                            "path": ["text", "title"]
                        }
                    }
                },
                {
                    "$addFields": {
                        "text_score": {"$meta": "searchScore"}
                    }
                },
                {"$limit": max(1, len(vector_results) * 2)}
            ]
            
            text_results = list(self._collection.aggregate(text_pipeline))
            
            # Combine and re-rank results
            combined_results = self._combine_search_results(
                vector_results, text_results, alpha
            )
            
            return combined_results
            
        except Exception as e:
            logger.warning(f"Hybrid search fallback failed: {e}")
            return vector_results
    
    def _text_search_fallback(self, query_text: str, filters: Dict, topk: int) -> List[Dict]:
        """Fallback text search when vector search is not available."""
        try:
            if not query_text:
                return []
                
            # Try text search first
            try:
                search_query = {"$text": {"$search": query_text}}
                
                # Add filters
                if filters:
                    search_query.update(self._build_filters(filters))
                
                # Execute search
                results = list(
                    self._collection.find(
                        search_query,
                        {"content": 1, "topic": 1, "project": 1, "team": 1, "source": 1, "title": 1}
                    )
                    .limit(topk)
                )
                
                if results:
                    logger.info(f"Text search fallback returned {len(results)} results")
                    return results
                    
            except Exception as text_e:
                logger.warning(f"Text search failed: {text_e}")
            
            # If text search fails, try simple regex matching
            try:
                regex_query = {
                    "$or": [
                        {"content": {"$regex": query_text, "$options": "i"}},
                        {"title": {"$regex": query_text, "$options": "i"}}
                    ]
                }
                
                # Add filters
                if filters:
                    regex_query = {"$and": [regex_query, self._build_filters(filters)]}
                
                results = list(
                    self._collection.find(
                        regex_query,
                        {"content": 1, "topic": 1, "project": 1, "team": 1, "source": 1, "title": 1}
                    )
                    .limit(topk)
                )
                
                logger.info(f"Regex search fallback returned {len(results)} results")
                return results
                
            except Exception as regex_e:
                logger.error(f"Regex search failed: {regex_e}")
                return []
            
        except Exception as e:
            logger.error(f"Text search fallback failed: {e}")
            return []
    
    def _build_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build MongoDB query filters."""
        mongo_filters = {}
        
        for key, value in filters.items():
            if key in ['topic', 'project', 'team', 'source']:
                if isinstance(value, list):
                    mongo_filters[key] = {"$in": value}
                else:
                    mongo_filters[key] = value
            elif key == 'date_range':
                if 'start' in value or 'end' in value:
                    date_filter = {}
                    if 'start' in value:
                        date_filter['$gte'] = value['start']
                    if 'end' in value:
                        date_filter['$lte'] = value['end']
                    mongo_filters['created_at'] = date_filter
        
        return mongo_filters
    
    def _combine_search_results(
        self, 
        vector_results: List[Dict], 
        text_results: List[Dict], 
        alpha: float
    ) -> List[Dict]:
        """Combine and re-rank vector and text search results."""
        # Create lookup for text results
        text_scores = {str(doc['_id']): doc.get('text_score', 0) for doc in text_results}
        
        # Normalize scores and combine
        max_vector_score = max([doc.get('score', 0) for doc in vector_results] + [1])
        max_text_score = max(text_scores.values()) if text_scores else 1
        
        combined_results = []
        for doc in vector_results:
            doc_id = str(doc['_id'])
            
            # Normalize scores to [0, 1]
            vector_score = doc.get('score', 0) / max_vector_score
            text_score = text_scores.get(doc_id, 0) / max_text_score
            
            # Combine scores
            combined_score = (1 - alpha) * vector_score + alpha * text_score
            doc['combined_score'] = combined_score
            
            combined_results.append(doc)
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return combined_results
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by its ID."""
        try:
            result = self._collection.find_one({"_id": ObjectId(doc_id)})
            return result
        except Exception as e:
            logger.error(f"Failed to get document {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, updates: Dict[str, Any]) -> bool:
        """Update a document."""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = self._collection.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update document {doc_id}: {e}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document."""
        try:
            result = self._collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            stats = self._database.command("collStats", self.config.collection_name)
            return {
                'document_count': stats.get('count', 0),
                'storage_size': stats.get('storageSize', 0),
                'avg_document_size': stats.get('avgObjSize', 0),
                'indexes': len(stats.get('indexSizes', {}))
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def close_connection(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()