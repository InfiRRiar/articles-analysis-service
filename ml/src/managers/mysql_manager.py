from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Text

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
        pass

mysql_manager = MySQLManager()