#!/usr/bin/env python
"""Test that the Streamlit demo has valid syntax and imports"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_streamlit_demo_syntax():
    """Test if streamlit_demo.py has valid syntax"""
    try:
        with open('demos/streamlit_demo.py', 'r') as f:
            code = f.read()
        compile(code, 'demos/streamlit_demo.py', 'exec')
        print("✅ Streamlit demo syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Streamlit demo has syntax error: {e}")
        return False

def test_fastapi_demo_syntax():
    """Test if fastapi_demo.py has valid syntax"""
    try:
        with open('demos/fastapi_demo.py', 'r') as f:
            code = f.read()
        compile(code, 'demos/fastapi_demo.py', 'exec')
        print("✅ FastAPI demo syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ FastAPI demo has syntax error: {e}")
        return False

if __name__ == "__main__":
    result1 = test_streamlit_demo_syntax()
    result2 = test_fastapi_demo_syntax()
    
    if result1 and result2:
        print("\n🎉 All demo files have valid syntax")
        sys.exit(0)
    else:
        print("\n❌ Some demo files have syntax errors")
        sys.exit(1)


