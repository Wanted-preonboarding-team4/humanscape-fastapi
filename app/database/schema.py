from pydantic import BaseModel

class ResearchList(BaseModel):
    number       : str = 'C000000'
    name         : str = '테스트 연구'
    subject_count: int = 1
    period       : str = '1년'
    department_id: int = 1
    hospital_id  : int = 1
    type_id      : int = 1
    scope_id     : int = 1
    stage_id     : int = 1
    created_at   : str = '2021-11-16 02:08:55.681441'
    updated_at   : str = '2021-11-16 02:08:55.681441'



