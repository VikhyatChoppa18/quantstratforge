#!/bin/bash
# QuantStratForge Demo Launcher Script
# Copyright (c) 2025 Venkata Vikhyat Choppa

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         QuantStratForge Demo Launcher                     ║"
echo "║    Privacy-Preserving AI for Quant Strategy Development   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo -e "${YELLOW}Killing process on port $port...${NC}"
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 1
}

# Pre-flight checks
preflight_check() {
    echo -e "${BLUE}Running pre-flight checks...${NC}"
    
    # Check Python version
    python_version=$(python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python version: $python_version"
    
    # Run tests
    echo -e "${BLUE}Testing demo components...${NC}"
    if python tests/test_demos.py > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} All tests passed"
    else
        echo -e "${RED}✗${NC} Some tests failed. Run 'python tests/test_demos.py' for details"
        echo -e "${YELLOW}Continuing anyway...${NC}"
    fi
    
    # Check for required packages
    echo -e "${BLUE}Checking required packages...${NC}"
    python -c "import streamlit; import fastapi; import yfinance" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} All required packages installed"
    else
        echo -e "${RED}✗${NC} Missing packages. Install with:"
        echo "    pip install quantstratforge[demo]"
        exit 1
    fi
    
    echo ""
}

# Streamlit demo
run_streamlit() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}Starting Streamlit Demo${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    
    # Check if port 8501 is already in use
    if check_port 8501; then
        echo -e "${YELLOW}Port 8501 is already in use${NC}"
        read -p "Kill existing process? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill_port 8501
        else
            echo -e "${RED}Cannot start Streamlit on port 8501${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}Starting Streamlit on http://localhost:8501${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    
    streamlit run demos/streamlit_demo.py
}

# FastAPI demo
run_fastapi() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}Starting FastAPI Demo${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    
    # Check if port 8000 is already in use
    if check_port 8000; then
        echo -e "${YELLOW}Port 8000 is already in use${NC}"
        read -p "Kill existing process? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill_port 8000
        else
            echo -e "${RED}Cannot start FastAPI on port 8000${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}Starting FastAPI on http://localhost:8000${NC}"
    echo -e "${GREEN}API Docs: http://localhost:8000/docs${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    
    python demos/fastapi_demo.py
}

# Both demos (in background)
run_both() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}Starting Both Demos${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    
    # Check ports
    if check_port 8501; then
        kill_port 8501
    fi
    if check_port 8000; then
        kill_port 8000
    fi
    
    echo -e "${GREEN}Starting FastAPI in background...${NC}"
    python demos/fastapi_demo.py > /tmp/fastapi_demo.log 2>&1 &
    FASTAPI_PID=$!
    
    sleep 2
    
    echo -e "${GREEN}Starting Streamlit in background...${NC}"
    streamlit run demos/streamlit_demo.py > /tmp/streamlit_demo.log 2>&1 &
    STREAMLIT_PID=$!
    
    sleep 3
    
    echo ""
    echo -e "${GREEN}✓ Both demos running!${NC}"
    echo ""
    echo -e "${BLUE}Streamlit:${NC} http://localhost:8501"
    echo -e "${BLUE}FastAPI:${NC}   http://localhost:8000"
    echo -e "${BLUE}API Docs:${NC}  http://localhost:8000/docs"
    echo ""
    echo -e "${YELLOW}Logs:${NC}"
    echo -e "  Streamlit: /tmp/streamlit_demo.log"
    echo -e "  FastAPI:   /tmp/fastapi_demo.log"
    echo ""
    echo -e "${YELLOW}To stop:${NC}"
    echo "  kill $STREAMLIT_PID $FASTAPI_PID"
    echo ""
    
    # Wait for user interrupt
    trap "kill $STREAMLIT_PID $FASTAPI_PID 2>/dev/null; echo ''; echo 'Demos stopped.'; exit 0" INT TERM
    
    while true; do
        sleep 1
    done
}

# CLI demo
show_cli_help() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}CLI Demo - Available Commands${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${GREEN}Help:${NC}"
    quantstratforge --help
    
    echo ""
    echo -e "${GREEN}Example Commands:${NC}"
    echo ""
    
    echo -e "${YELLOW}1. Prepare training data:${NC}"
    echo "   quantstratforge prepare"
    echo ""
    
    echo -e "${YELLOW}2. Train model locally:${NC}"
    echo "   quantstratforge train"
    echo ""
    
    echo -e "${YELLOW}3. Train with federated learning:${NC}"
    echo "   quantstratforge train --federated --num_clients 3"
    echo ""
    
    echo -e "${YELLOW}4. Generate strategy:${NC}"
    echo "   quantstratforge generate --ticker AAPL --news 'Strong earnings expected'"
    echo ""
    
    echo -e "${YELLOW}5. Backtest strategy:${NC}"
    echo "   quantstratforge backtest --strategy_code 'def strategy_func(df): ...'"
    echo ""
    
    echo -e "${YELLOW}6. Optimize parameters:${NC}"
    echo "   quantstratforge optimize --strategy_code '...' --params '{\"threshold\": [0.01, 0.02]}'"
    echo ""
}

# Test demos
test_demos() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}Running Demo Tests${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""
    
    python tests/test_demos.py
}

# Recording setup
recording_setup() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}Recording Setup${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${YELLOW}Pre-Recording Checklist:${NC}"
    echo "  [ ] Increase terminal font (16-18pt)"
    echo "  [ ] Set browser zoom to 125-150%"
    echo "  [ ] Disable notifications"
    echo "  [ ] Clean desktop"
    echo "  [ ] Set screen resolution to 1920x1080"
    echo "  [ ] Test microphone"
    echo "  [ ] Close unnecessary applications"
    echo ""
    
    echo -e "${YELLOW}Running tests...${NC}"
    python tests/test_demos.py
    echo ""
    
    echo -e "${GREEN}Ready to record!${NC}"
    echo ""
    echo -e "${BLUE}Quick Reference:${NC}"
    echo "  • Streamlit: streamlit run demos/streamlit_demo.py"
    echo "  • FastAPI:   python demos/fastapi_demo.py"
    echo "  • See QUICK_DEMO_REFERENCE.md for talking points"
    echo ""
}

# Show menu
show_menu() {
    echo ""
    echo -e "${BLUE}Choose a demo to run:${NC}"
    echo ""
    echo "  1) Streamlit Web App"
    echo "  2) FastAPI REST API"
    echo "  3) Both (Streamlit + FastAPI)"
    echo "  4) CLI Help"
    echo "  5) Run Tests"
    echo "  6) Recording Setup"
    echo "  0) Exit"
    echo ""
    read -p "Enter choice [0-6]: " choice
    
    case $choice in
        1) run_streamlit ;;
        2) run_fastapi ;;
        3) run_both ;;
        4) show_cli_help ;;
        5) test_demos ;;
        6) recording_setup ;;
        0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}"; show_menu ;;
    esac
}

# Main execution
main() {
    # Run pre-flight checks
    preflight_check
    
    # If arguments provided, run directly
    if [ $# -gt 0 ]; then
        case $1 in
            streamlit) run_streamlit ;;
            fastapi) run_fastapi ;;
            both) run_both ;;
            cli) show_cli_help ;;
            test) test_demos ;;
            record) recording_setup ;;
            *)
                echo -e "${RED}Unknown argument: $1${NC}"
                echo "Usage: $0 [streamlit|fastapi|both|cli|test|record]"
                exit 1
                ;;
        esac
    else
        # Show interactive menu
        show_menu
    fi
}

# Run main
main "$@"


