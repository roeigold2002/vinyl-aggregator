# Project Summary - Israeli Vinyl Record Aggregator

## ✅ Phase 1 MVP - COMPLETE

**Development Status**: Implementation complete, ready for testing  
**Timeline**: Phase 1 of 4  
**Scope**: 2 initial stores (DiscCenter, TheVinylRoom) with ~3,500-4,000 records

---

## What Was Built

### Backend (FastAPI + Python)

**Location**: `backend/`

**Core Files**:
- `main.py` - FastAPI application entry point with startup/shutdown handlers
- `config.py` - Configuration management and store metadata
- `models.py` - SQLAlchemy ORM models + Pydantic schemas
- `database.py` - PostgreSQL connection, session management, initialization

**Scrapers** (`backend/scrapers/`):
- `base.py` - Abstract base class with common scraping logic
- `disccenter.py` - DiscCenter.co.il scraper (2000-3000 products)
- `thevinylroom.py` - TheVinylRoom.co.il scraper (1000-1500 products)

**Services** (`backend/services/`):
- `aggregator.py` - Deduplication, price normalization, record upsert logic
- `scheduler.py` - APScheduler configuration for daily scraping jobs

**Routes** (`backend/routes/`):
- `search.py` - `GET /api/search` and autocomplete endpoints
- `records.py` - `GET /api/records/{id}` for record details
- `stores.py` - Store listing, metadata, manual scrape trigger

**Database Schema**:
```sql
-- Vinyl records
CREATE TABLE records (
  id INTEGER PRIMARY KEY,
  title VARCHAR(500),
  artist VARCHAR(300),
  album VARCHAR(300),
  format VARCHAR(100),
  cover_art_url VARCHAR(1000),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  INDEXES: (artist, album, title)
);

-- Record stores
CREATE TABLE stores (
  id INTEGER PRIMARY KEY,
  name VARCHAR(200),
  store_key VARCHAR(100),
  base_url VARCHAR(500),
  is_active BOOLEAN,
  last_scrape TIMESTAMP
);

-- Prices & availability
CREATE TABLE prices (
  id INTEGER PRIMARY KEY,
  record_id INTEGER,
  store_id INTEGER,
  price_ils FLOAT,
  in_stock BOOLEAN,
  quantity_available INTEGER,
  store_url VARCHAR(1000),
  last_updated TIMESTAMP,
  UNIQUE: (record_id, store_id)
);
```

### Frontend (React + Vite)

**Location**: `frontend/`

**Components** (`frontend/src/components/`):
- `SearchInput.jsx` - Search form with submit handling
- `ResultsList.jsx` - Grid of search results with expandable prices
- `PriceComparison.jsx` - Store comparison table with "Buy" links

**Hooks** (`frontend/src/hooks/`):
- `useSearch.js` - Custom hook managing search state and API calls

**Services** (`frontend/src/services/`):
- `api.js` - Axios client with all API methods

**Styles** (`frontend/src/styles/`):
- `globals.css` - CSS variables, theme, app layout
- `components.css` - Component-specific styles
- `index.css` - Base element styling

**Pages** (`frontend/src/pages/`):
- `SearchPage.jsx` - Main search interface (to be expanded)

**Key Features**:
- Responsive design (mobile-first)
- Dark theme with accent colors
- Expandable price comparison tables
- Direct store product links
- Keyboard navigation support

### Infrastructure & Docs

**Docker**:
- `docker-compose.yml` - PostgreSQL + Redis services

**Configuration**:
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules

**Documentation**:
- `README.md` - Project overview, features, quick start
- `SETUP.md` - Development environment setup guide
- `DEPLOYMENT.md` - Production deployment guide
- `SCRIPTS.md` - Helper scripts for common tasks
- `frontend/README.md` - Frontend-specific documentation

---

## Key Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **FastAPI** | Async support, auto-generated docs, type safety |
| **PostgreSQL FTS** | Sufficient for 8,000 products; simpler than Elasticsearch |
| **BeautifulSoup** | 10/12 stores server-rendered; simple to implement |
| **React + Vite** | Modern tooling, fast dev server, small bundle |
| **APScheduler** | Simple for daily batch jobs; Celery overkill for MVP |
| **Railway + Vercel** | Low cost, auto-scaling, integrated CI/CD |

---

## API Endpoints (MVP)

### Search
- `GET /api/search?q=query` - Full-text search ✅
- `GET /api/search/autocomplete?q=query` - Suggestions ✅

### Records
- `GET /api/records/{id}` - Record details with all prices ✅

### Stores
- `GET /api/stores` - List all stores ✅
- `GET /api/stores/{id}` - Store details ✅
- `POST /api/stores/trigger-scrape` - Manual scrape (admin) ✅

### Health
- `GET /health` - Health check ✅
- `GET /` - Root/documentation ✅

**Full API docs auto-generated at**: `http://localhost:8000/docs` (Swagger UI)

---

## Data Flow

```
Store Websites
    ↓
[Scraper] (DiscCenter, TheVinylRoom)
    ↓
[Parse + Extract] (BeautifulSoup)
    ↓
[Aggregation Service] (Dedup, Normalize)
    ↓
PostgreSQL Database
    ↓
[FastAPI Routes]
    ↓
[React Frontend]
    ↓
User Search Interface
```

---

## Technology Stack Summary

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Scraping**: BeautifulSoup4, Requests
- **Scheduling**: APScheduler 3.10
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic 2.5

### Frontend
- **Language**: JavaScript (ES6+)
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **HTTP Client**: Axios 1.6
- **Styling**: CSS3 (CSS Variables, Flexbox, Grid)

### DevOps
- **Containerization**: Docker + Docker Compose
- **Backend Hosting**: Railway
- **Frontend Hosting**: Vercel
- **Database**: PostgreSQL (Railway managed)

---

## File Structure

```
Project V/
├── README.md                      # Project overview
├── SETUP.md                       # Development setup
├── DEPLOYMENT.md                  # Production deployment
├── SCRIPTS.md                     # Helper scripts
├── docker-compose.yml             # Docker services
├── .gitignore                     # Git ignore rules
│
├── backend/                       # Python/FastAPI backend
│   ├── main.py                   # App entry point
│   ├── config.py                 # Config & store metadata
│   ├── models.py                 # DB models & schemas
│   ├── database.py               # DB connection & init
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   ├── scrapers/                 # Web scrapers
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract base class
│   │   ├── disccenter.py         # DiscCenter scraper
│   │   └── thevinylroom.py       # TheVinylRoom scraper
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── aggregator.py         # Data aggregation
│   │   └── scheduler.py          # Scraping scheduler
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── search.py             # Search endpoints
│   │   ├── records.py            # Record endpoints
│   │   └── stores.py             # Store endpoints
│   └── tests/                    # Test suite
│       ├── __init__.py
│       └── test_api.py           # API tests
│
└── frontend/                      # React/Vite frontend
    ├── package.json              # NPM dependencies
    ├── vite.config.js            # Vite config
    ├── index.html                # HTML entry point
    ├── README.md                 # Frontend docs
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Root component
        ├── components/           # React components
        │   ├── SearchInput.jsx
        │   ├── ResultsList.jsx
        │   └── PriceComparison.jsx
        ├── hooks/                # Custom hooks
        │   └── useSearch.js
        ├── pages/                # Page components
        │   └── SearchPage.jsx
        ├── services/             # API client
        │   └── api.js
        ├── styles/               # Stylesheets
        │   ├── globals.css
        │   ├── components.css
        │   └── index.css
        └── index.css
```

---

## How to Use

### Development Setup (30 minutes)
```bash
# Start services
docker-compose up -d

# Backend
cd backend && python main.py

# Frontend (new terminal)
cd frontend && npm run dev

# Access
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Testing
1. Search for "Beatles" or any artist
2. View results with cover art
3. Expand to see prices from all stores
4. Click "Buy" to go to store product page

### Triggering Scrape
```bash
curl -X POST http://localhost:8000/api/stores/trigger-scrape
```

---

## Performance Targets

- **Search Latency**: < 100ms (typical queries)
- **API Response**: < 300ms (99th percentile)
- **Frontend Bundle**: < 100KB gzipped
- **Database Queries**: < 50ms with indexes

---

## Next Steps (Phase 2)

See Phase 2 plan in `/memories/session/plan.md`:
1. Add scrapers for 5 WooCommerce stores
2. Add scrapers for 3 custom platform stores
3. Investigate problematic stores
4. Scale scheduler to all 12 stores
5. **Target**: 8,000+ total products

---

## Deployment Path

1. **Phase 1 (Current)**: MVP complete
2. **Testing**: Local testing, fix any issues
3. **Phase 2**: Scale to all 12 stores
4. **Phase 3**: Optimization & Polish
5. **Production**: Deploy to Railway (backend) + Vercel (frontend)

---

## Known Limitations (MVP)

- Only 2 stores (out of 12 planned)
- Basic full-text search (no advanced filters yet)
- No user accounts/wishlists
- No price history
- No email alerts
- Scheduled scraping only (not real-time)

These are intentionally excluded for Phase 1 to keep scope manageable and validate core functionality first.

---

## Key Statistics

| Metric | Value |
|--------|-------|
| **Backend Files**: | 14 |
| **Frontend Files**: | 16 |
| **Database Tables**: | 3 |
| **API Endpoints**: | 7 |
| **Components**: | 3 |
| **Hooks**: | 1 |
| **Scrapers**: | 2 |
| **Services**: | 2 |
| **Total Lines of Code**: | ~1500 |
| **Time to MVP**: | ~12 hours |

---

## Support & Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

### Deployment
- Railway: https://railway.app/
- Vercel: https://vercel.com/

### Development
- Vite: https://vitejs.dev/
- Axios: https://axios-http.com/
- SQLAlchemy: https://www.sqlalchemy.org/

---

**Status**: ✅ MVP Ready for Testing  
**Last Updated**: 2026-03-28  
**Next Milestone**: Phase 2 - Scale to all 12 stores

