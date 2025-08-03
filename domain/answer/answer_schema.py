from pydantic import BaseModel, field_validator
import datetime
from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v
    # content 필드가 비어있지 않도록 검증하는 메서드입니다.

class Answer(BaseModel):
    id : int
    content: str
    create_date: datetime.datetime
    user: User | None  # 답변 작성자를 나타내는 필드입니다.
    question_id: int  # 답변이 속한 질문의 ID입니다.
    modify_date: datetime.datetime | None = None  # 수정 날짜 필드, 기본값은 None입니다.
    voter: list[User] = []  # 답변에 투표한 사용자 목록을 나타내는 필드입니다.
    


class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int

class AnswerVote(BaseModel):
    answer_id: int