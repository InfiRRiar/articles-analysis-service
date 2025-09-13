from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Text
from sqlalchemy import insert, select
from langchain_core.documents import Document

DATABASE_URL="mysql+pymysql://admin:12345@mysql:3306/QNA_DB"

class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "processed_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(Text)


class MySQLManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)

    def find_article_by_id(self, article_id: str) -> str:
        with self.engine.connect() as conn:
            article = conn.execute(
                select(Article).where(Article.article_id == article_id)
            ).first()
            if not article:
                return None
            article_text = article.text
        return article_text

    def add_article(self, article: Document):
        with self.engine.connect() as conn:
            conn.execute(
                insert(Article),
                [
                    {"article_id": article.metadata["article_id"], "text": article.page_content}
                ]
            )
            conn.commit()

mysql_manager = MySQLManager()