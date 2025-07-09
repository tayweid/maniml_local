# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

maniml_local is a working implementation that runs ManimCE code on ManimGL's fast OpenGL renderer. This codebase demonstrates how to combine ManimCE's API with ManimGL's performance through a compatibility layer.

### Key Architecture

The project uses a dual-layer structure:
- **maniml/**: Compatibility layer providing ManimCE-style API
- **maniml/manimgl_core/**: Forked ManimGL engine for OpenGL rendering

This allows existing ManimCE code to run with 10-20x performance improvements.

## Commands

### Running Animations
```bash
# Standard usage (always opens preview window)
maniml script.py SceneName

# Alternative: run as module
python -m maniml script.py SceneName

# Run with auto-reload for development
maniml script.py SceneName --autoreload

# Examples
maniml examples/01_getting_started/01_hello_world.py HelloWorld
```

### Testing
```bash
# Run all tests with pytest
pytest

# Run with coverage
pytest --cov=maniml --cov-report=html

# Run integration tests
python tests/integration/run_all_tests.py

# Run specific test file
pytest tests/unit/test_mobject.py
```

### Linting and Formatting
```bash
# Format code with black
black maniml/

# Sort imports
isort maniml/

# Type checking
mypy maniml/

# Lint with flake8
flake8 maniml/
```

### Development Setup
```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e .[dev]

# Alternative setup script
./setup.sh
```

## High-Level Architecture

### Compatibility Layer Design
The `maniml/` directory wraps ManimGL functionality to provide ManimCE compatibility:
- **Animation mapping**: `Create` → `ShowCreation`, `Uncreate` → `Uncreation`
- **Default values**: CE-style defaults for colors, sizes, positions
- **API translation**: Methods and parameters adapted to match CE expectations
- **Font handling**: Cross-platform font name mapping

### Auto-Reload System
Located in `maniml/scene/scene.py`, this system enables hot-reloading during development:
- Watches for file changes and re-executes only modified code
- Maintains scene state through checkpoints
- Preserves mobject positions and properties between reloads
- Supports line-by-line change detection
- Uses IPython's `run_cell()` for isolated code execution

### Checkpoint Navigation
The scene system supports interactive navigation:
- **Arrow keys**: Navigate between animation checkpoints
- **Left/Right**: Move backward/forward through animations
- **State preservation**: Each checkpoint saves complete scene state

### Rendering Pipeline
1. **Scene Construction**: User code creates mobjects and animations
2. **API Translation**: CE calls converted to GL equivalents
3. **OpenGL Rendering**: ManimGL core handles GPU acceleration
4. **Window Management**: Real-time preview with interactive controls

### Key Integration Points
- **Scene class**: Enhanced with auto-reload and CE compatibility
- **Animation system**: Dual inheritance for CE/GL compatibility
- **Mobject wrappers**: Translate properties and methods
- **Config system**: Unified configuration handling

## Performance Considerations

### OpenGL vs Cairo
- This implementation uses OpenGL (like ManimGL) instead of Cairo (like ManimCE)
- Results in 10-20x faster rendering for most scenes
- Real-time preview instead of file generation
- GPU acceleration for complex animations

### Optimization Strategies
- Batch operations using `VGroup`
- Minimize updater functions
- Cache computed values where possible
- Use shader-based effects for performance

## Important Implementation Details

### File Change Detection
The auto-reload system (`maniml/scene/scene.py`) uses:
- File modification time tracking
- Line-by-line diff detection
- Smart re-execution of only changed code sections

### Animation Checkpointing
When implementing checkpoint features:
- Each `self.play()` call creates a checkpoint
- Checkpoints store full scene state
- Navigation preserves object references and properties

### Import System
The compatibility layer rewrites imports:
- `from manim import *` → loads maniml compatibility layer
- Preserves existing ManimCE code functionality
- Maps CE classes to GL implementations

## Testing Patterns

### Scene Testing
```python
class TestScene(Scene):
    def construct(self):
        # Create test objects
        circle = Circle()
        self.play(Create(circle))
        
        # Test transformations
        self.play(circle.animate.shift(RIGHT))
        
        # Verify state
        self.wait()
```

Run test scenes directly:
```bash
python -m maniml test_file.py TestScene
```

### Integration Testing
- Located in `tests/integration/`
- Tests full animation rendering
- Verifies CE compatibility
- Checks checkpoint functionality