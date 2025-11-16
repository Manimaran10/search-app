
from services.models.embedding_model import EmbeddingModel

class TeamClassifier:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.TEAM_KEYWORDS = {
            "Marketing": ["marketing", "campaign", "roas", "ctr", "ad", "ads", "performance marketing"],
            "Design": ["design", "logo", "visual", "ux", "ui", "illustration"],
            "Product": ["product", "roadmap", "feature", "specification", "spec", "release"],
            "Sales": ["sales", "pitch", "deal", "quota", "pipeline"],
            "Content": ["content", "copy", "blog", "script", "storyboard"],
            "SEO": ["seo", "keyword", "backlink", "organic", "search"]
        }
        

    def categorize(self, text: str) -> dict:
        text_l = text.lower()
        scores = {}
        for team, keys in self.TEAM_KEYWORDS.items():
            s = sum(1 for k in keys if k in text_l)
            if s > 0:
                scores[team] = s
        if scores:
            # choose team with highest rule hits
            best_team = max(scores.items(), key=lambda x: x[1])[0]
            # return {"team": best_team, "method": "rules", "score": float(scores[best_team])}
            return best_team
        # fallback: semantic similarity between team descriptions and doc
        team_descriptions = {team: " ".join(keys) for team, keys in self.TEAM_KEYWORDS.items()}
        doc_emb = self.embedding_model.encode(text, convert_to_tensor=True)
        best = None
        best_score = -1.0
        for team, desc in team_descriptions.items():
            emb = self.embedding_model.encode(desc, convert_to_tensor=True)
            sim = self.embedding_model.compute_similarity(doc_emb, emb).item()
            if sim > best_score:
                best_score = sim
                best = team
        # return {"team": best, "method": "semantic_fallback", "score": float(best_score)}
        return best