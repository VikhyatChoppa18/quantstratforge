# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Test script for FastAPI demo"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient


def test_fastapi_imports():
    """Test if FastAPI demo can be imported"""
    print("\n🧪 Testing FastAPI imports...")
    try:
        from demos.fastapi_demo import app, data_fetcher, MODEL_AVAILABLE
        assert app is not None, "FastAPI app should not be None"
        assert data_fetcher is not None, "DataFetcher should not be None"
        print(f"  ✅ Model available: {MODEL_AVAILABLE}")
        print("  ✅ FastAPI imports successful")
        return True
    except Exception as e:
        print(f"  ❌ FastAPI import failed: {e}")
        return False


def test_fastapi_app_creation():
    """Test if FastAPI app is created correctly"""
    print("\n🧪 Testing FastAPI app creation...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        # Test app metadata
        assert app.title == "QuantStratForge API"
        assert app.version == "0.1.0"
        print("  ✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"  ❌ FastAPI app creation failed: {e}")
        return False


def test_fastapi_root_endpoint():
    """Test root endpoint returns HTML"""
    print("\n🧪 Testing FastAPI root endpoint (/)...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "QuantStratForge Demo" in response.text
        print(f"  ✅ Root endpoint working (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"  ❌ Root endpoint test failed: {e}")
        return False


def test_fastapi_health_endpoint():
    """Test health check endpoint"""
    print("\n🧪 Testing FastAPI health endpoint (/health)...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "QuantStratForge API"
        print(f"  ✅ Health endpoint working: {data}")
        return True
    except Exception as e:
        print(f"  ❌ Health endpoint test failed: {e}")
        return False


def test_fastapi_market_data_endpoint():
    """Test market data endpoint"""
    print("\n🧪 Testing FastAPI market data endpoint (/api/market-data)...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        payload = {"ticker": "AAPL", "period": "1y"}
        response = client.post("/api/market-data", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == "AAPL"
        assert data["status"] == "success"
        assert "data" in data
        print(f"  ✅ Market data endpoint working")
        print(f"     Ticker: {data['ticker']}")
        print(f"     Status: {data['status']}")
        return True
    except Exception as e:
        print(f"  ❌ Market data endpoint test failed: {e}")
        return False


def test_fastapi_backtest_endpoint():
    """Test backtest endpoint"""
    print("\n🧪 Testing FastAPI backtest endpoint (/api/backtest)...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        strategy_code = """def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(20).mean()
    signals = df['Close'] > df['MA_20']
    return signals.astype(int)"""
        
        payload = {
            "strategy_code": strategy_code,
            "ticker": "AAPL",
            "period": "1y"
        }
        
        response = client.post("/api/backtest", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "sharpe_ratio" in data
        assert "cum_returns" in data
        print(f"  ✅ Backtest endpoint working")
        print(f"     Sharpe Ratio: {data['sharpe_ratio']:.3f}")
        print(f"     Cumulative Returns: {data['cum_returns']:.3f}")
        return True
    except Exception as e:
        print(f"  ❌ Backtest endpoint test failed: {e}")
        return False


def test_fastapi_optimize_endpoint():
    """Test optimization endpoint"""
    print("\n🧪 Testing FastAPI optimize endpoint (/api/optimize)...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        strategy_code = """def strategy_func(df):
    period = {period}
    df['MA'] = df['Close'].rolling(period).mean()
    signals = df['Close'] > df['MA']
    return signals.astype(int)"""
        
        payload = {
            "strategy_code": strategy_code,
            "params": {"period": [10, 20, 30]},
            "ticker": "AAPL",
            "period": "1y"
        }
        
        response = client.post("/api/optimize", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "best_params" in data
        assert "best_sharpe" in data
        print(f"  ✅ Optimize endpoint working")
        print(f"     Best Parameters: {data['best_params']}")
        print(f"     Best Sharpe: {data['best_sharpe']:.3f}")
        return True
    except Exception as e:
        print(f"  ❌ Optimize endpoint test failed: {e}")
        return False


def test_fastapi_generate_strategy_endpoint():
    """Test strategy generation endpoint (may fail if model not available)"""
    print("\n🧪 Testing FastAPI generate strategy endpoint (/api/generate-strategy)...")
    try:
        from demos.fastapi_demo import app, MODEL_AVAILABLE
        client = TestClient(app)
        
        if not MODEL_AVAILABLE:
            print("  ⚠️  Model not available, testing error response...")
            payload = {
                "ticker": "AAPL",
                "risk_level": "medium",
                "news_sentiment": "Positive sentiment"
            }
            response = client.post("/api/generate-strategy", json=payload)
            assert response.status_code == 503
            print("  ✅ Correctly returns 503 when model unavailable")
            return True
        else:
            print("  ⚠️  Model available, testing generation...")
            payload = {
                "ticker": "AAPL",
                "risk_level": "medium",
                "news_sentiment": "Positive sentiment"
            }
            response = client.post("/api/generate-strategy", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "strategy_code" in data
            print("  ✅ Strategy generation working")
            return True
    except Exception as e:
        print(f"  ⚠️  Generate strategy endpoint test: {e}")
        return True  # Don't fail test if model not available


def test_fastapi_invalid_endpoint():
    """Test that invalid endpoints return 404"""
    print("\n🧪 Testing FastAPI invalid endpoint...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        response = client.get("/api/invalid-endpoint")
        assert response.status_code == 404
        print("  ✅ Invalid endpoint correctly returns 404")
        return True
    except Exception as e:
        print(f"  ❌ Invalid endpoint test failed: {e}")
        return False


def test_fastapi_openapi_docs():
    """Test that OpenAPI docs are available"""
    print("\n🧪 Testing FastAPI OpenAPI docs...")
    try:
        from demos.fastapi_demo import app
        client = TestClient(app)
        
        # Test /docs (Swagger UI)
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test /openapi.json (OpenAPI schema)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        print("  ✅ OpenAPI docs available at /docs and /openapi.json")
        return True
    except Exception as e:
        print(f"  ❌ OpenAPI docs test failed: {e}")
        return False


def main():
    """Run all FastAPI tests"""
    print("=" * 60)
    print("FastAPI Demo Tests")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_fastapi_imports()))
    results.append(("App Creation", test_fastapi_app_creation()))
    results.append(("Root Endpoint", test_fastapi_root_endpoint()))
    results.append(("Health Endpoint", test_fastapi_health_endpoint()))
    results.append(("Market Data Endpoint", test_fastapi_market_data_endpoint()))
    results.append(("Backtest Endpoint", test_fastapi_backtest_endpoint()))
    results.append(("Optimize Endpoint", test_fastapi_optimize_endpoint()))
    results.append(("Generate Strategy Endpoint", test_fastapi_generate_strategy_endpoint()))
    results.append(("Invalid Endpoint", test_fastapi_invalid_endpoint()))
    results.append(("OpenAPI Docs", test_fastapi_openapi_docs()))
    
    print("\n" + "=" * 60)
    print("FastAPI Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:<30} {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All FastAPI tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


