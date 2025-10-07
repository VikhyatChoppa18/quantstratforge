# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Proprietary License. See LICENSE file for details.

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from quantstratforge import DataFetcher, StrategyGenerator, Backtester, Optimizer

class TestDataFetcher:
    """Test cases for DataFetcher class"""
    
    def test_init(self):
        """Test DataFetcher initialization"""
        fetcher = DataFetcher()
        assert fetcher.dataset == "financial_phrasebank"
        assert fetcher.split == "sentences_allagree"
        assert fetcher.synthetic_count == 200
        assert fetcher.final_dataset is None
    
    def test_get_time_series(self):
        """Test time series data fetching"""
        fetcher = DataFetcher()
        # Mock yfinance to avoid actual API calls in tests
        with patch('quantstratforge.data_prep.yfi.download') as mock_download:
            mock_data = pd.DataFrame({
                'Close': np.random.randn(100).cumsum() + 100,
                'Open': np.random.randn(100).cumsum() + 100,
                'High': np.random.randn(100).cumsum() + 105,
                'Low': np.random.randn(100).cumsum() + 95,
                'Volume': np.random.randint(1000, 10000, 100)
            })
            mock_download.return_value = mock_data
            
            result = fetcher.get_time_series("AAPL")
            assert isinstance(result, str)
            assert "Close" in result
    
    def test_generate_synthetic_strategy(self):
        """Test synthetic strategy generation"""
        fetcher = DataFetcher()
        
        # Test low risk strategy
        result = fetcher.generate_synthetic_strategy("low")
        assert result["risk"] == "low"
        assert "def low_risk_strategy" in result["code"]
        assert "mean-reversion" in result["explanation"]
        
        # Test medium risk strategy
        result = fetcher.generate_synthetic_strategy("medium")
        assert result["risk"] == "medium"
        assert "def medium_strategy" in result["code"]
        assert "momentum" in result["explanation"]
        
        # Test high risk strategy
        result = fetcher.generate_synthetic_strategy("high")
        assert result["risk"] == "high"
        assert "def high_strategy" in result["code"]
        assert "HFT" in result["explanation"]

class TestStrategyGenerator:
    """Test cases for StrategyGenerator class"""
    
    @patch('quantstratforge.generator.pipeline')
    def test_init(self, mock_pipeline):
        """Test StrategyGenerator initialization"""
        mock_pipeline.return_value = Mock()
        generator = StrategyGenerator()
        assert generator.generator is not None
    
    @patch('quantstratforge.generator.pipeline')
    def test_generate(self, mock_pipeline):
        """Test strategy generation"""
        mock_generator = Mock()
        mock_generator.return_value = [{"generated_text": "Strategy Code: def strategy_func(df):\n    return pd.Series([1] * len(df))\nOptimization Explanation: Test explanation"}]
        mock_pipeline.return_value = mock_generator
        
        generator = StrategyGenerator()
        result = generator.generate("test input")
        
        assert "strategy_code" in result
        assert "explanation" in result
        assert "[WM:" in result["explanation"]  # Check watermark

class TestBacktester:
    """Test cases for Backtester class"""
    
    def test_init(self):
        """Test Backtester initialization"""
        backtester = Backtester()
        assert backtester.ticker == "AAPL"
        assert backtester.period == "1y"
        assert backtester.data is None
    
    @patch('quantstratforge.backtester.yf.download')
    def test_fetch_data(self, mock_download):
        """Test data fetching"""
        mock_data = pd.DataFrame({
            'Close': np.random.randn(100).cumsum() + 100,
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        mock_download.return_value = mock_data
        
        backtester = Backtester()
        result = backtester.fetch_data()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 100
        assert backtester.data is not None
    
    def test_normalize_signals(self):
        """Test signal normalization"""
        backtester = Backtester()
        
        # Test boolean signals
        bool_signals = pd.Series([True, False, True])
        normalized = backtester.normalize_signals(bool_signals)
        assert all(normalized == [1, 0, 1])
        
        # Test string signals
        str_signals = pd.Series(['Buy', 'Sell', 'Buy'])
        normalized = backtester.normalize_signals(str_signals)
        assert all(normalized == [1, 0, 1])
    
    @patch('quantstratforge.backtester.yf.download')
    def test_backtest(self, mock_download):
        """Test backtesting functionality"""
        # Create mock data
        mock_data = pd.DataFrame({
            'Close': np.random.randn(100).cumsum() + 100,
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        mock_download.return_value = mock_data
        
        backtester = Backtester()
        
        # Define a simple strategy
        strategy_code = """def strategy_func(df):
    return pd.Series([1] * len(df))"""
        
        result = backtester.backtest(strategy_code)
        
        assert "sharpe_ratio" in result
        assert "cum_returns" in result
        assert isinstance(result["sharpe_ratio"], (int, float))
        assert isinstance(result["cum_returns"], (int, float))

class TestOptimizer:
    """Test cases for Optimizer class"""
    
    def test_init(self):
        """Test Optimizer initialization"""
        mock_backtester = Mock()
        optimizer = Optimizer(mock_backtester)
        assert optimizer.backtester == mock_backtester
    
    @patch('quantstratforge.backtester.yf.download')
    def test_optimize(self, mock_download):
        """Test optimization functionality"""
        # Create mock data
        mock_data = pd.DataFrame({
            'Close': np.random.randn(100).cumsum() + 100,
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        mock_download.return_value = mock_data
        
        backtester = Backtester()
        optimizer = Optimizer(backtester)
        
        # Define parameterized strategy
        strategy_code = """def strategy_func(df):
    threshold = {threshold}
    return pd.Series([threshold] * len(df))"""
        
        params = {"threshold": [0.01, 0.02, 0.03]}
        
        result = optimizer.optimize(strategy_code, params)
        
        assert "best_params" in result
        assert "best_sharpe" in result
        assert "explanation" in result
        assert isinstance(result["best_params"], dict)
        assert isinstance(result["best_sharpe"], (int, float))

class TestIntegration:
    """Integration tests"""
    
    @patch('quantstratforge.generator.pipeline')
    @patch('quantstratforge.backtester.yf.download')
    def test_full_workflow(self, mock_download, mock_pipeline):
        """Test complete workflow from data fetching to optimization"""
        # Setup mocks
        mock_data = pd.DataFrame({
            'Close': np.random.randn(100).cumsum() + 100,
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        mock_download.return_value = mock_data
        
        mock_generator = Mock()
        mock_generator.return_value = [{"generated_text": "Strategy Code: def strategy_func(df):\n    return pd.Series([1] * len(df))\nOptimization Explanation: Test explanation"}]
        mock_pipeline.return_value = mock_generator
        
        # Test workflow
        fetcher = DataFetcher()
        generator = StrategyGenerator()
        backtester = Backtester()
        optimizer = Optimizer(backtester)
        
        # Generate strategy
        strategy_result = generator.generate("test input")
        assert "strategy_code" in strategy_result
        
        # Run backtest
        backtest_result = backtester.backtest(strategy_result["strategy_code"])
        assert "sharpe_ratio" in backtest_result
        
        # Optimize strategy
        params = {"threshold": [0.01, 0.02]}
        optimization_result = optimizer.optimize(strategy_result["strategy_code"], params)
        assert "best_params" in optimization_result
        
        print("✅ Full workflow test completed successfully!")

if __name__ == "__main__":
    pytest.main([__file__])
