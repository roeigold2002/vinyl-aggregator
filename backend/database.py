"""Database connection and session management"""
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from config import settings
from models import Base

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Test connections before using
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise


def test_db_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def seed_stores(db: Session):
    """Seed initial store data"""
    from models import Store
    from config import STORE_CONFIGS
    
    try:
        # Check if stores already exist
        existing_count = db.query(Store).count()
        if existing_count > 0:
            logger.info(f"Database already has {existing_count} stores, skipping seed")
            return
        
        stores_to_add = []
        for store_key, config in STORE_CONFIGS.items():
            store = Store(
                name=config["name"],
                store_key=store_key,
                base_url=config["base_url"],
                is_active=True,
            )
            stores_to_add.append(store)
        
        db.add_all(stores_to_add)
        db.commit()
        logger.info(f"✅ Seeded {len(stores_to_add)} stores into database")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error seeding stores: {e}")
        db.rollback()
        raise
