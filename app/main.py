from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException
from app.api.api import api_router
from app.db.database import Base, engine, metadata, database

Base.metadata.create_all(engine)

app = FastAPI()
origins = [    
    "http://127.0.0.1:8000/",
    "http://localhost:8081",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    #allow_methods=["*"],
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],    
)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,content={"detail": exc.message})

@app.on_event("startup")
async def startup():
    await database.connect()  

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"This is first Python FastAPI Demo"}

app.include_router(api_router,prefix="/api")

#app.include_router(blogs.router, prefix="/api/blogs", tags=["blogs"])
