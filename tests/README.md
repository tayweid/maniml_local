# maniml Tests

This directory contains the test suite for maniml, ensuring reliability and compatibility.

## Directory Structure

### 📁 unit/
Unit tests for individual components:
- `test_cursor_fix.py` - Tests for cursor positioning fixes
- `test_manimse.py` - Legacy compatibility tests
- `test_minimal.py` - Minimal functionality tests
- `test_queue.py` - Animation queue tests

### 📁 integration/
Integration tests for complete workflows:
- `test_maniml_imports.py` - Import system verification
- `test_simple_maniml.py` - Basic integration tests
- `test_final_maniml.py` - Comprehensive integration tests
- `test_with_window.py` - Window creation and display tests
- `run_all_tests.py` - Master test runner
- `check_config.py` - Configuration verification

### 📁 fixtures/
Test fixtures and sample data (currently empty, for future use)

## Running Tests

### Run all tests:
```bash
python tests/integration/run_all_tests.py
```

### Run specific test files:
```bash
# Unit tests
python -m pytest tests/unit/test_minimal.py

# Integration tests  
python tests/integration/test_maniml_imports.py
```

### Run with coverage:
```bash
python -m pytest tests/ --cov=maniml --cov-report=html
```

## Test Categories

### Import Tests
Verify that all maniml imports work correctly and that the package structure is sound.

### Rendering Tests
Ensure animations render without errors and produce expected output.

### Interactive Tests
Test interactive features like draggable objects and mouse events.

### Compatibility Tests
Verify compatibility with ManimCE-style code and API differences.

### Performance Tests
Monitor rendering performance and memory usage.

## Writing New Tests

When adding new tests:
1. Place unit tests in `tests/unit/`
2. Place integration tests in `tests/integration/`
3. Use descriptive test names starting with `test_`
4. Include docstrings explaining what is being tested
5. Follow the existing test patterns

Example test structure:
```python
"""Test module description"""

import pytest
from maniml import *

class TestFeatureName:
    """Test class for specific feature"""
    
    def test_specific_behavior(self):
        """Test that specific behavior works correctly"""
        # Test implementation
        assert expected == actual
```

## Continuous Integration

These tests are designed to be run in CI/CD pipelines. They avoid opening windows or requiring user interaction unless specifically testing those features.