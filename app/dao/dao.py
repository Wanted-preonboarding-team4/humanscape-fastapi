from database.models import (
    Research, 
    Hospital, 
    Department, 
    Stage, 
    Scope, 
    Type
)


def get_research_detail_data(q, session):
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
    .filter(Research.number==q).first()

    if research:
        return research
    
    return None