from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.topic import TopicCreate, TopicUpdate, Topic as TopicSchema
from app.repositories.topic_repo import TopicRepository

class TopicService:
    def __init__(self, db: Session):
        self.repo = TopicRepository(db)

    def list_topics(self, status: Optional[str]) -> List[TopicSchema]:
        return self.repo.list(status=status)

    def get_topic(self, topic_id: int) -> Optional[TopicSchema]:
        return self.repo.get(topic_id)

    def create_topic(self, payload: TopicCreate) -> TopicSchema:
        return self.repo.create(payload)

    def update_topic(self, topic_id: int, payload: TopicUpdate) -> Optional[TopicSchema]:
        return self.repo.update(topic_id, payload)
