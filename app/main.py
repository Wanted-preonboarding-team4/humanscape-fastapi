# uvicorn app.main:app --reload (app.main 파일 안에 있는 app을 실행, reload는 코드 변경 시 서버 재시작)
import uvicorn
from dataclasses    import dataclass, asdict
from typing         import Optional
from fastapi        import FastAPI, Depends
from router         import route
from database.conn  import db
from common.config  import conf
from sqlalchemy.orm import Session

description = """
# [Assignment 5] 휴먼스케이프 과제

### 팀원 : 강대훈, 김훈태, 이무현

"""


def create_app():
    
    c = conf()
    app = FastAPI(title="Humanscape research API",
                  description=description)
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    
    app.include_router(route.router)
    
    @app.get("/")
    def hello_fastapi():
        return "hello_fastapi"

    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    