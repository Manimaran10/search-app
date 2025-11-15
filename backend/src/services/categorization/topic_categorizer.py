from services.models.embedding_model import EmbeddingModel

class TopicCategorizer:
    
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.TOPIC_DESCRIPTIONS = {
            "pricing": "Documents related to pricing, discounts, offers, cost changes, rate card",
            "product_release": "Documents about product launches, product updates, release notes",
            "campaign": "Marketing campaign plans, creatives, ad copies, promotions",
            "brand_guidelines": "Brand guidelines, logos, visual identity, style guide",
            "sales_enablement": "Sales decks, battle cards, pitch, enablement content",
            "internal_documents": "Internal memos, policies, processes, HR documents"
        }

    def categorize(self, text):
        if not text or not text.strip():
            return {"topic": "uncategorized", "score": 0.0}
        doc_emb = self.embedding_model.encode(text, convert_to_tensor=True)
        best = None
        best_score = -1.0
        for topic, desc in self.TOPIC_DESCRIPTIONS.items():
            cat_emb = self.embedding_model.encode(desc, convert_to_tensor=True)
            sim = self.embedding_model.compute_similarity(doc_emb, cat_emb).item()
            if sim > best_score:
                best_score = sim
                best = topic
        # return {"topic": best, "score": float(best_score)}
        return best or "uncategorized"