from urllib import parse
import requests
from app.dao import dao

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
    dao.batch_update_dao(datas)
    return True
