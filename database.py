from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config(".env")
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

# import contextlib

SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db" #데이터베이스 접속 주소
#sqlite:///./myapi.db는 sqlite3 데이터베이스의 파일을 의미하며 프로젝트 루트 디렉터리에 저장한다는 의미이다.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#create_engine는 SQLAlchemy의 데이터베이스 엔진을 생성(컨넥션 풀을 생성)하는 함수이다.
#컨넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말함.
#connect_args={"check_same_thread": False}는 SQLite에서 멀티스레드 환경에서 사용할 수 있도록 설정하는 옵션이다.

SessionLocal = sessionmaker(autocommit = False, bind = engine)
#autocommit=False는 세션이 자동으로 커밋되지 않도록 설정한다.
#bind=engine는 세션이 사용할 데이터베이스 엔진을 지정한다.

Base = declarative_base()

# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# naming_convention은 테이블과 컬럼의 이름 규칙을 정의하는 딕셔너리이다.
# 이 규칙은 SQLAlchemy가 테이블과 컬럼을 생성할 때 이름을 지정하는 데 사용된다.
# 예를 들어, "ix"는 인덱스의 접두사로 사용되며, "uq"는 유니크 제약 조건의 접두사로 사용된다.
Base.metadata = MetaData(naming_convention = naming_convention)

