# maniml Examples

This directory contains various examples demonstrating the capabilities of maniml, a standalone version of Manim without external dependencies.

## Directory Structure

### 📁 basic/
Introductory examples for beginners:
- `01_hello_world.py` - Your first maniml animation
- `02_shapes_and_colors.py` - Working with shapes and colors
- `03_animation_basics.py` - Fundamental animation types

### 📁 interactive/
Interactive features and user input:
- `interactive_basics.py` - Introduction to interactive elements
- `draggable_objects.py` - Creating draggable shapes
- `motion_mobject_demo.py` - Using MotionMobject for drag functionality
- `interactive_bezier.py` - Interactive Bezier curve manipulation
- `interactive_triangle.py` - Interactive triangle demonstration
- `cursor_demo.py` - Mouse cursor interaction examples
- `mouse_events.py` - Handling various mouse events

### 📁 3d/
Three-dimensional animations:
- `basic_3d_scene.py` - Introduction to 3D scenes
- `comprehensive_3d.py` - Various 3D objects and transformations
- `advanced_3d_scene.py` - Complex 3D animations
- `surface_plots.py` - 3D surface plotting
- `interactive_3d_scene.py` - Interactive 3D scene manipulation

### 📁 advanced/
Advanced features and specialized use cases:
- `edge_cases_demo.py` - Handling edge cases and special scenarios
- `api_compatibility.py` - Differences between ManimCE and maniml APIs
- `feature_showcase.py` - Comprehensive feature demonstration
- `plotting_showcase.py` - Advanced plotting capabilities
- `custom_axes.py` - Creating custom coordinate systems
- `live_reload_demo.py` - Live code reloading for development

## Running Examples

To run any example, use the maniml command:

```bash
# Run a basic example
maniml examples/basic/hello_world.py HelloWorld

# Run an interactive example
maniml examples/interactive/draggable_objects.py DraggableShapes

# Run a 3D example
maniml examples/3d/basic_3d_scene.py Basic3DScene
```

## Prerequisites

1. **Python 3.7+** installed
2. **LaTeX** (optional, for mathematical expressions)
3. **maniml** package installed

## Tips

- Interactive examples will open a window where you can interact with the animation
- Press `q` or `ESC` to quit an animation
- Use `d`, `f`, or `z` keys to interact with scenes (when applicable)
- Some examples may require additional dependencies noted in their docstrings

## Contributing

Feel free to add your own examples! Please follow the existing structure and naming conventions.