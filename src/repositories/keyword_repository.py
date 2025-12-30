from .base_repository import BaseRepository
from models.db import Keyword

class KeywordRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__(session)
    
    def commit(self) -> None:
        self.session.commit()

    def get_or_create_keywords(self, words: list[str]) -> list[Keyword]:
        keywords = []
        for word in words:
            keyword = self.session.query(Keyword).filter_by(word=word).first()
            if not keyword:
                keyword = Keyword(word=word)
                self.session.add(keyword)
                self.session.flush()
            keywords.append(keyword)
        return keywords
    
    def get_all_keywords(self) -> list[Keyword]:
        return self.session.query(Keyword).all()