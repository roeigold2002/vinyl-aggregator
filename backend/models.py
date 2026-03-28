"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

Base = declarative_base()

# ===== SQLAlchemy ORM Models =====

class Record(Base):
    """Vinyl record product"""
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False, index=True)
    artist = Column(String(300), nullable=False, index=True)
    album = Column(String(300), nullable=False, index=True)
    format = Column(String(100), nullable=True)  # LP, EP, 7", etc.
    cover_art_url = Column(String(1000), nullable=True)
    cover_art_full_url = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = relationship("Price", back_populates="record", cascade="all, delete-orphan")
    
    # Indexes for full-text search (artist || ' ' || album || ' ' || title)
    __table_args__ = (
        Index("ix_record_search", "artist", "album", "title"),
    )
    
    def __repr__(self):
        return f"<Record(id={self.id}, artist={self.artist}, album={self.album})>"


class Store(Base):
    """Vinyl record store"""
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    store_key = Column(String(100), nullable=False, unique=True)  # e.g., "disccenter"
    base_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_scrape = Column(DateTime, nullable=True)
    
    # Relationships
    prices = relationship("Price", back_populates="store", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Store(id={self.id}, name={self.name})>"


class Price(Base):
    """Price and availability for a record at a specific store"""
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False, index=True)
    price_ils = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    quantity_available = Column(Integer, default=0)
    store_url = Column(String(1000), nullable=False)  # Direct link to product on store
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    record = relationship("Record", back_populates="prices")
    store = relationship("Store", back_populates="prices")
    
    __table_args__ = (
        Index("ix_price_record_store", "record_id", "store_id", unique=True),
    )
    
    def __repr__(self):
        return f"<Price(record_id={self.record_id}, store_id={self.store_id}, price={self.price_ils})>"


# ===== Pydantic Schemas (for API) =====

class RecordBase(BaseModel):
    """Base record schema"""
    title: str
    artist: str
    album: str
    format: Optional[str] = None
    cover_art_url: Optional[str] = None
    cover_art_full_url: Optional[str] = None


class RecordCreate(RecordBase):
    """Schema for creating a record"""
    pass


class PriceResponse(BaseModel):
    """Price info for API response"""
    store_id: int
    store_name: str
    price_ils: float
    in_stock: bool
    quantity_available: int
    store_url: str
    last_updated: datetime
    
    class Config:
        from_attributes = True


class RecordResponse(RecordBase):
    """Full record response with prices"""
    id: int
    prices: List[PriceResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordSearchResponse(BaseModel):
    """Simplified record for search results"""
    id: int
    title: str
    artist: str
    album: str
    format: Optional[str]
    cover_art_url: Optional[str]
    min_price: float  # Minimum price across all stores
    prices: List[PriceResponse]
    
    class Config:
        from_attributes = True


class StoreResponse(BaseModel):
    """Store info"""
    id: int
    name: str
    store_key: str
    base_url: str
    last_scrape: Optional[datetime]
    
    class Config:
        from_attributes = True


class ScrapeResultSchema(BaseModel):
    """Result of a scrape job"""
    store_name: str
    records_scraped: int
    records_updated: int
    errors: List[str] = []
    duration_seconds: float
    timestamp: datetime
