from src.managers.qdrant_manager import QdrantManager

class Analyze:
    def __init__(self):
        self.qdrant_manager = QdrantManager()

    def invoke(self, article_id: str):
        article_in_db = self.qdrant_manager.find_article_by_id(article_id)
        if not article_in_db:
            self.qdrant_manager.add_document(article_id)
        
        return "Finished"


analyze_pipeline = Analyze()