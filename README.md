# Israeli Vinyl Record Aggregator

Centralized search platform for Israeli vinyl record market with automated web scraping, unified database indexing, and fast price comparison across 12 local stores.

## Features

✅ **Multi-Store Scraping**: Aggregates products from 12 Israeli vinyl record stores  
✅ **Real-Time Search**: Full-text search across artist, album, and title  
✅ **Price Comparison**: View prices from all stores in a single interface  
✅ **Stock Status**: Check availability across stores  
✅ **Direct Purchase**: One-click redirect to store product page  
✅ **Responsive Design**: Works on desktop, tablet, and mobile  

## Tech Stack

- **Backend**: FastAPI (Python) + PostgreSQL + Redis
- **Frontend**: React + Vite
- **Hosting**: Railway (backend) + Vercel (frontend)
- **Scraping**: BeautifulSoup + Requests
- **Scheduling**: APScheduler

## Integrated Stores

1. DiscCenter (disccenter.co.il)
2. The Vinyl Room (thevinylroom.co.il)
3. The Third Ear (third-ear.com)
4. Beatnik (beatnik.co.il)
5. Shablool Records (shabloolrecords.co.il)
6. Tav8 (tav8.co.il)
7. Giora Records (giorarecords.co.il)
8. Has Ivoov (hasivoov.co.il)
9. Vinyl Stock (vinylstock.co.il)
10. Takli House (taklithouse.com)
11. My Records (my-records.co.il)
12. Rollin Daise (rollindaise.com)

## Quick Start

### Prerequisites
- Docker & Docker Compose (for local development)
- Node.js 18+ (if running frontend without Docker)
- Python 3.11+ (if running backend without Docker)

### Option 1: Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
```

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Make sure PostgreSQL and Redis are running, then:
python main.py
```

Backend API available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend available at: `http://localhost:3000`

## API Endpoints

### Search
- `GET /api/search?q=query` - Search records
- `GET /api/search/autocomplete?q=query` - Get suggestions

### Records
- `GET /api/records/{id}` - Get record details with all prices

### Stores
- `GET /api/stores` - List all stores
- `GET /api/stores/{id}` - Get store info
- `POST /api/stores/trigger-scrape` - Manually trigger scrape (admin)

### Health
- `GET /health` - Health check

## Database

The system uses PostgreSQL with the following tables:
- `records` - Vinyl record products
- `stores` - Record store information
- `prices` - Price and stock info per record per store

Automatic scraping runs daily at 2 AM IST. Manual scraping can be triggered via `/api/stores/trigger-scrape`.

## Development

### Project Structure

```
backend/
├── main.py              # FastAPI app entry
├── config.py            # Configuration
├── models.py            # Database models & schemas
├── database.py          # Database setup
├── scrapers/            # Store-specific scrapers
├── services/            # Business logic (aggregation, scheduling)
└── routes/              # API endpoints

frontend/
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom hooks
│   ├── pages/           # Page components
│   ├── services/        # API client
│   └── styles/          # CSS styles
└── vite.config.js       # Vite configuration
```

### Adding New Stores

1. Create a new scraper in `backend/scrapers/newstore.py` extending `BaseScraper`
2. Implement the `scrape()` method
3. Add store config to `backend/config.py`
4. Register the scraper in `backend/services/scheduler.py`

Example scraper:

```python
from scrapers.base import BaseScraper

class NewStoreScraper(BaseScraper):
    def __init__(self):
        config = {
            "name": "Store Name",
            "base_url": "https://store.co.il",
            "product_selector": "div.product",
            # ... other selectors
        }
        super().__init__("store_key", "https://store.co.il", config)
    
    def scrape(self):
        products = []
        # Implement scraping logic
        return products
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/vinyl_aggregator
REDIS_URL=redis://localhost:6379
DEBUG=True
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3
RATE_LIMIT_DELAY=2.5
```

## Performance

- **Search latency**: < 100ms for typical queries
- **Database**: PostgreSQL with full-text search indexing
- **Caching**: Redis for frequently accessed records
- **Scraping**: Staggered to avoid hammering stores

## Legal Notice

This tool respects robots.txt and implements rate limiting to avoid overloading store servers. For production use, consider contacting stores for official data partnerships.

## Roadmap

- [x] Phase 1: MVP with 2 stores (DiscCenter, TheVinylRoom)
- [ ] Phase 2: Scale to all 12 stores
- [ ] Phase 3: Search optimization & Polish
- [ ] Phase 4: User accounts & wishlists
- [ ] Price history & trend charts
- [ ] Email alerts for price drops
- [ ] Advanced filtering & faceted search

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test locally
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

Issues & questions? Please open an issue or reach out.

---

**Status**: 🚀 MVP Development - Phase 1 in progress

