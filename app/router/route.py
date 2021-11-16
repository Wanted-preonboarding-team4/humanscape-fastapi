from http.client import HTTPException

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from app.service import service
from typing import Optional
from app.database.conn import db

router = APIRouter(prefix='/api')


@router.get("/batch", tags=['batch'])
async def get_batch_clinical_data(serviceKey: Optional[str] = None, session:Session = Depends(db.session)):
    return {'ststus':200}
