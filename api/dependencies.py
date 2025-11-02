from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Optional

ModelType = TypeVar("ModelType")


def get_object_or_404(
    db: Session,
    model: Type[ModelType],
    object_id: int,
    error_message: str = "Object not found"
) -> ModelType:
    obj = db.query(model).filter(model.id == object_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
    return obj

