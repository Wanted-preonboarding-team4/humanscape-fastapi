from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from database.conn import db
from dao.dao import get_research_detail_data, batch_update_dao
from urllib import parse
import requests


def get_research_detail(q: Optional[str] = None, session: Session = Depends(db.session)):
    data = get_research_detail_data(q, session)

    if not data:
        return None
    
    data_detail = {
        "research_number": data[0],
        "research_name": data[1],
        "research_subject_count": data[2],
        "research_period": data[3],
        "research_created_at": data[4].strftime('%Y.%m.%d %H:%M:%S'),
        "research_updated_at": data[5].strftime('%Y.%m.%d %H:%M:%S'),
        "department_name": data[6],
        "hospital_name": data[7],
        "type_name": data[8],
        "scope_name": data[9],
        "stage_name": data[10],
    }
    
    return data_detail


# Open API 연결
def get_clinical_information(session):
    default = 'https://api.odcloud.kr/api'
    path = '/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887'
    key = 'UFUf%2FTVAEEqxwHrP8vn1TUNCZLsvr7JROAp2HRCTGaidmHxNyahCRtD0uchYLqO0ziuL6XVtRoCSAMhIkReRaQ%3D%3D'
    queryParams = '?' +parse.urlencode({
        parse.quote_plus("page"): 1,
        parse.quote_plus("perPage"): 145,
    })

    url = default + path + queryParams + "&serviceKey=" + key
    request = requests.get(url)
    datas = request.json()['data']
    batch_update_dao(datas)
    return True
