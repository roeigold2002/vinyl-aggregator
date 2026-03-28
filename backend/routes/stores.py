"""Store information API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Store, StoreResponse
from typing import List

router = APIRouter(prefix="/api/stores", tags=["stores"])


@router.get("", response_model=List[StoreResponse])
def list_stores(
    db: Session = Depends(get_db),
):
    """
    List all integrated vinyl record stores
    """
    stores = db.query(Store).filter(Store.is_active == True).all()
    return stores


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: int,
    db: Session = Depends(get_db),
):
    """
    Get information about a specific store
    """
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    return store


@router.post("/trigger-scrape", tags=["admin"])
def trigger_scrape(db: Session = Depends(get_db)):
    """
    Manually trigger a scrape of all stores (useful for testing)
    
    Returns immediately; scraping happens in background
    """
    from services.scheduler import trigger_scrape_manually
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from config import settings
    
    # Create a separate session factory for the background job
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    trigger_scrape_manually(SessionLocal)
    
    return {"message": "Scrape triggered", "status": "background"}
