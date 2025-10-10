# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import streamlit as st
import pandas as pd
import yfinance as yf
from quantstratforge import DataFetcher, StrategyGenerator, Backtester, Optimizer
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="QuantStratForge Demo",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 QuantStratForge Demo")
st.markdown("**Privacy-preserving agentic SLM for quant strategy forging**")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"], index=0)
risk_level = st.sidebar.selectbox("Risk Level", ["low", "medium", "high"], index=1)
news_sentiment = st.sidebar.text_area("Market News/Sentiment", "Positive market sentiment with strong earnings growth expected.")

# Initialize components
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

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Market Data")
    
    # Fetch and display market data
    if st.button("Fetch Market Data"):
        with st.spinner("Fetching market data..."):
            try:
                data = yf.download(ticker, period="1y")
                
                # Create candlestick chart
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
                    xaxis_title="Date"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display latest data
                st.subheader("Latest Data")
                st.dataframe(data.tail(10))
                
                st.success(f"✅ Data fetched for {ticker}")
                
            except Exception as e:
                st.error(f"❌ Error fetching data: {str(e)}")

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
                # Get time series data
                time_series = data_fetcher.get_time_series(ticker)
                
                # Generate strategy
                input_data = f"Ticker: {ticker}\nRisk Level: {risk_level}\nNews: {news_sentiment}\nTime Series: {time_series}"
                result = generator.generate(input_data)
                
                st.subheader("Generated Strategy Code")
                st.code(result["strategy_code"], language="python")
                
                st.subheader("AI Explanation")
                st.info(result["explanation"])
                
                st.success("✅ Strategy generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating strategy: {str(e)}")

# Backtesting section
st.header("🔬 Strategy Backtesting")

strategy_code_input = st.text_area(
    "Enter Strategy Code (or use generated strategy above)",
    '''def strategy_func(df):
    # Simple moving average strategy
    df['MA_20'] = df['Close'].rolling(20).mean()
    signals = df['Close'] > df['MA_20']
    return signals.astype(int)''',
    height=150
)

if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        try:
            # Create backtester with current ticker
            backtester_for_test = Backtester(ticker=ticker, period="1y")
            # Run backtest
            results = backtester_for_test.backtest(strategy_code_input)
            
            # Display results
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

# Optimization section
st.header("⚡ Strategy Optimization")

if st.button("Optimize Strategy"):
    with st.spinner("Optimizing strategy..."):
        try:
            # Create backtester with current ticker
            backtester_for_opt = Backtester(ticker=ticker, period="1y")
            
            # Define optimization parameters
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

# Footer
st.markdown("---")
st.markdown("**QuantStratForge** - Privacy-preserving AI for quantitative strategy development")
st.markdown("For licensing inquiries, contact: Venkata Vikhyat Choppa <vikhyathchoppa699@gmail.com>")
