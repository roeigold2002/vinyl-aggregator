"""Data aggregation and deduplication service"""
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import Record, Price, Store

logger = logging.getLogger(__name__)


class AggregationService:
    """Service for aggregating scraped products and managing duplicates"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def aggregate_scrape_results(
        self, 
        store_id: int,
        products: List[Dict],
    ) -> Tuple[int, int, List[str]]:
        """
        Aggregate scraped products into database
        
        Args:
            store_id: ID of the store being scraped
            products: List of product dicts from scraper
        
        Returns:
            (created_count, updated_count, errors)
        """
        created_count = 0
        updated_count = 0
        errors = []
        
        logger.info(f"📦 Aggregating {len(products)} products for store_id={store_id}")
        
        for product_data in products:
            try:
                created_or_updated = self._upsert_product(store_id, product_data)
                
                if created_or_updated == "created":
                    created_count += 1
                elif created_or_updated == "updated":
                    updated_count += 1
            
            except Exception as e:
                error_msg = f"Error upserting product: {product_data.get('title', 'unknown')} - {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        # Update store's last_scrape time
        try:
            store = self.db.query(Store).filter(Store.id == store_id).first()
            if store:
                store.last_scrape = datetime.utcnow()
                self.db.commit()
        except Exception as e:
            logger.error(f"Error updating store last_scrape: {e}")
        
        logger.info(f"✅ Aggregation complete: {created_count} created, {updated_count} updated, {len(errors)} errors")
        return created_count, updated_count, errors
    
    def _upsert_product(self, store_id: int, product_data: Dict) -> str:
        """
        Insert or update a product record
        
        Returns: "created" or "updated"
        """
        # Deduplicate by (artist, album, title)
        artist = product_data.get('artist', '').strip()
        album = product_data.get('album', '').strip()
        title = product_data.get('title', '').strip()
        
        if not artist or not album or not title:
            raise ValueError(f"Missing required fields: artist={artist}, album={album}, title={title}")
        
        # Find existing record
        existing_record = self.db.query(Record).filter(
            Record.artist == artist,
            Record.album == album,
            Record.title == title,
        ).first()
        
        if existing_record:
            # Update existing record
            existing_record.format = product_data.get('format')
            existing_record.cover_art_url = product_data.get('cover_art_url')
            existing_record.cover_art_full_url = product_data.get('cover_art_full_url')
            existing_record.updated_at = datetime.utcnow()
            record_id = existing_record.id
            action = "updated"
        else:
            # Create new record
            new_record = Record(
                title=title,
                artist=artist,
                album=album,
                format=product_data.get('format'),
                cover_art_url=product_data.get('cover_art_url'),
                cover_art_full_url=product_data.get('cover_art_full_url'),
            )
            self.db.add(new_record)
            self.db.flush()  # Get the ID before commit
            record_id = new_record.id
            action = "created"
        
        # Upsert price record
        price_query = self.db.query(Price).filter(
            Price.record_id == record_id,
            Price.store_id == store_id,
        ).first()
        
        if price_query:
            # Update existing price
            price_query.price_ils = product_data.get('price_ils', 0)
            price_query.in_stock = product_data.get('in_stock', False)
            price_query.quantity_available = product_data.get('quantity_available', 0)
            price_query.store_url = product_data.get('store_url', '')
            price_query.last_updated = datetime.utcnow()
        else:
            # Create new price
            new_price = Price(
                record_id=record_id,
                store_id=store_id,
                price_ils=product_data.get('price_ils', 0),
                in_stock=product_data.get('in_stock', False),
                quantity_available=product_data.get('quantity_available', 0),
                store_url=product_data.get('store_url', ''),
            )
            self.db.add(new_price)
        
        self.db.commit()
        return action
    
    def get_record_with_prices(self, record_id: int) -> Optional[Dict]:
        """Get a record with all price info across stores"""
        record = self.db.query(Record).filter(Record.id == record_id).first()
        
        if not record:
            return None
        
        prices = self.db.query(Price).filter(Price.record_id == record_id).all()
        
        return {
            'id': record.id,
            'title': record.title,
            'artist': record.artist,
            'album': record.album,
            'format': record.format,
            'cover_art_url': record.cover_art_url,
            'prices': [
                {
                    'store_id': p.store_id,
                    'store_name': p.store.name,
                    'price_ils': p.price_ils,
                    'in_stock': p.in_stock,
                    'quantity_available': p.quantity_available,
                    'store_url': p.store_url,
                    'last_updated': p.last_updated.isoformat(),
                }
                for p in prices
            ]
        }
    
    def search_records(self, query: str, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Search records by artist/album/title"""
        from sqlalchemy import or_, func
        
        # Simple text search - improve later with full-text search
        search_term = f"%{query}%"
        
        records = self.db.query(Record).filter(
            or_(
                Record.artist.ilike(search_term),
                Record.album.ilike(search_term),
                Record.title.ilike(search_term),
            )
        ).limit(limit).offset(offset).all()
        
        results = []
        for record in records:
            prices = self.db.query(Price).filter(Price.record_id == record.id).all()
            
            min_price = min([p.price_ils for p in prices]) if prices else 0
            
            results.append({
                'id': record.id,
                'title': record.title,
                'artist': record.artist,
                'album': record.album,
                'format': record.format,
                'cover_art_url': record.cover_art_url,
                'min_price': min_price,
                'prices': [
                    {
                        'store_id': p.store_id,
                        'store_name': p.store.name,
                        'price_ils': p.price_ils,
                        'in_stock': p.in_stock,
                        'quantity_available': p.quantity_available,
                        'store_url': p.store_url,
                    }
                    for p in prices
                ]
            })
        
        return results
