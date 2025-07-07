# Advanced Techniques in maniml

This section covers advanced topics for experienced users.

## Prerequisites

- Complete all previous tutorials
- Comfortable with Python programming
- Understanding of maniml's architecture

## Lesson 1: API Differences from ManimCE

Understanding differences when migrating from ManimCE.

### Running the Example

```bash
maniml 01_api_differences.py APIDifferences
```

### Key Differences

#### Parameter Names
```python
# ManimCE
shapes.arrange_in_grid(rows=2, cols=3, buff=0.5)

# maniml
shapes.arrange_in_grid(2, 3, buff=0.5)  # Positional args
```

#### Missing Methods
```python
# ManimCE
self.add_fixed_in_frame_mobjects(text)

# maniml
text.fix_in_frame()
self.add(text)
```

#### Animation Differences
```python
# Some animations have different names or parameters
# Check the example file for comprehensive list
```

### Migration Strategy

1. Start with simple scenes
2. Test each animation type
3. Create wrapper functions for compatibility
4. Document differences you find

## Lesson 2: Custom Objects

Create your own reusable mobjects.

### Running the Example

```bash
maniml 02_custom_objects.py CustomObjects
```

### Creating Custom Mobjects

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_shape()
    
    def create_shape(self):
        # Define points
        points = [
            LEFT * 2,
            UP * 1,
            RIGHT * 2,
            DOWN * 1
        ]
        
        # Create path
        self.set_points_as_corners(points)
        self.close_path()
        
        # Style
        self.set_fill(BLUE, opacity=0.5)
        self.set_stroke(WHITE, width=2)
```

### Custom Animations

```python
class Spiral(Animation):
    def __init__(self, mobject, center=ORIGIN, **kwargs):
        self.center = center
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha):
        angle = 4 * PI * alpha
        radius = 2 * alpha
        
        position = self.center + radius * np.array([
            np.cos(angle),
            np.sin(angle),
            0
        ])
        
        self.mobject.move_to(position)
        self.mobject.rotate(angle)
```

### Composite Objects

```python
class LabeledAxes(VGroup):
    def __init__(self, x_range, y_range, **kwargs):
        # Create components
        self.axes = Axes(x_range=x_range, y_range=y_range)
        self.x_label = MathTex("x").next_to(self.axes.x_axis, DOWN)
        self.y_label = MathTex("y").next_to(self.axes.y_axis, LEFT)
        
        # Group them
        super().__init__(
            self.axes,
            self.x_label,
            self.y_label,
            **kwargs
        )
```

## Lesson 3: Development Workflow

Efficient development techniques.

### Hot Reload Setup

```python
# Enable file watching for automatic reload
from maniml.scene.auto_reload import AutoReloadScene

class DevelopmentScene(AutoReloadScene):
    def construct(self):
        # Your code here
        # Changes reload automatically!
        pass
```

### Performance Optimization

```python
# Profile your scene
import cProfile
import pstats

def profile_scene():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run your scene
    scene = YourScene()
    scene.run()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

### Debugging Techniques

```python
class DebugScene(Scene):
    def construct(self):
        # Visual debugging
        debug_dot = Dot(color=RED)
        debug_dot.move_to(self.get_debug_point())
        self.add(debug_dot)
        
        # Print debugging
        self.add_debug_text("Current state: " + str(self.state))
        
        # Pause for inspection
        self.wait(5)
    
    def add_debug_text(self, text):
        debug_text = Text(text, font_size=16, color=YELLOW)
        debug_text.to_corner(DL)
        self.add(debug_text)
```

## Advanced Animation Techniques

### Custom Rate Functions

```python
def bounce_rate_func(t):
    if t < 0.5:
        return 4 * t * t
    else:
        return 1 - 4 * (1 - t) * (1 - t)

self.play(
    circle.animate.shift(RIGHT * 3),
    rate_func=bounce_rate_func
)
```

### Animation Queues

```python
class QueuedAnimations(Scene):
    def construct(self):
        # Create animation queue
        animations = []
        
        for i in range(5):
            circle = Circle(radius=0.3)
            circle.shift(RIGHT * i)
            animations.append(Create(circle))
        
        # Play with delay
        self.play(LaggedStart(*animations, lag_ratio=0.2))
```

### Updater Chains

```python
# Complex updater system
tracker = ValueTracker(0)

def update_position(mob):
    t = tracker.get_value()
    mob.move_to([np.cos(t), np.sin(t), 0])

def update_color(mob):
    t = tracker.get_value()
    mob.set_color(interpolate_color(BLUE, RED, t / (2 * PI)))

circle.add_updater(update_position)
circle.add_updater(update_color)

self.play(tracker.animate.set_value(2 * PI), run_time=5)
```

## Shader Programming

For advanced visual effects:

```python
# Custom shader (in manimgl_core/shaders/)
# vertex.glsl
"""
#version 330
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

in vec3 position;
in vec4 color;
out vec4 v_color;

void main() {
    v_color = color;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

# Use in mobject
class ShaderMobject(Mobject):
    shader_folder = "custom_shader"
    # Implementation details...
```

## Best Practices

### Code Organization

```python
# scene_utils.py
def create_title(text, **kwargs):
    """Standardized title creation"""
    title = Text(text, font_size=48, **kwargs)
    title.to_edge(UP)
    return title

# main_scene.py
from scene_utils import create_title

class MyScene(Scene):
    def construct(self):
        title = create_title("My Animation")
        self.play(Write(title))
```

### Configuration Management

```python
# config.py
COLORS = {
    "primary": "#0096FF",
    "secondary": "#FF6B6B",
    "background": "#1F1F1F"
}

ANIMATION_DEFAULTS = {
    "run_time": 1.0,
    "lag_ratio": 0.1
}

# Usage
from config import COLORS, ANIMATION_DEFAULTS

circle = Circle(color=COLORS["primary"])
self.play(Create(circle), **ANIMATION_DEFAULTS)
```

### Error Handling

```python
def safe_animation(scene, animation):
    """Run animation with error handling"""
    try:
        scene.play(animation)
    except Exception as e:
        print(f"Animation failed: {e}")
        # Fallback behavior
        scene.add(animation.mobject)
```

## Performance Optimization

### Batch Operations

```python
# Slow
for i in range(1000):
    dot = Dot()
    dot.shift(random_point())
    self.add(dot)

# Fast
dots = VGroup(*[
    Dot().shift(random_point())
    for i in range(1000)
])
self.add(dots)
```

### Lazy Evaluation

```python
class LazyMobject(VMobject):
    def __init__(self, generator_func, **kwargs):
        self.generator_func = generator_func
        self._generated = False
        super().__init__(**kwargs)
    
    def generate(self):
        if not self._generated:
            self.become(self.generator_func())
            self._generated = True
    
    def get_points(self):
        self.generate()
        return super().get_points()
```

## Advanced Project Structure

```
my_maniml_project/
├── scenes/
│   ├── __init__.py
│   ├── intro.py
│   ├── main_content.py
│   └── outro.py
├── utils/
│   ├── __init__.py
│   ├── custom_mobjects.py
│   ├── custom_animations.py
│   └── helpers.py
├── assets/
│   ├── images/
│   ├── svg/
│   └── data/
├── config.py
├── main.py
└── requirements.txt
```

## Testing Your Code

```python
# test_custom_objects.py
import pytest
from custom_mobjects import CustomShape

def test_custom_shape_creation():
    shape = CustomShape()
    assert shape.get_color() == BLUE
    assert len(shape.get_points()) > 0

def test_custom_shape_animation():
    from maniml import Scene, Create
    
    scene = Scene()
    shape = CustomShape()
    animation = Create(shape)
    
    # Test animation runs without error
    scene.play(animation)
```

## Next Steps

1. Study the maniml source code
2. Contribute to the project
3. Create your own animation library
4. Build educational content
5. Experiment with new visualization techniques

## Resources

- [maniml GitHub](https://github.com/yourusername/maniml)
- [Contributing Guide](../../CONTRIBUTING.md)
- [API Documentation](../../docs/api/README.md)
- Community forums and discussions

Remember: The best way to learn is by creating!