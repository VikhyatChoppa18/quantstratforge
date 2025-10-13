from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import json
from quantstratforge import DataFetcher, StrategyGenerator, Backtester, Optimizer

app = FastAPI(
    title="QuantStratForge API",
    description="Privacy-preserving agentic SLM for quant strategy forging",
    version="0.1.0"
)

class MarketDataRequest(BaseModel):
    ticker: str = "AAPL"
    period: str = "1y"

class StrategyRequest(BaseModel):
    ticker: str = "AAPL"
    risk_level: str = "medium"
    news_sentiment: str = "Positive market sentiment"
    time_series_data: Optional[str] = None

class BacktestRequest(BaseModel):
    strategy_code: str
    ticker: str = "AAPL"
    period: str = "1y"

class OptimizationRequest(BaseModel):
    strategy_code: str
    params: Dict[str, list]
    ticker: str = "AAPL"
    period: str = "1y"

data_fetcher = DataFetcher()
try:
    generator = StrategyGenerator()
    MODEL_AVAILABLE = True
except FileNotFoundError:
    generator = None
    MODEL_AVAILABLE = False

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>QuantStratForge Demo</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            button { background-color: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #2980b9; }
            .result { margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 4px; }
            .api-link { color: #3498db; text-decoration: none; }
            .api-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📈 QuantStratForge Demo</h1>
            <p style="text-align: center; color: #7f8c8d;">Privacy-preserving agentic SLM for quant strategy forging</p>
            
            <div class="section">
                <h2>📊 Market Data</h2>
                <div class="form-group">
                    <label for="ticker">Ticker Symbol:</label>
                    <select id="ticker">
                        <option value="AAPL">AAPL</option>
                        <option value="GOOGL">GOOGL</option>
                        <option value="MSFT">MSFT</option>
                        <option value="TSLA">TSLA</option>
                        <option value="NVDA">NVDA</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="period">Period:</label>
                    <select id="period">
                        <option value="1y">1 Year</option>
                        <option value="2y">2 Years</option>
                        <option value="5y">5 Years</option>
                    </select>
                </div>
                <button onclick="fetchMarketData()">Fetch Market Data</button>
                <div id="marketDataResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="section">
                <h2>🤖 AI Strategy Generation</h2>
                <div class="form-group">
                    <label for="strategyTicker">Ticker Symbol:</label>
                    <select id="strategyTicker">
                        <option value="AAPL">AAPL</option>
                        <option value="GOOGL">GOOGL</option>
                        <option value="MSFT">MSFT</option>
                        <option value="TSLA">TSLA</option>
                        <option value="NVDA">NVDA</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="riskLevel">Risk Level:</label>
                    <select id="riskLevel">
                        <option value="low">Low Risk</option>
                        <option value="medium" selected>Medium Risk</option>
                        <option value="high">High Risk</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="newsSentiment">Market News/Sentiment:</label>
                    <textarea id="newsSentiment" rows="3">Positive market sentiment with strong earnings growth expected.</textarea>
                </div>
                <button onclick="generateStrategy()">Generate Strategy</button>
                <div id="strategyResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="section">
                <h2>🔬 Strategy Backtesting</h2>
                <div class="form-group">
                    <label for="strategyCode">Strategy Code:</label>
                    <textarea id="strategyCode" rows="8">def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(20).mean()
    signals = df['Close'] > df['MA_20']
    return signals.astype(int)</textarea>
                </div>
                <div class="form-group">
                    <label for="backtestTicker">Ticker Symbol:</label>
                    <select id="backtestTicker">
                        <option value="AAPL">AAPL</option>
                        <option value="GOOGL">GOOGL</option>
                        <option value="MSFT">MSFT</option>
                        <option value="TSLA">TSLA</option>
                        <option value="NVDA">NVDA</option>
                    </select>
                </div>
                <button onclick="runBacktest()">Run Backtest</button>
                <div id="backtestResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="section">
                <h2>⚡ Strategy Optimization</h2>
                <div class="form-group">
                    <label for="optimizationCode">Strategy Code:</label>
                    <textarea id="optimizationCode" rows="8">def strategy_func(df):
    threshold = {threshold}
    period = {period}
    df['MA'] = df['Close'].rolling(period).mean()
    signals = df['Close'] > df['MA'] * (1 + threshold)
    return signals.astype(int)</textarea>
                </div>
                <button onclick="optimizeStrategy()">Optimize Strategy</button>
                <div id="optimizationResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="section">
                <h2>📚 API Documentation</h2>
                <p>Access the interactive API documentation:</p>
                <p><a href="/docs" class="api-link">📖 Swagger UI</a> | <a href="/redoc" class="api-link">📋 ReDoc</a></p>
            </div>
        </div>
        
        <script>
            async function fetchMarketData() {
                const ticker = document.getElementById('ticker').value;
                const period = document.getElementById('period').value;
                
                try {
                    const response = await fetch('/api/market-data', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ticker, period})
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('marketDataResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<h3>Market Data Result:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function generateStrategy() {
                const ticker = document.getElementById('strategyTicker').value;
                const riskLevel = document.getElementById('riskLevel').value;
                const newsSentiment = document.getElementById('newsSentiment').value;
                
                try {
                    const response = await fetch('/api/generate-strategy', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ticker, risk_level: riskLevel, news_sentiment: newsSentiment})
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('strategyResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<h3>Generated Strategy:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function runBacktest() {
                const strategyCode = document.getElementById('strategyCode').value;
                const ticker = document.getElementById('backtestTicker').value;
                
                try {
                    const response = await fetch('/api/backtest', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({strategy_code: strategyCode, ticker})
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('backtestResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<h3>Backtest Results:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function optimizeStrategy() {
                const strategyCode = document.getElementById('optimizationCode').value;
                
                const params = {
                    "threshold": [0.01, 0.02, 0.03, 0.04, 0.05],
                    "period": [10, 15, 20, 25, 30]
                };
                
                try {
                    const response = await fetch('/api/optimize', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({strategy_code: strategyCode, params})
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('optimizationResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<h3>Optimization Results:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/market-data")
async def get_market_data(request: MarketDataRequest):
    try:
        data = data_fetcher.get_time_series(request.ticker)
        return {"ticker": request.ticker, "data": data, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-strategy")
async def generate_strategy(request: StrategyRequest):
    if not MODEL_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Model not available. Please train the model first using 'quantstratforge prepare' and 'quantstratforge train'"
        )
    
    try:
        time_series = data_fetcher.get_time_series(request.ticker)
        
        input_data = f"Ticker: {request.ticker}\nRisk Level: {request.risk_level}\nNews: {request.news_sentiment}\nTime Series: {time_series}"
        result = generator.generate(input_data)
        
        return {
            "ticker": request.ticker,
            "risk_level": request.risk_level,
            "strategy_code": result["strategy_code"],
            "explanation": result["explanation"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/backtest")
async def run_backtest(request: BacktestRequest):
    try:
        backtester = Backtester(ticker=request.ticker, period=request.period)
        results = backtester.backtest(request.strategy_code)
        
        return {
            "ticker": request.ticker,
            "sharpe_ratio": results["sharpe_ratio"],
            "cum_returns": results["cum_returns"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
async def optimize_strategy(request: OptimizationRequest):
    try:
        backtester = Backtester(ticker=request.ticker, period=request.period)
        optimizer = Optimizer(backtester)
        results = optimizer.optimize(request.strategy_code, request.params)
        
        return {
            "ticker": request.ticker,
            "best_params": results["best_params"],
            "best_sharpe": results["best_sharpe"],
            "explanation": results["explanation"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "QuantStratForge API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
