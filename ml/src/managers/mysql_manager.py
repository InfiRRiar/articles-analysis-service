from sqlalchemy import create_engine, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Text
from sqlalchemy import insert, select, update
from langchain_core.documents import Document
import json

DATABASE_URL="mysql+pymysql://admin:12345@mysql:3306/QNA_DB"

class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "processed_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(Text)

    summarization: Mapped[str] = mapped_column(Text, default="")

    onthology: Mapped[dict] = mapped_column(JSON, default={})
    terms: Mapped[dict] = mapped_column(JSON, default={})


class MySQLManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)

    def find_article_by_id(self, article_id: str) -> Article:
        with self.engine.connect() as conn:
            article = conn.execute(
                select(Article).where(Article.article_id == article_id)
            ).first()
            if not article:
                return None
        return article
    
    def add_summarization_to_article(self, article_id: str, sum: str):
        with self.engine.connect() as conn:
            conn.execute(
                update(Article).where(
                    Article.article_id == article_id
                ).values(summarization=sum)
            )
            conn.commit()

    def add_onthology_to_article(self, article_id: str, onthology: list[dict]):
        onthology = json.dumps({"onthology": onthology})
        with self.engine.connect() as conn:
            conn.execute(
                update(Article).where(
                    Article.article_id == article_id
                ).values(onthology=onthology)
            )
            conn.commit()

    def add_terms_to_article(self, article_id: str, terms: dict):
        with self.engine.connect() as conn:
            conn.execute(
                update(Article).where(
                    Article.article_id == article_id
                ).values(terms=terms)
            )
            conn.commit()


    def add_articles(self, articles: list[Document]):
        with self.engine.connect() as conn:
            for article in articles:
                conn.execute(
                    insert(Article),
                    [
                        {"article_id": article.metadata["article_id"], "text": article.page_content}
                    ]
                )
            conn.commit()

mysql_manager = MySQLManager()