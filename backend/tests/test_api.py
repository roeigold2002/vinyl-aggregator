"""
Basic integration tests for the Vinyl Aggregator API
Run with: pytest tests/test_api.py
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# These would be run with proper test database setup


class TestSearchEndpoint:
    """Test search functionality"""
    
    def test_search_empty_query(self, client):
        """Search with empty query should fail"""
        response = client.get("/api/search?q=")
        assert response.status_code == 422  # Validation error
    
    def test_search_valid_query(self, client):
        """Valid search should return results"""
        response = client.get("/api/search?q=Beatles")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_pagination(self, client):
        """Search should support pagination"""
        response = client.get("/api/search?q=test&limit=10&offset=0")
        assert response.status_code == 200
        results = response.json()
        assert len(results) <= 10


class TestRecordEndpoint:
    """Test record detail endpoint"""
    
    def test_get_nonexistent_record(self, client):
        """Getting nonexistent record should return 404"""
        response = client.get("/api/records/99999")
        assert response.status_code == 404
    
    def test_get_existing_record(self, client, sample_record_id):
        """Getting existing record should return full details"""
        response = client.get(f"/api/records/{sample_record_id}")
        assert response.status_code == 200
        record = response.json()
        assert record['id'] == sample_record_id
        assert 'prices' in record
        assert isinstance(record['prices'], list)


class TestStoresEndpoint:
    """Test stores listing endpoint"""
    
    def test_list_stores(self, client):
        """List stores should return all active stores"""
        response = client.get("/api/stores")
        assert response.status_code == 200
        stores = response.json()
        assert isinstance(stores, list)
        assert len(stores) >= 2  # At least DiscCenter and TheVinylRoom
    
    def test_get_store(self, client, sample_store_id):
        """Get specific store"""
        response = client.get(f"/api/stores/{sample_store_id}")
        assert response.status_code == 200
        store = response.json()
        assert store['id'] == sample_store_id
        assert 'name' in store


class TestHealthEndpoint:
    """Test health check"""
    
    def test_health_check(self, client):
        """Health check should return 200"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'


# Running these tests:
# 1. Set up test database: TEST_DATABASE_URL in environment
# 2. Run: pytest tests/test_api.py
# 3. Use pytest fixtures for client and sample data
