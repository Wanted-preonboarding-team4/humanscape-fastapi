from sqlalchemy.orm import Session, relationship
from database.conn import Base, db
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)

class BaseMixin:
    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

class Department(Base,BaseMixin):
    __tablename__ = 'department'
    name          = Column(String(length=50),nullable=False)
    research      = relationship('Research', backref='department')

class Hospital(Base,BaseMixin):
    __tablename__ = 'hospital'
    name          = Column(String(length=50),nullable=False)
    research      = relationship('Research', backref='hospital')

class Type(Base,BaseMixin):
    __tablename__ = 'type'
    name          = Column(String(length=50),nullable=False)
    research      = relationship('Research', backref='type')

class Scope(Base,BaseMixin):
    __tablename__ = 'scope'
    name          = Column(String(length=50),nullable=False)
    research      = relationship('Research', backref='scope')

class Stage(Base,BaseMixin):
    __tablename__ = 'stage'
    name          = Column(String(length=50),nullable=False)
    research      = relationship('Research', backref='stage')

class Research(Base,BaseMixin):
    __tablename__  = 'research'
    __table_args__ = {'extend_existing': True}
    number         = Column(String(length=50),nullable=False)
    name           = Column(String(length=200),nullable=False)
    subject_count  = Column(Integer,nullable=True)
    period         = Column(String(length=30),nullable=True)
    department_id  = Column(Integer,ForeignKey(Department.id))
    hospital_id    = Column(Integer,ForeignKey(Hospital.id))
    type_id        = Column(Integer,ForeignKey(Type.id))
    scope_id       = Column(Integer,ForeignKey(Scope.id))
    stage_id       = Column(Integer,ForeignKey(Stage.id),nullable=True)

