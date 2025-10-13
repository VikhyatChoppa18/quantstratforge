# 🎥 QuantStratForge Demo Recording Guide

## Prerequisites Check
✅ Model trained: `quant-strat-forge/` exists (155MB)
✅ Tests passing: 40/42 tests pass
✅ All demos ready in `demos/` folder

---

## 🎬 Demo 1: FastAPI Demo (~5 minutes)

### Start FastAPI Server:
```bash
cd demos
python fastapi_demo.py
```

### What to Show:
1. **Swagger UI**: Open http://localhost:8000/docs
2. **Endpoints to demonstrate:**
   - `GET /` - Welcome message
   - `GET /health` - Health check
   - `POST /backtest` - Run a backtest with sample data
   - `POST /optimize` - Optimize strategy parameters
   - `POST /generate-strategy` - Generate AI strategy (uses trained model!)

### Sample API Call (in browser or Postman):
```json
POST http://localhost:8000/backtest
{
  "ticker": "AAPL",
  "period": "1y",
  "strategy_code": "def strategy_func(df): return pd.Series([1] * len(df))"
}
```

**Stop server**: Ctrl+C

---

## 🎬 Demo 2: Streamlit App (~5 minutes)

### Start Streamlit:
```bash
cd demos
streamlit run streamlit_demo.py
```

### What to Show:
1. **Beautiful UI** opens at http://localhost:8501
2. **Features to demonstrate:**
   - Data Fetcher: Fetch real market data
   - Strategy Generator: Generate strategies with AI
   - Backtester: Test strategy performance
   - Optimizer: Optimize parameters
   - Interactive charts and results

### Sample Inputs:
- Ticker: AAPL, MSFT, or GOOGL
- Period: 1y
- Strategy: Let AI generate or use simple moving average

**Stop app**: Ctrl+C

---

## 🎬 Demo 3: Jupyter Notebook (~3 minutes)

### Start Jupyter:
```bash
cd demos
jupyter notebook notebook_demo.ipynb
```

### What to Show:
1. **Notebook opens** in browser
2. **Run all cells** (Cell → Run All)
3. **Demonstrate:**
   - Data fetching
   - Strategy generation
   - Backtesting with visualizations
   - Results and metrics

---

## 🎬 Demo 4: Testing (~3 minutes)

### Run Tests:
```bash
cd /home/v/PycharmProjects/YadVansh/StratForge
pytest tests/ -v
```

### What to Show:
1. **40 tests passing** ✅
2. **Test coverage:**
   - Unit tests
   - Integration tests
   - FastAPI endpoint tests
   - Notebook validation tests
   - Streamlit syntax tests

### Show Test Details:
```bash
pytest tests/ -v --tb=short
```

---

## 🎯 Complete Demo Flow (15-20 minutes)

### 1. Introduction (1 min)
"QuantStratForge - Privacy-preserving AI for quantitative strategy development"

### 2. FastAPI Demo (5 min)
Show REST API capabilities

### 3. Streamlit Demo (5 min)
Show interactive web UI

### 4. Jupyter Notebook (3 min)
Show data science workflow

### 5. Testing (3 min)
Show quality assurance

### 6. Conclusion (1 min)
Recap features and next steps

---

## 📝 Demo Script Tips

### Opening:
"Hi! Today I'll show you QuantStratForge, a privacy-preserving AI framework for quantitative trading strategy development. It uses a locally-trained language model - no external APIs, your data stays private."

### Key Points to Mention:
- ✅ Locally trained model (155MB Phi-2 based)
- ✅ No external LLM APIs
- ✅ Privacy-first design
- ✅ Multiple interfaces (API, Web, Notebook)
- ✅ Real market data integration
- ✅ Comprehensive testing

### Closing:
"QuantStratForge provides a complete, privacy-preserving solution for AI-powered quantitative strategy development. Thanks for watching!"

---

## 🎥 Recording Setup

### Tools:
- Screen recorder: OBS Studio, QuickTime, or built-in screen recorder
- Audio: Good microphone for narration
- Resolution: 1920×1080 (1080p)

### Before Recording:
```bash
# Make sure everything is ready
cd /home/v/PycharmProjects/YadVansh/StratForge
pytest tests/ -q  # Quick test check
ls -lh quant-strat-forge/  # Verify model exists
```

### During Recording:
- Clear browser cache/cookies
- Close unnecessary tabs
- Full screen demos
- Smooth mouse movements
- Clear explanations

---

## 🚀 Quick Start All Demos

```bash
# Terminal 1 - FastAPI
cd demos && python fastapi_demo.py

# Terminal 2 - Streamlit
cd demos && streamlit run streamlit_demo.py

# Terminal 3 - Jupyter
cd demos && jupyter notebook notebook_demo.ipynb

# Terminal 4 - Tests
pytest tests/ -v
```

---

Good luck with your demo! 🎬🚀
