from sentence_transformers import SentenceTransformer , util


class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, convert_to_tensor=False):
        return self.model.encode(texts, convert_to_tensor=convert_to_tensor)
    
    def compute_similarity(self, emb1, emb2):
        return util.cos_sim(emb1, emb2)