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

# Run with auto-reload for development
maniml script.py SceneName --autoreload

# Examples
maniml examples/01_getting_started/01_hello_world.py HelloWorld
```

### Testing
```bash
# Run all integration tests
python tests/integration/run_all_tests.py

# Run unit tests with pytest
pytest tests/unit/

# Run with coverage
pytest --cov=maniml --cov-report=html
```

### Development Setup
```bash
# Install in development mode
pip install -e .

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

## Code Architecture

### Core Structure

```
maniml/
├── manimlib/          # Core library (from ManimGL)
│   ├── animation/     # Animation classes
│   ├── camera/        # Camera and rendering
│   ├── mobject/       # Mathematical objects
│   ├── scene/         # Scene management
│   ├── utils/         # Utilities
│   └── shaders/       # OpenGL shaders
├── examples/          # Tutorial-style examples
├── tests/             # Test suite
└── docs/              # Documentation
```

### Key Components

1. **Mobjects** (Mathematical Objects)
   - Base classes: `Mobject`, `VMobject`, `SVGMobject`
   - Geometric shapes: `Circle`, `Square`, `Line`, etc.
   - Text: `Text`, `MathTex`, `Tex`
   - Groups: `VGroup`, `Group`

2. **Animations**
   - Creation: `Create`, `Write`, `FadeIn`
   - Transformation: `Transform`, `ReplacementTransform`
   - Property changes: `.animate` syntax
   - Custom animations via `Animation` base class

3. **Scenes**
   - `Scene`: Basic 2D scenes
   - `ThreeDScene`: 3D scenes with camera control
   - `InteractiveScene`: Scenes with mouse/keyboard input
   - Custom scenes inherit from these

4. **Interactive Features** (Unique to ManimGL/maniml)
   - `MotionMobject`: Draggable objects
   - `Button`, `Slider`, `Checkbox`: UI elements
   - Mouse event handling
   - Real-time parameter updates

## Common Development Tasks

### Adding New Features

1. **New Mobject Types**: Add to `manimlib/mobject/`
2. **New Animations**: Add to `manimlib/animation/`
3. **Scene Enhancements**: Modify `manimlib/scene/`
4. **Utilities**: Add to `manimlib/utils/`

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_mobject.py

# Run with coverage
pytest --cov=manimlib
```

### Examples

When adding examples:
1. Follow the tutorial structure in `examples/`
2. Include comprehensive comments
3. Add to appropriate difficulty level directory
4. Update the README.md in that directory

## API Compatibility Notes

### ManimGL Compatibility

maniml aims for high compatibility with ManimGL code:
- Same class names and hierarchy
- Same method signatures (mostly)
- Same coordinate system
- Same default styles

### Known Differences from ManimCE

Users coming from ManimCE should note:
- Different renderer (OpenGL vs Cairo)
- Different coordinate system (pixels vs units)
- Different default styles
- No `Manim` class (use `Scene` directly)
- Interactive features not in ManimCE

### Migration Considerations

When helping users migrate code:
1. From ManimGL → Usually works directly
2. From ManimCE → May need coordinate adjustments
3. Check for missing methods (some ManimCE additions not in maniml)

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints where helpful
- Google-style docstrings
- Descriptive variable names

### Animation Patterns
```python
# Good: Clear, simple animations
circle = Circle()
self.play(Create(circle))
self.play(circle.animate.shift(RIGHT))

# Avoid: Overly complex one-liners
self.play(*[Create(Circle().shift(i*RIGHT)) for i in range(10)])
```

### Performance Considerations
- Minimize mobject count
- Use `VGroup` for batch operations
- Avoid excessive updaters
- Cache computed values

## Common Issues and Solutions

### Performance Problems
- Too many mobjects → Use `VGroup`
- Slow updaters → Optimize calculations
- Memory leaks → Remove unused updaters

### Rendering Issues
- Black screen → Check OpenGL compatibility
- Flickering → Adjust frame rate
- Wrong colors → Check color space

### API Confusion
- Missing method → Check if it's ManimCE-specific
- Different behavior → Check coordinate system
- Import errors → Verify installation

## Development Workflow

### Making Changes
1. Create feature branch
2. Write tests first (TDD preferred)
3. Implement feature
4. Update documentation
5. Add example if appropriate
6. Update CHANGELOG.md

### Code Review Focus
- API compatibility
- Performance impact
- Documentation quality
- Test coverage
- Example clarity

## Project Philosophy

1. **Simplicity over features**: Better to do less but do it well
2. **Stability over innovation**: Avoid breaking changes
3. **Learning over complexity**: Make it easy for beginners
4. **Performance matters**: Keep animations smooth
5. **Interactivity is key**: This sets maniml apart

## Future Directions

Potential areas for development:
- Enhanced interactive features
- Better performance optimization
- More comprehensive examples
- Integration with Jupyter notebooks
- Export to various formats
- Plugin system for extensions

## Quick Reference

### Running Examples
```bash
# Basic example
maniml examples/01_getting_started/01_hello_world.py HelloWorld

# Interactive example
maniml examples/02_interactive_objects/01_draggable_shapes.py DraggableShapes

# 3D example
maniml examples/03_3d_animations/01_basic_3d_shapes.py Basic3DShapes
```

### Creating New Scene
```python
from maniml import *

class MyScene(Scene):
    def construct(self):
        # Your animation here
        circle = Circle()
        self.play(Create(circle))
        self.wait()
```

### Interactive Scene Template
```python
class InteractiveDemo(Scene):
    def construct(self):
        # Create draggable object
        circle = Circle()
        draggable = MotionMobject(circle)
        self.add(draggable)
        
        # Enable interaction
        self.embed()
```

## Getting Help

1. Check existing examples
2. Review test files for usage patterns
3. Look at manimlib source code
4. Consider ManimGL documentation (often applicable)
5. Open GitHub issue for bugs/questions

Remember: maniml prioritizes clarity and usability. When in doubt, choose the simpler solution.