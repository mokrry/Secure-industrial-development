from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.topic import Topic as TopicModel
from app.schemas.topic import TopicCreate, TopicUpdate

class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, status: Optional[str] = None) -> List[TopicModel]:
        stmt = select(TopicModel)
        if status:
            stmt = stmt.where(TopicModel.status == status)
        return list(self.db.execute(stmt).scalars().all())

    def get(self, topic_id: int) -> Optional[TopicModel]:
        return self.db.get(TopicModel, topic_id)

    def create(self, data: TopicCreate) -> TopicModel:
        obj = TopicModel(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, topic_id: int, data: TopicUpdate) -> Optional[TopicModel]:
        obj = self.get(topic_id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj
