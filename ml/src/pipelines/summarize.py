from src.managers.chunk_manager import ArxivChunker
from src.managers.mysql_manager import mysql_manager
from src.managers.qdrant_manager import qdrant_manager

class Summarize:
    def __init__(self):
        self.qdrant_manager = qdrant_manager
        self.my_sql_manager = mysql_manager
        self.summarize_chunker = ArxivChunker(
            chunk_size=1000, 
            overlap=0
        )

    def invoke(self, article_id: str):
        is_article_in_db = self.qdrant_manager.find_article_by_id(article_id)
        if not is_article_in_db:
            self.qdrant_manager.add_article(article_id)
        
        text = self.my_sql_manager.find_article_by_id(article_id)
        resume = self.summarize(text)
        
        return resume
    
    def summarize(self, text: str) -> str:
        pass


summarize_pipeline = Summarize()