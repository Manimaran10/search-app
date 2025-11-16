
from services.models.embedding_model import EmbeddingModel


def get_all_project_embeddings():
    # Placeholder function to retrieve all project embeddings
    # In a real implementation, this would fetch data from a database or other storage
    SAMPLE_PROJECTS = [
    {
        "project_id": "P001",
        "name": "Q4 Promo Campaign",
        "description": "End of year promotional campaign involving email outreach, paid ads, and social media creatives."
    },
    {
        "project_id": "P002",
        "name": "Mobile App Launch",
        "description": "Launch of the new mobile application including product updates, feature walkthroughs, and launch assets."
    },
    {
        "project_id": "P003",
        "name": "Brand Redesign Initiative",
        "description": "Company-wide redesign of brand guidelines including typography changes, new logo, and refreshed color palette."
    },
    {
        "project_id": "P004",
        "name": "Competitor Benchmark Study",
        "description": "Analysis of competitor pricing, positioning, and campaign messaging to support product strategy."
    },
    {
        "project_id": "P005",
        "name": "Summer Discount Drive",
        "description": "Seasonal summer sale with discounts, landing page refresh, banners, and promotional emails."
    }
    ]
    return SAMPLE_PROJECTS



class ProjectClassifier:

    def __init__(self):
        self.embedding_model = EmbeddingModel()

    def categorize(self, text: str) -> dict:
        projects = get_all_project_embeddings()
        if not projects:
            return {"project": "General", "score": 0.0}
        doc_emb = self.embedding_model.encode(text, convert_to_tensor=True)
        best = None
        best_score = -1.0
        for p in projects:
            if not p.get("embedding"):
                continue
            p_emb = p["embedding"]
            # convert to tensor via numpy
            sim = self.embedding_model.compute_similarity(doc_emb, self.embedding_model.encode(p["description"], convert_to_tensor=True)).item() \
                if p_emb is None else self.embedding_model.compute_similarity(doc_emb, p_emb).item()
            # note: we stored embedding json but recomputing from description keeps it consistent; or you can decode p_emb to tensor
            # Keep this straightforward: use project description similarity
            if sim > best_score:
                best_score = sim
                best = p["name"]
        return best or "General"