# Getting Started with maniml

Welcome to maniml! This tutorial will guide you through the basics of creating mathematical animations.

## Prerequisites

- maniml installed (see [Installation Guide](../../INSTALLATION.md))
- Basic Python knowledge
- A text editor or IDE

## Lesson 1: Hello World

Let's start with the simplest possible animation.

### Running the Example

```bash
maniml 01_hello_world.py HelloWorld
```

### Understanding the Code

```python
from maniml import *

class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello, maniml!", font_size=48)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
```

**Key Concepts:**
- Every animation is a `Scene` class
- The `construct()` method defines what happens
- `Text` creates text objects
- `self.play()` runs animations
- `self.wait()` pauses the animation

### Exercise

Try modifying the example:
1. Change the text message
2. Change the font size
3. Try different animations: `Create`, `FadeIn`, `DrawBorderThenFill`

## Lesson 2: Shapes and Colors

Now let's work with geometric shapes.

### Running the Example

```bash
maniml 02_shapes_and_colors.py ShapesAndColors
```

### Key Concepts

**Creating Shapes:**
```python
circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
square = Square(side_length=2, color=RED)
triangle = Triangle(color=GREEN)
```

**Positioning:**
```python
circle.shift(LEFT * 3)  # Move 3 units left
square.to_edge(UP)     # Move to top edge
triangle.next_to(circle, RIGHT)  # Position relative to another object
```

**Styling:**
- `color`: Stroke color
- `fill_opacity`: Transparency (0-1)
- `stroke_width`: Line thickness

### Exercise

Create a scene with:
1. A blue circle on the left
2. A red square in the center
3. A green triangle on the right
4. All shapes should have 70% opacity

## Lesson 3: Animation Basics

Learn about different animation types.

### Running the Example

```bash
maniml 03_animation_basics.py AnimationBasics
```

### Animation Types

**Creation Animations:**
- `Create`: Draws the outline
- `FadeIn`: Fades in with optional direction
- `GrowFromCenter`: Grows from center point

**Transformation Animations:**
- `Transform`: Morphs one object into another
- `ReplacementTransform`: Transform and replace
- `TransformFromCopy`: Transform a copy

**Property Animations:**
```python
circle.animate.shift(RIGHT * 2)
square.animate.scale(1.5)
triangle.animate.rotate(PI)
text.animate.set_color(RED)
```

### Simultaneous Animations

Run multiple animations at once:
```python
self.play(
    circle.animate.shift(UP),
    square.animate.rotate(PI/4),
    triangle.animate.scale(0.5),
    run_time=2
)
```

### Exercise

Create an animation that:
1. Creates three shapes
2. Moves them to form a horizontal line
3. Transforms the circle into a square
4. Rotates all shapes simultaneously
5. Fades everything out

## Tips for Beginners

1. **Start Simple**: Master basic shapes before complex scenes
2. **Use Comments**: Document what each section does
3. **Test Often**: Run your scene frequently to check progress
4. **Read Errors**: Error messages often point to the exact problem
5. **Experiment**: Try changing parameters to see what happens

## Common Patterns

### Scene Setup
```python
class MyScene(Scene):
    def construct(self):
        # Create title
        title = Text("My Animation", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Main content here
        
        # Clean up
        self.play(FadeOut(*self.mobjects))
```

### Grouping Objects
```python
shapes = VGroup(circle, square, triangle)
shapes.arrange(RIGHT, buff=0.5)  # Arrange with spacing
self.play(Create(shapes))  # Animate all at once
```

### Using Loops
```python
circles = VGroup()
for i in range(5):
    circle = Circle(radius=0.3)
    circle.shift(RIGHT * i)
    circles.add(circle)

self.play(Create(circles, lag_ratio=0.1))
```

## Next Steps

After completing these exercises:
1. Move on to [Interactive Objects](../02_interactive_objects/README.md)
2. Explore [3D Animations](../03_3d_animations/README.md)
3. Check out [Advanced Techniques](../04_advanced_techniques/README.md)

## Getting Help

- Check the [Troubleshooting Guide](../../TROUBLESHOOTING.md)
- Look at more examples in each category
- Open an issue on GitHub for bugs or questions

Happy animating!