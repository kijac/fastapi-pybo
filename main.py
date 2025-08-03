from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/hello")
# def hello():
#     return {"message": "Hello, World!"}

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)

# 빌드된 정적 파일들을 서빙
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

