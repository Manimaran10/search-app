from services.models.embedding_model import EmbeddingModel
from services.indexer.chunker import TextChunker
from services.classifiers.topic_classifier import TopicClassifier
from services.classifiers.project_classifier import ProjectClassifier
from services.classifiers.team_classifier import TeamClassifier

class TextIndexer:
    
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.text_chunker = TextChunker()

    def process(self, text: str,source= None) -> dict:
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
                "source": source
            })
        embeddings = [self.embedding_model.encode(chunk, convert_to_tensor=False).tolist() for chunk in chunks]

        for node,embedding in zip(nodes,embeddings):
            node["embedding"] = embedding

        db_operation_response = self.persist_to_db(nodes)
        return db_operation_response

    def persist_to_db(self, nodes: list):
        for node in nodes:
            # Here you would implement the logic to persist each node to your database
            # For example:
            db.insert("index", {
                "text": node["text"],
                "topic": node["topic"],
                "project": node["project"],
                "team": node["team"],
                "embedding": node["embedding"],
                "source": node["source"]
            })
