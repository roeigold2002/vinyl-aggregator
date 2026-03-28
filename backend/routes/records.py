"""Record detail API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.aggregator import AggregationService
from models import RecordResponse

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("/{record_id}", response_model=RecordResponse)
def get_record_detail(
    record_id: int,
    db: Session = Depends(get_db),
):
    """
    Get detailed information about a specific vinyl record
    
    Includes all available prices across all integrated stores
    """
    from models import Record
    
    record = db.query(Record).filter(Record.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    aggregator = AggregationService(db)
    record_data = aggregator.get_record_with_prices(record_id)
    
    return record_data
