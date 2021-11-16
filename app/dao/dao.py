from sqlalchemy.sql.expression import desc
from datetime                  import datetime, timedelta
from database.models           import (
    Research, 
    Hospital, 
    Department, 
    Stage, 
    Scope, 
    Type
)
from sqlalchemy.sql import exists 


def get_research_detail_data(q, session):
    research = session.query(
        Research.number,
        Research.name, 
        Research.subject_count, 
        Research.period, 
        Research.created_at, 
        Research.updated_at,
        Department.name,  
        Hospital.name,
        Type.name, 
        Scope.name, 
        Stage.name) \
    .join(Hospital, Research.hospital_id == Hospital.id) \
    .join(Department, Research.department_id == Department.id) \
    .join(Scope, Research.scope_id == Scope.id) \
    .join(Type, Research.type_id == Type.id) \
    .join(Stage, Research.stage_id == Stage.id,isouter=True) \
    .filter(Research.number==q).first()


    if research:
        return research
    
    return None


def research_list_dao(skip, limit, session):
    start = (int(skip)-1) * limit
    now = datetime.now()
    before_one_week = now - timedelta(weeks=1)

    research_list = session.query(
        Research.id,
        Research.number,
        Research.name, 
        Research.subject_count, 
        Research.period, 
        Research.created_at, 
        Research.updated_at,
        Department.name,  
        Hospital.name,
        Type.name, 
        Scope.name, 
        Stage.name) \
    .join(Hospital, Research.hospital_id == Hospital.id) \
    .join(Department, Research.department_id == Department.id) \
    .join(Scope, Research.scope_id == Scope.id) \
    .join(Type, Research.type_id == Type.id) \
    .join(Stage, Research.stage_id == Stage.id, isouter=True)\
    .filter(Research.updated_at > before_one_week).order_by(desc(Research.updated_at))[start:start+limit]

    if research_list:
        return research_list
    
    return None


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
        name   = data['과제명']
        period = data['연구기간']
        subject_count = data['전체목표연구대상자수']
        department = data['진료과']
        scope = data['연구범위']
        stage = data['임상시험단계(연구모형)']

        if not session.query(exists().where(Department.name == data['진료과'])).scalar():
            department_id=create_department_dao(data['진료과'], session)
        else:
            department_id = session.query(Department.id).filter(Department.name == department).first()[0]
            
        if not session.query(exists().where(Scope.name == data['연구범위'])).scalar():
            scope_id=create_scope_dao(data['연구범위'], session)
        else:
            scope_id = session.query(Scope.id).filter(Scope.name == scope).first()[0]

        if not session.query(exists().where(Hospital.name == data['연구책임기관'])).scalar():
            hospital_id=create_hospital_dao(data['연구책임기관'], session)
        else:
            hospital_id = session.query(Hospital.id).filter(Hospital.name == data['연구책임기관']).first()[0]

        if not session.query(exists().where(Stage.name == data['임상시험단계(연구모형)'])).scalar():
            stage_id=create_stage_dao(data['임상시험단계(연구모형)'], session)
        else:
            stage_id = session.query(Stage.id).filter(Stage.name == stage).first()[0]
        
        if not session.query(exists().where(Research.number == data['과제번호'])).scalar():
            create_research_dao(session, number, name, period, subject_count, department_id, scope_id, stage_id, hospital_id)
        else:
            update_research_dao(session, number, name, period, subject_count, stage_id)


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
    research = session.query(Research).filter(Research.number == number).first()

    research.period = period
    research.subject_count = subject_count
    research.stage_id = stage_id
    research.updated_at = datetime.now()

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

    return create_stage.id


def create_hospital_dao(hospital_name, session):
    create_hospital = Hospital(
        name=hospital_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_hospital)
    session.commit()

    return create_hospital.id


def create_department_dao(department_name, session):
    create_department = Department(
        name=department_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_department)
    session.commit()

    return create_department.id


def create_scope_dao(scope_name, session):
    create_stage = Scope(
        name=scope_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    session.add(create_stage)
    session.commit()

    return create_stage.id


