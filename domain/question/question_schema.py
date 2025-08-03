import datetime
from pydantic import BaseModel, field_validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


class Question(BaseModel):
    id : int
    subject : str
    content : str
    create_date : datetime.datetime
    answers: list[Answer] = []  # 답변 목록을 포함하는 필드입니다.
    user: User | None # Pydantic 모델에서 User 타입을 사용하여 질문 작성자를 나타냅니다.
    modify_date: datetime.datetime | None = None  # 수정 날짜 필드, 기본값은 None입니다.
    voter: list[User] = []  # 질문에 투표한 사용자 목록을 나타내는 필드입니다.
    

# Pydantic 모델을 사용하여 JSON 직렬화 및 역직렬화를 자동으로 처리할 수 있습니다.
    # Pydantic은 데이터 검증과 직렬화를 쉽게 해주는 라이브러리입니다.

# subject: str | None = None
# subject 항목은 문자열 또는 None을 가질 수 있고 디폴트 값은 None이라는 뜻이다.

class QuestionCreate(BaseModel):
    subject: str
    content: str
    
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v
    
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []
    
class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int

