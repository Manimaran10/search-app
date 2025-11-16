from services.models.embedding_model import EmbeddingModel
from services.db_handler.mongodb_handler import MongoDBHandler
import logging

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self, mongodb_handler: MongoDBHandler = None):
        self.embedding_model = EmbeddingModel()
        self.db_handler = mongodb_handler or MongoDBHandler()

    def query(self, query_text: str, query_filters: dict = None, do_hybrid_search: bool = True, topk: int = 5) -> list:
        """
        Query documents using vector search with optional hybrid search.
        
        Args:
            query_text: The search query text
            query_filters: Optional filters for search
            do_hybrid_search: Whether to combine vector and text search
            topk: Number of results to return
            
        Returns:
            List of search results formatted for the frontend
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query_text, convert_to_tensor=False)
            
            # Perform search using the MongoDB handler
            if do_hybrid_search:
                results = self.db_handler.vector_search(
                    query_vector=query_embedding,
                    query_text=query_text,
                    filters=query_filters,
                    topk=topk,
                    alpha=0.5
                )
            else:
                results = self.db_handler.vector_search(
                    query_vector=query_embedding,
                    filters=query_filters,
                    topk=topk
                )
            
            # Format results for frontend
            formatted_results = self._format_results(results)
            
            logger.info(f"Query '{query_text}' returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

    def _format_results(self, results: list) -> list:
        """Format database results for frontend consumption."""
        formatted = []
        
        for i, res in enumerate(results, 1):
            formatted_result = {
                "id": i,
                "content": res.get('text', ''),
                "categories": {
                    "topic": res.get("topic"),
                    "team": res.get("team"), 
                    "project": res.get("project"),
                    "citation": res.get("source", "")
                },
                "title": res.get("title", "Untitled"),
                "source": res.get("source", ""),
                "score": res.get("score", 0),
                "created_at": res.get("created_at")
            }
            formatted.append(formatted_result)
        
        return formatted