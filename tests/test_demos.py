# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Test script for validating demo functionality"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantstratforge import DataFetcher, Backtester, Optimizer


def test_data_fetcher():
    """Test DataFetcher functionality"""
    print("Testing DataFetcher...")
    try:
        fetcher = DataFetcher()
        data = fetcher.get_time_series("AAPL")
        assert data is not None, "Data should not be None"
        assert len(data) > 0, "Data should not be empty"
        print("✅ DataFetcher test passed")
        return True
    except Exception as e:
        print(f"❌ DataFetcher test failed: {e}")
        return False


def test_backtester():
    """Test Backtester functionality"""
    print("\nTesting Backtester...")
    try:
        backtester = Backtester(ticker="AAPL", period="1y")
        
        # Test with simple strategy
        strategy_code = """def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(20).mean()
    signals = df['Close'] > df['MA_20']
    return signals.astype(int)"""
        
        results = backtester.backtest(strategy_code)
        assert "sharpe_ratio" in results, "Results should contain sharpe_ratio"
        assert "cum_returns" in results, "Results should contain cum_returns"
        print(f"  Sharpe Ratio: {results['sharpe_ratio']:.3f}")
        print(f"  Cumulative Returns: {results['cum_returns']:.3f}")
        print("✅ Backtester test passed")
        return True
    except Exception as e:
        print(f"❌ Backtester test failed: {e}")
        return False


def test_optimizer():
    """Test Optimizer functionality"""
    print("\nTesting Optimizer...")
    try:
        backtester = Backtester(ticker="AAPL", period="1y")
        optimizer = Optimizer(backtester)
        
        # Strategy with parameters
        strategy_code = """def strategy_func(df):
    period = {period}
    df['MA'] = df['Close'].rolling(period).mean()
    signals = df['Close'] > df['MA']
    return signals.astype(int)"""
        
        params = {"period": [10, 20, 30]}
        results = optimizer.optimize(strategy_code, params)
        
        assert "best_params" in results, "Results should contain best_params"
        assert "best_sharpe" in results, "Results should contain best_sharpe"
        print(f"  Best Parameters: {results['best_params']}")
        print(f"  Best Sharpe: {results['best_sharpe']:.3f}")
        print("✅ Optimizer test passed")
        return True
    except Exception as e:
        print(f"❌ Optimizer test failed: {e}")
        return False


def test_streamlit_imports():
    """Test if Streamlit demo imports are available"""
    print("\nTesting Streamlit demo imports...")
    try:
        import streamlit
        import plotly.graph_objects
        import yfinance
        print("✅ Streamlit demo imports test passed")
        return True
    except ImportError as e:
        print(f"❌ Streamlit demo imports test failed: {e}")
        return False


def test_fastapi_imports():
    """Test if FastAPI demo imports are available"""
    print("\nTesting FastAPI demo imports...")
    try:
        import fastapi
        import uvicorn
        from pydantic import BaseModel
        print("✅ FastAPI demo imports test passed")
        return True
    except ImportError as e:
        print(f"❌ FastAPI demo imports test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("QuantStratForge Demo Tests")
    print("=" * 60)
    
    results = []
    results.append(("DataFetcher", test_data_fetcher()))
    results.append(("Backtester", test_backtester()))
    results.append(("Optimizer", test_optimizer()))
    results.append(("Streamlit Imports", test_streamlit_imports()))
    results.append(("FastAPI Imports", test_fastapi_imports()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:<25} {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! Demos are ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


