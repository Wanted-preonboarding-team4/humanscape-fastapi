from typing import Optional, List
from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database.conn import db
from http.client import HTTPException
<<<<<<< HEAD
from service.service import get_research_detail
=======
from service.service import get_research_detail, research_list_service
from database.schema import ResearchList
>>>>>>> 38ddb70 (feat : research list4)

router = APIRouter(prefix="/api")


@router.get("/search", tags=['research'])
async def search(q: Optional[str] = None, session: Session = Depends(db.session)):
    data = get_research_detail(q, session)
    if not data:
        return JSONResponse(status_code=404, content={"MESSAGE": "NO DATA"})
    
    return JSONResponse(status_code=200, content={"RESULT": data})


@router.get("/batch", tags=['batch'])
async def get_batch_clinical_data(serviceKey: Optional[str] = None, session:Session = Depends(db.session)):
    return {'ststus':200}
from fastapi.responses import JSONResponse

from http.client    import HTTPException
from sqlalchemy.orm import Session
from typing         import Optional

from database.conn   import db
from database.models import Research
from service.service import research_list_service

router = APIRouter(prefix='/api')

<<<<<<< HEAD
@router.get('/list', response_model=List[Research], tags=['research']) 
async def research_list(offset: int = None, limit: int = None, session: Session=Depends(db.session)):
    research_list=research_list_service(offset,limit,session)
    return JSONResponse(status_code=200, content=dict(msg=research_list))
    
=======
@router.get("/batch", tags=['batch'])
async def get_batch_clinical_data(serviceKey: Optional[str] = None, session:Session = Depends(db.session)):
    return {'ststus':200}

<<<<<<< HEAD
@router.get('/list', tags=['research']) 
async def research_list(
    offset : int     = 0,
    limit  : int     = 10,
    session: Session = Depends(db.session)):
    research_list=research_list_service(offset,limit,session)
    return JSONResponse(status_code=200, content=dict(msg=research_list))[offset:offset+limit]
   

>>>>>>> 772b769 (feat : research list2)
=======
@router.get("/list", response_model=List[ResearchList], tags=['research']) 
async def research_list(skip: int = 1, limit: int = 30, session: Session = Depends(db.session)):
    research_list=research_list_service(skip, limit, session)
    return JSONResponse(status_code=200, content={"RESULT": research_list})
>>>>>>> 38ddb70 (feat : research list4)
