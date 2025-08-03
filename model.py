from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('question_id', Integer, ForeignKey('questions.id'), primary_key = True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key = True)
)


class Question(Base):
    __tablename__="questions"  #테이블 이름

    id = Column(Integer, primary_key = True)  #id 컬럼, 기본키로 설정
    subject = Column(String, nullable = False) #subject 컬럼, 문자열 타입, null 허용 안함
    content = Column(Text, nullable = False)  #content 컬럼, 텍스트 타입, null 허용 안함
    create_date = Column(DateTime, nullable = False) #create_date 컬럼, 날짜/시간 타입, null 허용 안함
    user_id = Column(Integer, ForeignKey("user.id"), nullable = True)
    # user_id 컬럼, user 테이블의 id를 외래키로 설정, null 허용
    user = relationship("User", backref = "question_users")
    # User 모델과의 관계 설정, backref를 통해 User에서 question_users 속성으로 접근 가능
    modify_date = Column(DateTime, nullable = True) # 수정 날짜 컬럼, null 허용
    voter = relationship('User', secondary = question_voter, backref = 'question_voters')
    # voter 속성은 User 모델과 다대다 관계를 설정, question_voter 테이블을 통해 연결됨


class Answer(Base):
    __tablename__ = "answer" #테이블 이름

    id = Column(Integer, primary_key = True)  #id 컬럼, 기본키로 설정
    content = Column(Text, nullable = False)  #content 컬럼, 텍스트 타입, null 허용 안함
    create_date = Column(DateTime, nullable = False)  #create_date 컬럼, 날짜/시간 타입, null 허용 안함
    question_id = Column(Integer, ForeignKey("questions.id"))  #question_id 컬럼, questions 테이블의 id를 외래키로 설정
    question = relationship("Question", backref = "answers")  #Question 모델과의 관계 설정, backref를 통해 Question에서 answers 속성으로 접근 가능
    #backref 파라미터는 역참조 설정. answers 속성을 통해 Question 객체에서 관련된 Answer 객체에 접근할 수 있게 한다.
    user_id = Column(Integer, ForeignKey("user.id"), nullable = True)
    # user_id 컬럼, user 테이블의 id를 외래키로 설정, null 허용
    user = relationship("User", backref = "answer_users")
    # User 모델과의 관계 설정, backref를 통해 User에서 answer_users 속성으로 접근 가능
    modify_date = Column(DateTime, nullable = True)
    voter = relationship('User', secondary = answer_voter, backref = 'answer_voters')
    # voter 속성은 User 모델과 다대다 관계를 설정, answer_voter 테이블을 통해 연결됨

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)

