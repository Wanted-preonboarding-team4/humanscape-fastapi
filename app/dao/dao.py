<<<<<<< HEAD
from database.models import (
<<<<<<< HEAD
=======
from sqlalchemy.sql.expression import desc, update
from datetime                  import datetime, timedelta
from database.models           import (
>>>>>>> 38ddb70 (feat : research list4)
    Research, 
    Hospital, 
    Department, 
    Stage, 
    Scope, 
    Type
=======
    Department,
    Hospital,
    Type,
    Scope,
    Stage,
    Research
>>>>>>> 52ed1c5 (feat : research list)
)


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


async def batch_update_dao(datas, session):
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
        department_id, scope_id, stage_id, hospital_id =0,0,0,0
        if not session.query(Department).filter(Department.name == data['진료과']).exitst():
            department_id=create_department_dao(data['진료과'],session)

        if not session.query(Scope).filter(Scope.name == data['연구범위']).exitst():
            scope_id=create_scope_dao(data['연구범위'], session)

        if not session.query(Hospital).filter(Hospital.name == data['연구책임기관']).exitst():
            hospital_id=create_hospital_dao(data['연구책임기관'])

        if not session.query(Stage).filter(Stage.name == data['임상시험단계(연구모형)']).exitst():
            stage_id=create_stage_dao(data['임상시험단계(연구모형)'])

        if not session.query(Research).filter(Research.number == data['과제번호']).exitst():
            create_research_dao(session, number, name, period, subject_count, department_id, scope_id, stage_id, hospital_id)
        else:
            update_research_dao(session, number, name, period, subject_count)


def create_research_dao(session, number, name, period, subject_count, department_id, scope_id, stage_id, hospital_id):
    create_research = Research(number        = number,
                               name          = name,
                               period        = period,
                               subject_count = subject_count,
                               department_id = department_id,
                               scope_id      = scope_id,
                               stage_id      = stage_id,
                               hospital_id   = hospital_id)

    session.add(create_research)
    session.commit()
    session.refresh(create_research)


def update_research_dao(session, number, name, peiod, subject_count): # 업데이트가 되는 속성은 연구기간, 연구종류, 실험단계
    research = session.query(Research.stage_id,
                            Research.scope_id).filter(
                            Research.number == number
                            ).first()
    print(research)
    return True


def create_stage_dao(stage_name, session):
    create_stage = Stage(name=stage_name)
    session.add(create_stage)
    session.commit()
    session.refresh(create_stage)
    return create_stage.id


def create_hospital_dao(hospital_name, session):
    create_hospital = Hospital(name=hospital_name)
    session.add(create_hospital)
    session.commit()
    session.refresh(create_hospital)
    return create_hospital.id


def create_department_dao(department_name, session):
    create_department = Hospital(name=department_name)
    session.add(create_department)
    session.commit()
    session.refresh(create_department)
    return create_department.id


def create_scope_dao(scope_name, session):
    create_stage = Scope(name=scope_name)
    session.add(create_stage)
    session.commit()
    session.refresh(create_stage)
    return create_stage.id



# def research_list_dao(skip, limit, session):
#     research_list = session.query(Research).order_by(desc(Research.updated_at)).offset(skip).limit(limit)
#     result = []
#     for i in research_list:
#         result.append(i.to_dict())
#     return result

# def menu_list_repository(skip, limit, session):
#     menu_list = session.query(Menu).offset(skip).limit(limit)
#     temp = []
#     for i in menu_list:
#         temp.append(i.to_dict())
#     return temp