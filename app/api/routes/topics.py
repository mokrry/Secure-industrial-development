from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.topic import Topic, TopicCreate, TopicUpdate
from app.services.topic_service import TopicService

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=List[Topic])
def list_topics(status: Optional[str] = None, db: Session = Depends(get_db)):
    return TopicService(db).list_topics(status=status)


@router.get("/{topic_id}", response_model=Topic)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    t = TopicService(db).get_topic(topic_id)
    if not t:
        raise HTTPException(404, "Topic not found")
    return t


@router.post("", response_model=Topic, status_code=201)
def create_topic(payload: TopicCreate, db: Session = Depends(get_db)):
    return TopicService(db).create_topic(payload)


@router.put("/{topic_id}", response_model=Topic)
def update_topic(topic_id: int, payload: TopicUpdate, db: Session = Depends(get_db)):
    t = TopicService(db).update_topic(topic_id, payload)
    if not t:
        raise HTTPException(404, "Topic not found")
    return t
