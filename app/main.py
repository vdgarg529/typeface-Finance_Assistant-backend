 
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.db.base import Base
# from app.db.session import engine
# from app.routers import auth, transactions, receipts

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Personal Finance Assistant", version="1.0.0")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(auth.router)
# app.include_router(transactions.router)
# app.include_router(receipts.router)

# @app.get("/")
# def read_root():
#     return {"message": "Personal Finance Assistant API"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routers import auth, transactions, receipts
from app.core.config import settings
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Assistant", version="1.0.0")

# Add CORS middleware with dynamic origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(receipts.router)

@app.get("/")
def read_root():
    return {"message": "Personal Finance Assistant API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add this for Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)