"""Search API routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.aggregator import AggregationService
from models import RecordSearchResponse
from typing import List

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=List[RecordSearchResponse])
def search_records(
    q: str = Query(..., min_length=1, description="Search query (artist, album, or title)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Search for vinyl records by artist, album, or title
    
    Returns records with prices from all stores
    """
    aggregator = AggregationService(db)
    results = aggregator.search_records(q, limit=limit, offset=offset)
    return results


@router.get("/autocomplete", response_model=List[str])
def search_autocomplete(
    q: str = Query(..., min_length=2, description="Autocomplete query"),
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """
    Get autocomplete suggestions for artists and albums
    """
    from sqlalchemy import or_, func, text
    from models import Record
    
    # Simple prefix match on artist and album
    search_term = f"{q}%"
    
    artists = db.query(Record.artist).distinct().filter(
        Record.artist.ilike(search_term)
    ).limit(limit).all()
    
    albums = db.query(Record.album).distinct().filter(
        Record.album.ilike(search_term)
    ).limit(limit).all()
    
    suggestions = []
    suggestions.extend([a[0] for a in artists])
    suggestions.extend([a[0] for a in albums])
    
    # Remove duplicates and return
    return list(set(suggestions))[:limit]
