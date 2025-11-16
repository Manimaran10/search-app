from services.models.embedding_model import EmbeddingModel
from services.indexer.chunker import TextChunker
from services.classifiers.topic_classifier import TopicClassifier
from services.classifiers.project_classifier import ProjectClassifier
from services.classifiers.team_classifier import TeamClassifier
from services.db_handler.mongodb_handler import MongoDBHandler
import logging

logger = logging.getLogger(__name__)

class TextIndexer:
    
    def __init__(self, mongodb_handler: MongoDBHandler = None):
        self.embedding_model = EmbeddingModel()
        self.text_chunker = TextChunker()
        self.db_handler = mongodb_handler or MongoDBHandler()

    def process(self, text: str, filename=None, source= None) -> dict:
        topic_classifier = TopicClassifier()
        project_classifier = ProjectClassifier()
        team_classifier = TeamClassifier()
        project= project_classifier.categorize(text)
        team = team_classifier.categorize(text)
        chunks  = self.text_chunker.chunk(text)
        nodes = []
        for chunk in chunks:
            topic = topic_classifier.categorize(chunk)
            nodes.append({
                "text": chunk,
                "topic": topic,
                "project": project,
                "team": team,
                "source": source,
                "filename": filename
            })
        embeddings = [self.embedding_model.encode(chunk, convert_to_tensor=False).tolist() for chunk in chunks]

        for node,embedding in zip(nodes,embeddings):
            node["embedding"] = embedding

        db_operation_response = self.persist_to_db(nodes)
        print("DB ingestion response:", db_operation_response)
        return db_operation_response

    def persist_to_db(self, nodes: list) -> dict:
        """Persist nodes to MongoDB database."""
        try:
            # Format nodes for database insertion
            documents = []
            for node in nodes:
                # Convert source object to string representation
                source_str = str(node["source"]) if node["source"] else None
                
                document = {
                    "text": node["text"],
                    "topic": node["topic"],
                    "project": node["project"],
                    "team": node["team"],
                    "embedding": node["embedding"],
                    "source": source_str,
                    "title": node.get("title", None),
                }
                documents.append(document)
            
            # Insert documents using MongoDB handler
            inserted_ids = self.db_handler.insert_documents(documents)
            print("Inserted document IDs:", inserted_ids)
            logger.info(f"Successfully persisted {len(inserted_ids)} nodes to database")
            
            return {
                "success": True,
                "inserted_count": len(inserted_ids),
                "inserted_ids": inserted_ids,
                "message": f"Successfully indexed {len(inserted_ids)} document chunks"
            }
            
        except Exception as e:
            logger.error(f"Failed to persist nodes to database: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to index documents"
            }
