from typing         import Optional
from fastapi        import Depends, requests
from sqlalchemy.orm import Session
from database.conn  import db
from dao.dao        import get_research_detail_data, batch_update_dao, research_list_dao
from urllib         import parse


def get_research_detail(q: Optional[str] = None, session: Session = Depends(db.session)):
    data = get_research_detail_data(q, session)

    if not data:
        return None
    
    data_detail = {
        "research_number"       : data[0],
        "research_name"         : data[1],
        "research_subject_count": data[2],
        "research_period"       : data[3],
        "research_created_at"   : data[4].strftime('%Y.%m.%d %H:%M:%S'),
        "research_updated_at"   : data[5].strftime('%Y.%m.%d %H:%M:%S'),
        "department_name"       : data[6],
        "hospital_name"         : data[7],
        "type_name"             : data[8],
        "scope_name"            : data[9],
        "stage_name"            : data[10],
    }
    return data_detail


# Open API 연결
def get_clinical_information(serviceKey, session):
    default = 'https://api.odcloud.kr/api'
    path = '/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887'
    queryParams = '?' +parse.urlencode({
        parse.quote_plus("page"): 1,
        parse.quote_plus("perPage"): 145,
    })

    url = default + path + queryParams + "&serviceKey=" + serviceKey
    request = requests.get(url)
    datas = request.json()['data']

    batch_update_dao(datas, session)


def research_list_service(skip, limit, session):
    research_list = research_list_dao(skip, limit, session)
    if not research_list: 
        return None

    data_list = [{
        "id"           : data[0],
        "number"       : data[1],
        "name"         : data[2],
        "subject_count": data[3],
        "period"       : data[4],
        "created_at"   : data[5].strftime('%Y.%m.%d %H:%M:%S'),
        "updated_at"   : data[6].strftime('%Y.%m.%d %H:%M:%S'),
        "department"   : data[7],
        "hospital"     : data[8],
        "type"         : data[9],
        "scope"        : data[10],
        "stage"        : data[11],
    }for data in research_list]

    return data_list
