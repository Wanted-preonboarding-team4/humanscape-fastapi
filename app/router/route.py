from typing              import Optional, List
from fastapi             import APIRouter, Depends, Header, Request
from sqlalchemy.orm      import Session
from starlette.responses import JSONResponse
from http.client import HTTPException
from service.service import get_clinical_information, get_research_detail, research_list_service
from database.conn import db
from database.schema     import ResearchList

router = APIRouter(prefix="/api")


@router.get("/search", tags=['research'])
async def search(q: Optional[str] = None, session: Session = Depends(db.session)):
    data = get_research_detail(q, session)
    if not data:
        return JSONResponse(status_code=404, content={"MESSAGE": "NO DATA"})
    
    return JSONResponse(status_code=200, content={"RESULT": data})


@router.get("/batch", tags=['batch'])
async def get_batch_clinical_data(serviceKey: Optional[str] = None, session:Session = Depends(db.session)):
    get_clinical_information(serviceKey, session)
    return {'ststus':200}


@router.get("/list", response_model=List[ResearchList], tags=['research']) 
async def research_list(skip: int = 1, limit: int = 30, session: Session = Depends(db.session)):
    research_list=research_list_service(skip, limit, session)
    if skip < 0:
        return JSONResponse(status_code=400, content={"MESSAGE": "NOT LIST"})

    return JSONResponse(status_code=200, content={"RESULT": research_list})

