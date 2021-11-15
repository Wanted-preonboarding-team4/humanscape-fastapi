from dataclasses import dataclass, asdict
from pathlib import Path
from os import environ

from common.consts import DB_PW

BASE_DIR = Path(__file__).resolve().parent.parent  # app 경로
# print(BASE_DIR)


@dataclass
class Config:   
    BASE_DIR = BASE_DIR
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = f"sqlite:///./humanscape.db"


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    print(config)
    return config.get(environ.get("API_ENV", "local"))

print(asdict(LocalConfig()))  # {'DB_POOL_RECYCLE': 900, 'DB_ECHO': True, 'PROJ_RELOAD': True}