
# Release Notes
 pypi using [poetry 
 
 +]
## v0.1.0 (Initial Release) - October 2024

### 🎉 What's New

**QuantStratForge** - The first privacy-preserving agentic SLM for quantitative strategy forging is now available on PyPI!

### ✨ Key Features

- **🤖 AI Strategy Generation**: Generate trading strategies using advanced language models (Mistral-7B-Instruct-v0.2)
- **🔒 Privacy-Preserving**: Federated learning ensures your data never leaves your machine
- **📊 Comprehensive Backtesting**: Built-in backtesting engine with Sharpe ratio and performance metrics
- **⚡ Strategy Optimization**: Automated parameter optimization for maximum returns
- **🌐 Multiple Interfaces**: CLI, Streamlit web app, and FastAPI REST API
- **📈 Real-time Data**: Integration with Yahoo Finance for live market data
- **🎯 Risk Management**: Built-in risk assessment and portfolio optimization

### 🚀 Quick Start

```bash
# Install from PyPI
pip install quantstratforge

# Try the CLI
quantstratforge --help

# Generate a strategy for AAPL
quantstratforge generate --ticker AAPL --news "Positive earnings outlook"
```

### 💻 Python API Example

```python
from quantstratforge import DataFetcher, StrategyGenerator, Backtester, Optimizer

# 1. Fetch market data
fetcher = DataFetcher()
data = fetcher.get_time_series("AAPL")

# 2. Generate AI strategy
generator = StrategyGenerator()
strategy = generator.generate(f"Market data for AAPL: {data}")

# 3. Backtest strategy
backtester = Backtester(ticker="AAPL")
results = backtester.backtest(strategy["strategy_code"])

# 4. Optimize parameters
optimizer = Optimizer(backtester)
optimized = optimizer.optimize(strategy["strategy_code"], {
    "threshold": [0.01, 0.02, 0.03],
    "period": [10, 15, 20]
})

print(f"Sharpe Ratio: {results['sharpe_ratio']:.3f}")
print(f"Best Parameters: {optimized['best_params']}")
```

### 🖥️ Demo Applications

#### Streamlit Web App
```bash
pip install quantstratforge[demo]
streamlit run demos/streamlit_demo.py
```

#### FastAPI REST API
```bash
python demos/fastapi_demo.py
# Visit http://localhost:8000/docs for API documentation
```

### 🏗️ Architecture

- **DataFetcher**: Market data acquisition and preprocessing with pandas-ta indicators
- **StrategyModel**: AI model training with local and federated learning support
- **StrategyGenerator**: Strategy generation using pre-trained language models
- **Backtester**: Strategy execution and performance analysis
- **Optimizer**: Parameter optimization for maximum returns

### 🔒 Privacy & Security

- **Local Processing**: All sensitive data stays on your machine
- **Federated Learning**: Models trained without sharing raw data using Flower framework
- **Encryption**: All communications encrypted in transit
- **Compliance**: GDPR, SOX, and PCI DSS ready

### 📊 Supported Features

- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages (via pandas-ta)
- **Market Data**: Yahoo Finance integration for real-time data
- **Strategy Types**: Momentum, Mean Reversion, Arbitrage, ML-based strategies
- **Risk Metrics**: Sharpe ratio, maximum drawdown, volatility analysis
- **Optimization**: Grid search, parameter sensitivity analysis

### 🧪 Testing

Comprehensive test suite included:
- Unit tests for all core modules
- Integration tests for full workflows
- Mock data for testing without external dependencies

```bash
# Run tests
pip install quantstratforge[dev]
pytest tests/ -v
```

### 📚 Documentation

- [Complete README](https://github.com/vikhyatchoppa/quantstratforge#readme)
- [API Reference](https://github.com/vikhyatchoppa/quantstratforge#api-reference)
- [Demo Instructions](https://github.com/vikhyatchoppa/quantstratforge/blob/main/DEMO_INSTRUCTIONS.md)


### 🤝 Contributing

We welcome contributions! The project is open source and community-driven.

- **Issues**: Report bugs or request features
- **Pull Requests**: Submit improvements
- **Documentation**: Help improve docs
- **Testing**: Add more test cases

### 📄 License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

### 🆘 Support

- **GitHub Issues**: [Report bugs or ask questions](https://github.com/vikhyatchoppa/quantstratforge/issues)
- **Email**: [vikhyathchoppa699@gmail.com](mailto:vikhyathchoppa699@gmail.com)
- **Documentation**: [Full documentation](https://github.com/vikhyatchoppa/quantstratforge#readme)

### 🌟 Acknowledgments

- [Hugging Face](https://huggingface.co/) for transformer models
- [Flower](https://flower.dev/) for federated learning framework
- [Streamlit](https://streamlit.io/) for web application framework
- [FastAPI](https://fastapi.tiangolo.com/) for REST API framework
- [Yahoo Finance](https://finance.yahoo.com/) for market data

---

**Made with ❤️ for the quantitative finance community**

*QuantStratForge - Where AI meets Privacy in Quantitative Trading*

## Installation

```bash
pip install quantstratforge
```

## Links

- **PyPI**: https://pypi.org/project/quantstratforge/
- **GitHub**: https://github.com/vikhyatchoppa/quantstratforge
- **Documentation**: https://github.com/vikhyatchoppa/quantstratforge#readme

---

*For the latest updates and announcements, follow the project on GitHub!*
