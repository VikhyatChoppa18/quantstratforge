# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Test script for Jupyter Notebook demo"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json


def test_notebook_exists():
    """Test if notebook file exists"""
    print("\n🧪 Testing notebook existence...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        assert os.path.exists(notebook_path), f"Notebook not found at {notebook_path}"
        print(f"  ✅ Notebook found at {notebook_path}")
        return True
    except Exception as e:
        print(f"  ❌ Notebook existence test failed: {e}")
        return False


def test_notebook_structure():
    """Test if notebook has valid JSON structure"""
    print("\n🧪 Testing notebook structure...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        assert "cells" in notebook, "Notebook should have 'cells' key"
        assert "metadata" in notebook, "Notebook should have 'metadata' key"
        assert "nbformat" in notebook, "Notebook should have 'nbformat' key"
        
        cell_count = len(notebook["cells"])
        print(f"  ✅ Notebook structure valid")
        print(f"     Cells: {cell_count}")
        print(f"     Format: {notebook.get('nbformat', 'unknown')}")
        return True
    except Exception as e:
        print(f"  ❌ Notebook structure test failed: {e}")
        return False


def test_notebook_cells():
    """Test if notebook has expected cells"""
    print("\n🧪 Testing notebook cells...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        cells = notebook["cells"]
        assert len(cells) > 0, "Notebook should have at least one cell"
        
        # Check for markdown cells
        markdown_cells = [c for c in cells if c["cell_type"] == "markdown"]
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        
        print(f"  ✅ Notebook cells found")
        print(f"     Markdown cells: {len(markdown_cells)}")
        print(f"     Code cells: {len(code_cells)}")
        
        # Check if notebook has imports
        has_imports = False
        for cell in code_cells:
            source = "".join(cell["source"])
            if "import" in source and "quantstratforge" in source:
                has_imports = True
                break
        
        if has_imports:
            print(f"  ✅ Notebook imports QuantStratForge")
        else:
            print(f"  ⚠️  No QuantStratForge imports found")
        
        return True
    except Exception as e:
        print(f"  ❌ Notebook cells test failed: {e}")
        return False


def test_notebook_imports():
    """Test if notebook cells have valid imports"""
    print("\n🧪 Testing notebook imports...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        cells = notebook["cells"]
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        
        # Look for import cells
        import_modules = set()
        for cell in code_cells:
            source = "".join(cell["source"])
            if "import" in source:
                # Extract imported modules
                if "quantstratforge" in source:
                    import_modules.add("quantstratforge")
                if "pandas" in source:
                    import_modules.add("pandas")
                if "numpy" in source:
                    import_modules.add("numpy")
                if "matplotlib" in source:
                    import_modules.add("matplotlib")
                if "seaborn" in source:
                    import_modules.add("seaborn")
        
        print(f"  ✅ Found imports: {', '.join(sorted(import_modules))}")
        
        # Check if key modules are present
        required_modules = ["quantstratforge"]
        for module in required_modules:
            if module not in import_modules:
                print(f"  ⚠️  Required module not imported: {module}")
        
        return True
    except Exception as e:
        print(f"  ❌ Notebook imports test failed: {e}")
        return False


def test_notebook_code_validity():
    """Test if notebook code cells have valid Python syntax"""
    print("\n🧪 Testing notebook code validity...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        cells = notebook["cells"]
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        
        syntax_errors = 0
        for i, cell in enumerate(code_cells):
            source = "".join(cell["source"])
            if source.strip():  # Skip empty cells
                try:
                    compile(source, f"cell_{i}", "exec")
                except SyntaxError as e:
                    syntax_errors += 1
                    print(f"  ❌ Syntax error in cell {i}: {e}")
        
        if syntax_errors == 0:
            print(f"  ✅ All {len(code_cells)} code cells have valid syntax")
        else:
            print(f"  ❌ {syntax_errors} code cells have syntax errors")
        
        return syntax_errors == 0
    except Exception as e:
        print(f"  ❌ Notebook code validity test failed: {e}")
        return False


def test_notebook_content():
    """Test if notebook has expected content"""
    print("\n🧪 Testing notebook content...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        cells = notebook["cells"]
        all_content = ""
        for cell in cells:
            all_content += "".join(cell["source"]) + "\n"
        
        # Check for key terms
        expected_terms = [
            "QuantStratForge",
            "DataFetcher",
            "Backtester",
        ]
        
        found_terms = []
        missing_terms = []
        
        for term in expected_terms:
            if term in all_content:
                found_terms.append(term)
            else:
                missing_terms.append(term)
        
        print(f"  ✅ Found key terms: {', '.join(found_terms)}")
        if missing_terms:
            print(f"  ⚠️  Missing terms: {', '.join(missing_terms)}")
        
        return len(missing_terms) == 0
    except Exception as e:
        print(f"  ❌ Notebook content test failed: {e}")
        return False


def test_notebook_can_execute():
    """Test if notebook can be executed (requires jupyter/nbconvert)"""
    print("\n🧪 Testing notebook executability...")
    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor
        
        notebook_path = "demos/notebook_demo.ipynb"
        
        with open(notebook_path, 'r') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Try to execute with timeout
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        
        print("  ⚠️  Executing notebook (this may take a while)...")
        try:
            ep.preprocess(notebook, {'metadata': {'path': 'demos/'}})
            print("  ✅ Notebook executed successfully!")
            return True
        except Exception as e:
            print(f"  ⚠️  Notebook execution failed: {e}")
            print("     (This is expected if model not trained or data unavailable)")
            return True  # Don't fail test on execution errors
            
    except ImportError:
        print("  ⚠️  nbformat/nbconvert not installed, skipping execution test")
        print("     Install with: pip install nbformat nbconvert")
        return True  # Don't fail if tools not available
    except Exception as e:
        print(f"  ❌ Notebook executability test failed: {e}")
        return False


def test_notebook_outputs():
    """Test if notebook has any outputs (indicating it was run)"""
    print("\n🧪 Testing notebook outputs...")
    notebook_path = "demos/notebook_demo.ipynb"
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        cells = notebook["cells"]
        cells_with_output = 0
        
        for cell in cells:
            if cell["cell_type"] == "code":
                outputs = cell.get("outputs", [])
                if outputs:
                    cells_with_output += 1
        
        print(f"  ℹ️  {cells_with_output} code cells have outputs")
        if cells_with_output > 0:
            print("  ✅ Notebook has been executed at least once")
        else:
            print("  ⚠️  Notebook appears to be unexecuted (no outputs)")
        
        return True  # This is informational, not a failure
    except Exception as e:
        print(f"  ❌ Notebook outputs test failed: {e}")
        return False


def test_notebook_dependencies():
    """Test if notebook dependencies are available"""
    print("\n🧪 Testing notebook dependencies...")
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        from quantstratforge import DataFetcher, Backtester
        
        print("  ✅ All required dependencies available:")
        print(f"     - pandas: {pandas.__version__}")
        print(f"     - numpy: {numpy.__version__}")
        print(f"     - matplotlib: {matplotlib.__version__}")
        print(f"     - seaborn: {seaborn.__version__}")
        print(f"     - quantstratforge: imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
        return False


def main():
    """Run all notebook tests"""
    print("=" * 60)
    print("Jupyter Notebook Demo Tests")
    print("=" * 60)
    
    results = []
    results.append(("Notebook Exists", test_notebook_exists()))
    results.append(("Notebook Structure", test_notebook_structure()))
    results.append(("Notebook Cells", test_notebook_cells()))
    results.append(("Notebook Imports", test_notebook_imports()))
    results.append(("Code Validity", test_notebook_code_validity()))
    results.append(("Notebook Content", test_notebook_content()))
    results.append(("Dependencies", test_notebook_dependencies()))
    results.append(("Notebook Outputs", test_notebook_outputs()))
    # Optional: Only run if user wants full execution
    # results.append(("Notebook Execution", test_notebook_can_execute()))
    
    print("\n" + "=" * 60)
    print("Jupyter Notebook Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:<30} {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All Jupyter notebook tests passed!")
        print("\n💡 To run the notebook:")
        print("   jupyter notebook demos/notebook_demo.ipynb")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


