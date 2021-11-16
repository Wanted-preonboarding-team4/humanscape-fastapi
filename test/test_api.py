import os
# from app.database import *
from app.main import create_app
from app.database.conn import db, Base
from app.database.models import *
from sqlalchemy.sql.expression import desc
from datetime                  import datetime, timedelta

app = create_app()


def test_get_detail_data_success(client, session):
    research = session.query(
        Research.number,
        Research.name, 
        Research.subject_count, 
        Research.period, 
        Research.created_at, 
        Research.updated_at, 
        Hospital.name,
        Department.name, 
        Scope.name, 
        Type.name, 
        Stage.name) \
    .join(Hospital, Research.hospital_id == Hospital.id) \
    .join(Department, Research.hospital_id == Department.id) \
    .join(Scope, Research.scope_id == Scope.id) \
    .join(Type, Research.type_id == Type.id) \
    .join(Stage, Research.stage_id == Stage.id) \
    .filter(Research.number=='C160009').first()
    
    data = {
        "research_number": research[0],
        "research_name": research[1],
        "research_subject_count": research[2],
        "research_period": research[3],
        "research_created_at": research[4].strftime('%Y.%m.%d %H:%M:%S'),
        "research_updated_at": research[5].strftime('%Y.%m.%d %H:%M:%S'),
        "department_name": research[6],
        "hospital_name": research[7],
        "type_name": research[8],
        "scope_name": research[9],
        "stage_name": research[10],
    }

    response = client.get('/api/search?q=C160009')
    
    assert response.status_code == 200
    assert response.json() == {"RESULT": data}


def test_get_list_data_success(client,skip,limit, session):
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
        Hospital.name,
        Department.name, 
        Scope.name, 
        Type.name, 
        Stage.name) \
    .join(Hospital, Research.hospital_id == Hospital.id) \
    .join(Department, Research.hospital_id == Department.id) \
    .join(Scope, Research.scope_id == Scope.id) \
    .join(Type, Research.type_id == Type.id) \
    .join(Stage, Research.stage_id == Stage.id) \
    .filter(Research.updated_at > before_one_week).order_by(desc(Research.updated_at))[start:start+limit]
    
    data = [{
        "id": research[0], 
        "number": research[1],
        "name": research[2],
        "subject_count": research[3],
        "period": research[4],
        "created_at": research[5].strftime('%Y.%m.%d %H:%M:%S'),
        "updated_at": research[6].strftime('%Y.%m.%d %H:%M:%S'),
        "department_name": research[7],
        "hospital_name": research[8],
        "type_name": research[9],
        "scope_name": research[10],
        "stage_name": research[11],
    }for research in research_list]

    response = client.get('/api/list?skip=1&limit=30')
    
    assert response.status_code == 200
    assert response.json() == {"RESULT": data}

