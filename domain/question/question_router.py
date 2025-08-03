from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.question import question_schema, question_crud
# from database import SessionLocal
from database import get_db
# from model import Question
from starlette import status
from domain.user.user_router import get_current_user
from model import User


router = APIRouter(
    prefix="/api/question",
)

# @router.get("/list", response_model = list[question_schema.Question])
# def question_list(db: Session = Depends(get_db)):
#     # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     _question_list = question_crud.get_question_list(db)
#     return _question_list
#     # Question 모델의 모든 데이터를 가져와서 최신순으로 정렬하여 반환하는 API 엔드포인트입니다.

@router.get("/list", response_model = question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, skip = page*size, limit = size, keyword = keyword)

    return {'total': total, 'question_list': _question_list}

# 추가한 response_model=list[question_schema.Question]의 의미는 question_list 함수의 리턴값은 Question 스키마로 구성된 리스트임을 의미한다.

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id = question_id)
    return question
    # 데이터베이스에서 특정 ID에 해당하는 Question 객체를 가져오는 API 엔드포인트입니다.

@router.post("/create", status_code = status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db = db, question_create = _question_create, user = current_user)

@router.put("/update", status_code = status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_update.question_id)
    if not db_question:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "수정 권한이 없습니다.")
    question_crud.update_question(db = db, db_question = db_question, question_update = _question_update)

"""
# 1. 데이터베이스에서 질문 조회
db_question = question_crud.get_question(db, question_id = _question_update.question_id)

# 2. 조회 결과 확인
if not db_question:  # 질문이 존재하지 않으면
    # 3. 에러 발생 → 클라이언트에게 400 에러 응답
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                       detail = "데이터를 찾을 수 없습니다.")

# 4. 질문이 존재하면 다음 코드 실행 계속...
if current_user.id != db_question.user.id:
    # 권한 검사...
"""

@router.delete("/delete", status_code = status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "삭제 권한이 없습니다.")
    question_crud.delete_question(db = db, db_question = db_question)


@router.post("/vote", status_code = status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = "질문을 찾을 수 없습니다.")
    question_crud.vote_question(db, db_question= db_question, db_user = current_user)


