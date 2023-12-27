import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host="localhost", port=6379, db=0, encoding="utf-8", decode_responses= True)
    await FastAPILimiter.init(r)


@app.get("/")
async def root():
    return {"message": "Hi! Thank you for visiting the site :)"}