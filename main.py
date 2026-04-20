from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import contextlib
from routers import auth, wishlist

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title="Sallijang User Service",
    description="Microservice for handling User auth and profiles",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 로컬 개발용이므로 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(wishlist.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Sallijang User Service API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "user_service"}
