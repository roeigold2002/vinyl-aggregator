"""Main FastAPI application entry point"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from config import settings
from database import init_db, test_db_connection, seed_stores, SessionLocal
from services.scheduler import init_scheduler, stop_scheduler
from routes import search_router, records_router, stores_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== Lifespan events =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle app startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Vinyl Aggregator API...")
    
    # Test database connection
    if not test_db_connection():
        logger.error("❌ Failed to connect to database. Exiting.")
        raise Exception("Database connection failed")
    
    # Initialize database
    init_db()
    
    # Seed initial store data
    db = SessionLocal()
    try:
        seed_stores(db)
    finally:
        db.close()
    
    # Initialize scheduler
    init_scheduler(SessionLocal)
    
    logger.info("✅ Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    stop_scheduler()
    logger.info("✅ Application shutdown complete")


# ===== Create FastAPI app =====

app = FastAPI(
    title="Vinyl Record Aggregator API",
    description="Search and compare vinyl records across Israeli record stores",
    version="0.1.0",
    lifespan=lifespan,
)


# ===== CORS Middleware =====

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Routes =====

app.include_router(search_router)
app.include_router(records_router)
app.include_router(stores_router)


# ===== Health check =====

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vinyl-aggregator",
        "version": "0.1.0",
    }


@app.get("/")
def root():
    """Root endpoint - API documentation"""
    return {
        "message": "Israeli Vinyl Record Aggregator API",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "search": "/api/search?q=query",
            "records": "/api/records/{id}",
            "stores": "/api/stores",
        }
    }


# ===== Error handlers =====

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
