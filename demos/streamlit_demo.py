import streamlit as st
import pandas as pd
import yfinance as yf
from quantstratforge import DataFetcher, StrategyGenerator, Backtester, Optimizer
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="QuantStratForge Demo",
    page_icon="📈",
    layout="wide"
)

if 'market_data' not in st.session_state:
    st.session_state.market_data = None
if 'generated_strategy' not in st.session_state:
    st.session_state.generated_strategy = '''def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(20).mean()
    signals = df['Close'] > df['MA_20']
    return signals.astype(int)'''

st.title("📈 QuantStratForge Demo")
st.markdown("**Privacy-preserving agentic SLM for quant strategy forging**")

st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"], index=0)
risk_level = st.sidebar.selectbox("Risk Level", ["low", "medium", "high"], index=1)
news_sentiment = st.sidebar.text_area("Market News/Sentiment", "Positive market sentiment with strong earnings growth expected.")

@st.cache_resource
def init_components():
    data_fetcher = DataFetcher()
    try:
        generator = StrategyGenerator()
        model_available = True
    except FileNotFoundError:
        generator = None
        model_available = False
    backtester = Backtester(ticker="AAPL")
    return data_fetcher, generator, model_available, backtester

data_fetcher, generator, model_available, backtester = init_components()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Market Data")
    
    if st.button("Fetch Market Data"):
        with st.spinner("Fetching market data..."):
            try:
                data = yf.download(ticker, period="1y")
                
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                
                st.session_state.market_data = data
                
                st.success(f"✅ Data fetched for {ticker}")
                
            except Exception as e:
                st.error(f"❌ Error fetching data: {str(e)}")
    
    if st.session_state.market_data is not None:
        data = st.session_state.market_data
        
        fig = go.Figure(data=go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=ticker
        ))
        
        fig.update_layout(
            title=f"{ticker} Price Chart",
            yaxis_title="Price ($)",
            xaxis_title="Date",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Latest Data")
        st.dataframe(data.tail(10))

with col2:
    st.header("🤖 AI Strategy Generation")
    
    if not model_available:
        st.warning("⚠️ Custom trained model not found. Please train your model first using:\n"
                   "- `quantstratforge prepare` (prepare data)\n"
                   "- `quantstratforge train` (train model)")
        st.info("💡 For demo purposes, you can use the pre-written strategy in the Backtesting section below.")
    
    if st.button("Generate Strategy", disabled=not model_available):
        with st.spinner("Generating AI strategy..."):
            try:
                time_series = data_fetcher.get_time_series(ticker)
                
                input_data = f"Ticker: {ticker}\nRisk Level: {risk_level}\nNews: {news_sentiment}\nTime Series: {time_series}"
                result = generator.generate(input_data)
                
                st.session_state.generated_strategy = result["strategy_code"]
                
                st.subheader("Generated Strategy Code")
                st.code(result["strategy_code"], language="python")
                
                st.subheader("AI Explanation")
                st.info(result["explanation"])
                
                st.success("✅ Strategy generated successfully! Code auto-populated in Backtesting section below.")
                
            except Exception as e:
                st.error(f"❌ Error generating strategy: {str(e)}")

st.header("🔬 Strategy Backtesting")

st.subheader("📚 Example Strategies")
example_strategies = {
    "Current/Generated": st.session_state.generated_strategy,
    "Simple Moving Average (MA)": """def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    signals = (df['MA_20'] > df['MA_50']).astype(int)
    return signals""",
    "RSI Momentum": """def strategy_func(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    signals = (df['RSI'] < 30).astype(int)
    return signals""",
    "Bollinger Bands": """def strategy_func(df):
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['STD_20'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['MA_20'] + (df['STD_20'] * 2)
    df['Lower_Band'] = df['MA_20'] - (df['STD_20'] * 2)
    signals = (df['Close'] <= df['Lower_Band']).astype(int)
    return signals""",
    "MACD Strategy": """def strategy_func(df):
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    signals = (df['MACD'] > df['Signal']).astype(int)
    return signals"""
}

selected_example = st.selectbox(
    "Choose an example strategy or use the generated one:",
    options=list(example_strategies.keys()),
    index=0
)

strategy_code_input = st.text_area(
    "Strategy Code (edit as needed)",
    value=example_strategies[selected_example],
    height=200,
    key="strategy_code_area"
)

if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        try:
            backtester_for_test = Backtester(ticker=ticker, period="1y")
            results = backtester_for_test.backtest(strategy_code_input)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sharpe Ratio", f"{results['sharpe_ratio']:.3f}")
            
            with col2:
                st.metric("Cumulative Returns", f"{results['cum_returns']:.3f}")
            
            with col3:
                performance = "🟢 Good" if results['sharpe_ratio'] > 1.0 else "🟡 Moderate" if results['sharpe_ratio'] > 0.5 else "🔴 Poor"
                st.metric("Performance", performance)
            
            st.success("✅ Backtest completed!")
            
        except Exception as e:
            st.error(f"❌ Error running backtest: {str(e)}")

st.header("⚡ Strategy Optimization")

if st.button("Optimize Strategy"):
    with st.spinner("Optimizing strategy..."):
        try:
            backtester_for_opt = Backtester(ticker=ticker, period="1y")
            
            params = {
                "threshold": [0.01, 0.02, 0.03, 0.04, 0.05],
                "period": [10, 15, 20, 25, 30]
            }
            
            optimizer = Optimizer(backtester_for_opt)
            optimization_results = optimizer.optimize(strategy_code_input, params)
            
            st.subheader("Optimization Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Best Parameters:**")
                for param, value in optimization_results["best_params"].items():
                    st.write(f"- {param}: {value}")
            
            with col2:
                st.metric("Best Sharpe Ratio", f"{optimization_results['best_sharpe']:.3f}")
            
            st.info(f"**Explanation:** {optimization_results['explanation']}")
            
            st.success("✅ Optimization completed!")
            
        except Exception as e:
            st.error(f"❌ Error optimizing strategy: {str(e)}")

st.markdown("---")
st.markdown("**QuantStratForge** - Privacy-preserving AI for quantitative strategy development")
st.markdown("For licensing inquiries, contact: Venkata Vikhyat Choppa <vikhyathchoppa699@gmail.com>")
