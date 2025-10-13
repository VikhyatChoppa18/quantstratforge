#!/bin/bash
# Quick Demo Starter Script

echo "🎬 QuantStratForge Demo Starter"
echo ""
echo "Choose a demo to run:"
echo ""
echo "1. FastAPI Demo (REST API with Swagger UI)"
echo "2. Streamlit Demo (Interactive Web App)"
echo "3. Jupyter Notebook Demo"
echo "4. Run All Tests"
echo "5. Open Demo Guide"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting FastAPI Demo on http://localhost:8000/docs"
        cd demos && python fastapi_demo.py
        ;;
    2)
        echo "🚀 Starting Streamlit Demo on http://localhost:8501"
        cd demos && streamlit run streamlit_demo.py
        ;;
    3)
        echo "🚀 Starting Jupyter Notebook"
        cd demos && jupyter notebook notebook_demo.ipynb
        ;;
    4)
        echo "🧪 Running Tests..."
        pytest tests/ -v --tb=short
        ;;
    5)
        echo "📖 Opening Demo Guide..."
        cat DEMO_GUIDE.md
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
