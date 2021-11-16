import requests
from typing import Optional
from urllib import parse
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists 

from database.models import (
    Research, 
    Hospital, 
    Department, 
    Stage, 
    Scope, 
    Type
)


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

    batch_update_dao(datas, session)
    return True

def batch_update_dao(datas, session):
    # matched = {'과제번호' :
    #                '과제명':
    # '진료과'	Department
    # '연구책임기관' Hospital
    # '전체목표연구대상자수' subject_count
    # '연구기간'	period
    # '연구종류'	Type
    # '임상시험단계(연구모형)'Stage
    # '연구범위'Scope
    # }

# API 데이터 데이터베이스에 넣는 작업
    for data in datas:
        number = data['과제번호']
        name = data['과제명']
        period = data['연구기간']
        subject_count = data['전체목표연구대상자수']
        department = data['진료과']
        scope = data['연구범위']
        stage = data['임상시험단계(연구모형)']

        # department_id, scope_id, stage_id, hospital_id =0,0,0,0

        # if not session.query(Department).filter(Department.name == data['진료과']).exists():
        if not session.query(exists().where(Department.name == data['진료과'])).scalar():
            department_id=create_department_dao(data['진료과'], session)
        else:
            department_id = session.query(Department.id).filter(Department.name == department).first()[0]
            
        # if not session.query(Scope).filter(Scope.name == data['연구범위']).exists():
        if not session.query(exists().where(Scope.name == data['연구범위'])).scalar():
            scope_id=create_scope_dao(data['연구범위'], session)
        else:
            scope_id = session.query(Scope.id).filter(Scope.name == scope).first()[0]

        # if not session.query(Hospital).filter(Hospital.name == data['연구책임기관']).exists():
        if not session.query(exists().where(Hospital.name == data['연구책임기관'])).scalar():
            hospital_id=create_hospital_dao(data['연구책임기관'], session)
        else:
            hospital_id = session.query(Hospital.id).filter(Hospital.name == data['연구책임기관']).first()[0]
        # if not session.query(Stage).filter(Stage.name == data['임상시험단계(연구모형)']).exists():
        if not session.query(exists().where(Stage.name == data['임상시험단계(연구모형)'])).scalar():
            stage_id=create_stage_dao(data['임상시험단계(연구모형)'], session)
        else:
            stage_id = session.query(Stage.id).filter(Stage.name == stage).first()[0]
        
        # if not session.query(Research).filter(Research.number == data['과제번호']).exists():
        if not session.query(exists().where(Research.number == data['과제번호'])).scalar():
            create_research_dao(session, number, name, period, subject_count, department_id, scope_id, stage_id, hospital_id)
        else:
            update_research_dao(session, number, name, period, subject_count, stage)


def create_research_dao(session, number, name, period, subject_count, department_id, scope_id, stage_id, hospital_id):
    create_research = Research(number=number,
                               name=name,
                               period=period,
                               subject_count=subject_count,
                               department_id=department_id,
                               scope_id=scope_id,
                               stage_id=stage_id,
                               hospital_id=hospital_id,
                               created_at = datetime.now(),
                               updated_at = datetime.now(),
                               )

    session.add(create_research)
    session.commit()
    session.refresh(create_research)


def update_research_dao(session, number, name, period, subject_count, stage_id): # 업데이트가 되는 속성은 연구기간, 연구종류, 실험단계
    # research = session.query(Research.stage_id,
    #                         Research.scope_id).filter(
    #                         Research.number == number
    #                         ).first()
    research = session.query(Research).filter(Research.number == number).first()
    print(research)
    research.period = period
    research.subject_count = subject_count
    research.stage = stage_id
    research.updated_at = datetime.now()
    print(research)
    session.commit()

    return True


def create_stage_dao(stage_name, session):
    create_stage = Stage(
        name=stage_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_stage)
    session.commit()
    # session.refresh(create_stage)
    return create_stage.id


def create_hospital_dao(hospital_name, session):
    create_hospital = Hospital(
        name=hospital_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_hospital)
    session.commit()
    # session.refresh(create_hospital)
    return create_hospital.id


def create_department_dao(department_name, session):
    create_department = Department(
        name=department_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_department)
    session.commit()
    # session.refresh(create_department)
    return create_department.id


def create_scope_dao(scope_name, session):
    create_stage = Scope(
        name=scope_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_stage)
    session.commit()
    # session.refresh(create_stage)
    return create_stage.id

def create_app():
    
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    
    return app

app = create_app()

if __name__ == '__main__':
    print('start update')
    get_clinical_information(session)
    print('update done')