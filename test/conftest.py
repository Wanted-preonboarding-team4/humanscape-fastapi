import os
import asyncio
import pytest
from os import path
from typing import List
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import create_app
from app.database.models import Department, Hospital, Type, Scope, Stage, Research
from app.database.conn import db, Base


@pytest.fixture(scope="session")
def app():
    os.environ["API_ENV"] = "local"
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    # Create tables
    Base.metadata.create_all(db.engine)
    return TestClient(app=app)


@pytest.fixture(scope="function", autouse=True)
def session():
    sess = next(db.session())
    yield sess
    
    sess.rollback()


@pytest.fixture(scope="function")
def research_data(session):
    
    db_department = Department.create(
        id = 1,
        name = 'Cancer Center'
    )
    db_hospital = Hospital.create(
        id = 1,
        name = '가톨릭관동대 국제성모병원'
    )
    db_type = Type.create(
        id = 1,
        name = '관찰연구'
    )
    db_scope = Scope.create(
        id = 1,
        name = '국내다기관'
    )
    db_stage = Stage.create(
        id = 1,
        name = 'Case-only'
    )
    
    session.add(db_department)
    session.add(db_hospital)
    session.add(db_scope)
    session.add(db_stage)
    session.add(db_type)
    session.commit()

    db_research = [
        Research.create(
            id = 1,
            number = 'C160009',
            name = '한국인 알코올사용장애 임상경과1',
            subject_count = 840,
            period = '5년',
            department_id = 1,
            hospital_id = 1,
            type_id = 1,
            scope_id = 1,
            stage_id = 1,
            created_at = datetime.now(),
            updated_at = datetime.now(),
        ),
        Research.create(
            id = 2,
            number = 'C160010',
            name = '한국인 알코올사용장애 임상경과2',
            subject_count = 840,
            period = '5년',
            department_id = 1,
            hospital_id = 1,
            type_id = 1,
            scope_id = 1,
            stage_id = 1,
            created_at = datetime.now(),
            updated_at = datetime.now(),
        ),
        Research.create(
            id = 3,
            number = 'C160011',
            name = '한국인 알코올사용장애 임상경과3',
            subject_count = 840,
            period = '5년',
            department_id = 1,
            hospital_id = 1,
            type_id = 1,
            scope_id = 1,
            stage_id = 1,
            created_at = datetime.now(),
            updated_at = datetime.now(),
        ),
    ]
    session.bulk_save_objects(db_research)
    session.commit()


def clear_all_table_data(session: Session, metadata, except_tables: List[str] = None):
    session.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table in metadata.sorted_tables:
        if table.name not in except_tables:
            session.execute(table.delete())
    session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()