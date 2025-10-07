# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Proprietary License. See LICENSE file for details.

"""
Demo runner script for QuantStratForge
Provides easy access to different demo interfaces
"""

import argparse
import subprocess
import sys
import os

def run_streamlit_demo():
    """Run Streamlit demo"""
    print("🚀 Starting Streamlit demo...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_demo.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error running Streamlit demo. Make sure streamlit is installed.")
        print("Install with: pip install streamlit")

def run_fastapi_demo():
    """Run FastAPI demo"""
    print("🚀 Starting FastAPI demo...")
    try:
        subprocess.run([sys.executable, "fastapi_demo.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error running FastAPI demo. Make sure uvicorn is installed.")
        print("Install with: pip install uvicorn")

# Flask and Jupyter demos removed - focusing on Streamlit and FastAPI

def main():
    parser = argparse.ArgumentParser(description="QuantStratForge Demo Runner")
    parser.add_argument(
        "demo_type",
        choices=["streamlit", "fastapi", "all"],
        help="Type of demo to run"
    )
    
    args = parser.parse_args()
    
    print("📈 QuantStratForge Demo Runner")
    print("=" * 40)
    
    if args.demo_type == "streamlit":
        run_streamlit_demo()
    elif args.demo_type == "fastapi":
        run_fastapi_demo()
    elif args.demo_type == "all":
        print("🚀 Available demos:")
        print("1. Streamlit Demo (Interactive web app)")
        print("2. FastAPI Demo (REST API)")
        print("\nTo run a specific demo:")
        print("python run_demos.py streamlit")
        print("python run_demos.py fastapi")

if __name__ == "__main__":
    main()
