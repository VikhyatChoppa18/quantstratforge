# 🎪 QuantStratForge Demo Instructions

This guide provides step-by-step instructions for running and demonstrating QuantStratForge's various interfaces.

## 🚀 Quick Demo Setup

### Prerequisites
- Python 3.12+
- pip or poetry
- Internet connection (for market data)

### Installation
```bash
# Install QuantStratForge with demo dependencies
pip install quantstratforge[demo]

# Or using poetry
poetry install --with demo
```

## 🖥️ Demo Options

### 1. Streamlit Web App (Recommended for Live Demos)

**Best for**: Interactive presentations, live coding sessions, user demonstrations

```bash
# Run Streamlit demo
streamlit run demos/streamlit_demo.py
```

**Features**:
- Interactive web interface
- Real-time market data fetching
- Visual strategy generation
- Live backtesting with charts
- Parameter optimization
- Beautiful UI with metrics

**Demo Flow**:
1. Open browser to `http://localhost:8501`
2. Select ticker (AAPL, GOOGL, MSFT, etc.)
3. Choose risk level (low, medium, high)
4. Enter market sentiment/news
5. Click "Generate Strategy" to see AI in action
6. Run backtest to see performance metrics
7. Optimize parameters for better returns

### 2. FastAPI REST API

**Best for**: Technical demonstrations, API integrations, developer showcases

```bash
# Run FastAPI demo
python demos/fastapi_demo.py
```

**Features**:
- RESTful API endpoints
- Interactive API documentation (Swagger UI)
- JSON request/response format
- Rate limiting demonstration
- Health check endpoints

**Demo Flow**:
1. Open browser to `http://localhost:8000`
2. Visit `/docs` for interactive API documentation
3. Test endpoints using the Swagger UI
4. Show API responses and error handling
5. Demonstrate rate limiting and authentication

**Key Endpoints**:
- `GET /` - Main demo page
- `POST /api/market-data` - Fetch market data
- `POST /api/generate-strategy` - Generate AI strategy
- `POST /api/backtest` - Run strategy backtest
- `POST /api/optimize` - Optimize strategy parameters
- `GET /health` - Health check

### 3. Command Line Interface

**Best for**: Terminal demonstrations, automation scripts, batch processing

```bash
# Show CLI help
quantstratforge --help

# Prepare data
quantstratforge prepare

# Generate strategy
quantstratforge generate --ticker AAPL --news "Strong earnings expected"

# Backtest strategy
quantstratforge backtest --strategy_code "def strategy_func(df): return df['Close'] > df['Close'].rolling(20).mean()"

# Optimize parameters
quantstratforge optimize --strategy_code "..." --params '{"threshold": [0.01, 0.02, 0.03]}'
```

## 🎯 Demo Scripts

### 5-Minute Quick Demo

```bash
#!/bin/bash
# Quick demo script

echo "🚀 QuantStratForge Quick Demo"
echo "=============================="

# 1. Show CLI help
echo "1. CLI Interface:"
quantstratforge --help

# 2. Generate a strategy
echo "2. Generating AI Strategy:"
quantstratforge generate --ticker AAPL --news "Positive market sentiment with strong earnings growth expected"

# 3. Run backtest
echo "3. Running Backtest:"
quantstratforge backtest --strategy_code "def strategy_func(df): return df['Close'] > df['Close'].rolling(20).mean()"

echo "✅ Demo completed!"
```

### 15-Minute Comprehensive Demo

1. **Introduction** (2 minutes)
   - Explain privacy-preserving AI concept
   - Show federated learning benefits
   - Highlight key differentiators

2. **Streamlit Demo** (5 minutes)
   - Fetch live market data
   - Generate AI strategy
   - Run backtest with visualizations
   - Optimize parameters

3. **API Demo** (3 minutes)
   - Show REST API documentation
   - Test endpoints programmatically
   - Demonstrate error handling

4. **CLI Demo** (3 minutes)
   - Show command-line interface
   - Demonstrate automation capabilities
   - Show batch processing

5. **Q&A** (2 minutes)
   - Answer technical questions
   - Discuss use cases
   - Explain pricing/licensing

## 🎨 Demo Customization

### Custom Tickers
Modify demo to use different stocks:

```python
# In streamlit_demo.py
ticker = st.sidebar.selectbox("Select Ticker", 
    ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN", "META"], 
    index=0)
```

### Custom Strategies
Add your own strategy templates:

```python
# In fastapi_demo.py
CUSTOM_STRATEGIES = {
    "momentum": "def strategy_func(df): return df['Close'] > df['Close'].rolling(10).mean()",
    "mean_reversion": "def strategy_func(df): return df['Close'] < df['Close'].rolling(20).mean()",
    "rsi_oversold": "def strategy_func(df): return calculate_rsi(df['Close']) < 30"
}
```

### Custom Parameters
Adjust optimization parameters:

```python
# In optimizer.py
OPTIMIZATION_PARAMS = {
    "short_period": [5, 10, 15, 20],
    "long_period": [25, 30, 35, 40],
    "threshold": [0.01, 0.02, 0.03, 0.04, 0.05]
}
```

## 📊 Demo Metrics

### Key Performance Indicators
- **Strategy Generation Time**: < 5 seconds
- **Backtest Execution Time**: < 10 seconds
- **Parameter Optimization**: < 30 seconds
- **API Response Time**: < 2 seconds
- **UI Load Time**: < 3 seconds

### Success Metrics
- **User Engagement**: Time spent on demo
- **Conversion Rate**: Demo to signup ratio
- **Technical Interest**: API usage patterns
- **Feedback Quality**: User questions and comments

## 🛠️ Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find and kill process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run demos/streamlit_demo.py --server.port 8502
```

**2. Missing Dependencies**
```bash
# Install missing dependencies
pip install quantstratforge[demo]

# Or install individually
pip install streamlit plotly seaborn matplotlib
```

**3. Market Data Issues**
```bash
# Test data fetching
python -c "from quantstratforge import DataFetcher; print(DataFetcher().get_time_series('AAPL'))"
```

**4. Model Loading Issues**
```bash
# Check model path
ls -la ./quant-strat-forge/

# Download model if missing
python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2')"
```

### Performance Optimization

**1. Reduce Model Size**
```python
# Use smaller model for faster demos
generator = StrategyGenerator(model_path="gpt2")
```

**2. Limit Data Size**
```python
# Reduce data points for faster processing
data = yf.download(ticker, period="6mo")  # Instead of "1y"
```

**3. Cache Results**
```python
# Use Streamlit caching
@st.cache_data
def fetch_market_data(ticker):
    return DataFetcher().get_time_series(ticker)
```

## 🎬 Demo Recording

### Screen Recording Setup
- **Resolution**: 1920x1080
- **Frame Rate**: 30 FPS
- **Audio**: Clear microphone
- **Duration**: 5-15 minutes

### Recording Tips
1. **Prepare Script**: Write demo script beforehand
2. **Test Everything**: Ensure all features work
3. **Clear Audio**: Use good microphone
4. **Stable Connection**: Ensure reliable internet
5. **Backup Plan**: Have offline demo ready

### Post-Production
- Add captions for accessibility
- Include call-to-action at end
- Optimize for social media formats
- Create thumbnail with key benefits

## 📱 Social Media Demos

### Twitter/X Thread
1. **Tweet 1**: Announcement with demo link
2. **Tweet 2**: Privacy benefits explanation
3. **Tweet 3**: Technical capabilities
4. **Tweet 4**: Use cases and examples
5. **Tweet 5**: Call-to-action

### LinkedIn Post
- Professional tone
- Technical depth
- Business value focus
- Include demo video
- Tag relevant professionals

### YouTube Video
- **Title**: "QuantStratForge: Privacy-Preserving AI for Trading"
- **Description**: Comprehensive overview with timestamps
- **Thumbnail**: Eye-catching with key benefits
- **Tags**: #QuantTrading #AI #Privacy #FinTech

## 🎯 Demo Success Tips

### Before the Demo
- [ ] Test all features thoroughly
- [ ] Prepare backup plans
- [ ] Know your audience
- [ ] Practice the script
- [ ] Check internet connection

### During the Demo
- [ ] Start with value proposition
- [ ] Show real-time data
- [ ] Explain privacy benefits
- [ ] Demonstrate AI capabilities
- [ ] Answer questions clearly

### After the Demo
- [ ] Collect feedback
- [ ] Follow up with interested users
- [ ] Share demo recording
- [ ] Update based on feedback
- [ ] Plan next improvements

---

**Ready to demo QuantStratForge? Choose your interface and start showcasing the future of privacy-preserving quantitative trading! 🚀**
