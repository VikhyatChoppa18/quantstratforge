# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Comprehensive test suite for all demos"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import individual test modules
from .test_demos import main as test_core_demos
from .test_fastapi_demo import main as test_fastapi
from .test_notebook_demo import main as test_notebook


def main():
    """Run all demo tests"""
    print("\n" + "=" * 70)
    print("  QUANTSTRATFORGE - COMPREHENSIVE DEMO TEST SUITE")
    print("=" * 70 + "\n")
    
    results = {}
    
    # Test 1: Core components (DataFetcher, Backtester, Optimizer)
    print("\n" + "🔷" * 35)
    print("  TEST SUITE 1: Core Components")
    print("🔷" * 35)
    results['core'] = test_core_demos()
    
    # Test 2: FastAPI Demo
    print("\n" + "🔷" * 35)
    print("  TEST SUITE 2: FastAPI Demo")
    print("🔷" * 35)
    results['fastapi'] = test_fastapi()
    
    # Test 3: Jupyter Notebook
    print("\n" + "🔷" * 35)
    print("  TEST SUITE 3: Jupyter Notebook")
    print("🔷" * 35)
    results['notebook'] = test_notebook()
    
    # Final Summary
    print("\n" + "=" * 70)
    print("  FINAL TEST SUMMARY")
    print("=" * 70)
    
    suite_names = {
        'core': 'Core Components',
        'fastapi': 'FastAPI Demo',
        'notebook': 'Jupyter Notebook'
    }
    
    for suite, result in results.items():
        status = "✅ PASSED" if result == 0 else "❌ FAILED"
        print(f"{suite_names[suite]:<30} {status}")
    
    passed = sum(1 for r in results.values() if r == 0)
    total = len(results)
    
    print("=" * 70)
    print(f"Total Suites: {passed}/{total} passed")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 🎊 ALL DEMO TESTS PASSED! 🎊 🎉")
        print("\n✅ Ready to:")
        print("   • Launch Streamlit demo: streamlit run demos/streamlit_demo.py")
        print("   • Launch FastAPI demo: python demos/fastapi_demo.py")
        print("   • Open Jupyter notebook: jupyter notebook demos/notebook_demo.ipynb")
        print("   • Record demo video: Follow LINKEDIN_VIDEO_GUIDE.md")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed.")
        print("   Check the detailed output above for more information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


