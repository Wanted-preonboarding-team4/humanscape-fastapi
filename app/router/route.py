from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database.conn import db

from service.service import get_research_detail

router = APIRouter(prefix="/api")


@router.get("/search")
async def search(q: Optional[str] = None, session: Session = Depends(db.session)):
    data = get_research_detail(q, session)
    if not data:
        return JSONResponse(status_code=404, content={"MESSAGE": "NO DATA"})
    
    return JSONResponse(status_code=200, content={"RESULT": data})