# Copyright (c) 2025 Venkata Vikhyat Choppa
# Licensed under the Apache 2.0 License. See LICENSE file for details.

import pytest
from quantstratforge.generator import StrategyGenerator

@pytest.fixture
def generator():
    return StrategyGenerator(model_path="gpt2")

def test_generation(generator):
    result = generator.generate("Test input data")
    assert "strategy_code" in result
    assert "explanation" in result