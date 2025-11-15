from services.models.embedding_model import EmbeddingModel

class QueryService:
    def __init__(self):
        self.embedding_model = EmbeddingModel()

    def query(self, query_text: str, query_filters: dict = None, do_hybrid_search: bool = True) -> list:
        query_embedding = self.embedding_model.encode(query_text, convert_to_tensor=True)
        # Perform search using the query_embedding
        results  = None
        if do_hybrid_search:
            results = self.db.hybrid_search(query_text,query_embedding,filters=query_filters,topk=5,alpha=0.5)
        else:
            results = self.db.vector_search(query_embedding,filters=query_filters,topk=5)

        def result_to_nodes(results):
            return [
                    {
                    "content": res['text'],
                    "categories": {
                      "topic": res.get("topic",None),
                      "team": res.get("team",None),
                      "project": res.get("project",None),
                    },
                    "title": res["title"],
                    "source": res["source"]
                  }   for res in results 
            ]
        return result_to_nodes(results)