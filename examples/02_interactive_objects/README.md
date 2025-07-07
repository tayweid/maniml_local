# Interactive Objects in maniml

This tutorial covers creating interactive animations where users can click, drag, and manipulate objects in real-time.

## Prerequisites

- Complete the [Getting Started](../01_getting_started/README.md) tutorial
- Understanding of basic maniml objects and animations

## Lesson 1: Draggable Shapes

Learn how to make objects draggable with the mouse.

### Running the Example

```bash
maniml 01_draggable_shapes.py DraggableShapes
```

### The MotionMobject Class

`MotionMobject` wraps any mobject to make it draggable:

```python
circle = Circle(radius=1, color=BLUE)
draggable_circle = MotionMobject(circle)
self.add(draggable_circle)
```

### Entering Interactive Mode

Use `self.embed()` to enter interactive mode:

```python
def construct(self):
    # Create objects
    shapes = self.create_draggable_shapes()
    self.add(shapes)
    
    # Enter interactive mode
    self.embed()  # Allows mouse interaction
```

### Key Concepts

1. **MotionMobject**: Makes any object draggable
2. **self.embed()**: Enables interactive mode
3. **Grouping**: Objects maintain their relationships when dragged

### Exercise

Create a scene with:
1. Three draggable shapes of different colors
2. Labels that move with the shapes
3. A reset button that returns shapes to original positions

## Lesson 2: Advanced Dragging

More complex draggable interactions.

### Running the Example

```bash
maniml 02_draggable_demo.py DraggableDemo
```

### Constraints and Limits

You can constrain dragging behavior:

```python
# Limit to horizontal movement
def constrain_horizontal(mob, point):
    mob.move_to([point[0], mob.get_center()[1], 0])

draggable = MotionMobject(circle, update_function=constrain_horizontal)
```

### Connecting Objects

Create relationships between draggable objects:

```python
line = Line()

def update_line(line):
    line.put_start_and_end_on(
        circle1.get_center(),
        circle2.get_center()
    )

line.add_updater(update_line)
```

### Exercise

Create:
1. Two draggable points
2. A line connecting them that updates as they move
3. Display the distance between points

## Lesson 3: Mouse Events

Handle clicks and other mouse events.

### Running the Example

```bash
maniml 03_mouse_events.py MouseEvents
```

### Click Detection

Detect clicks on objects:

```python
def on_click(mob, event):
    # Change color on click
    mob.set_color(random_color())
    
circle.add_mouse_click_listener(on_click)
```

### Mouse Position Tracking

Track mouse movement:

```python
def construct(self):
    # Create a dot that follows the mouse
    cursor_dot = Dot(color=YELLOW)
    
    def update_cursor(mob):
        # Get mouse position in scene coordinates
        mouse_point = self.mouse_point.get_location()
        mob.move_to(mouse_point)
    
    cursor_dot.add_updater(update_cursor)
    self.add(cursor_dot)
```

### Exercise

Create an interactive drawing tool:
1. Click to place dots
2. Drag to draw lines
3. Right-click to clear

## Advanced Interactive Features

### Buttons

Create clickable buttons:

```python
from maniml import Button, Rectangle, Text, VGroup

# Create button visuals
button_bg = Rectangle(width=2, height=0.8, color=BLUE, fill_opacity=0.8)
button_text = Text("Click Me!", font_size=20)
button_group = VGroup(button_bg, button_text)

# Make it interactive
def on_button_click():
    print("Button clicked!")
    button_bg.set_color(GREEN)

button = Button(button_group, on_click=on_button_click)
self.add(button)
```

### Sliders

Create value sliders:

```python
from maniml import LinearNumberSlider

slider = LinearNumberSlider(
    value=5,
    min_value=0,
    max_value=10,
    step=0.1,
    width=4
)

# Track value changes
def on_value_change(value):
    print(f"Slider value: {value}")

slider.add_value_change_listener(on_value_change)
```

### Checkboxes

Toggle options:

```python
from maniml import Checkbox

checkbox = Checkbox(
    checked=False,
    size=0.5,
    color=WHITE
)

def on_toggle(checked):
    print(f"Checkbox is {'checked' if checked else 'unchecked'}")

checkbox.add_change_listener(on_toggle)
```

## Best Practices

### Performance

1. **Limit Updaters**: Too many updaters can slow interaction
2. **Batch Updates**: Group related updates together
3. **Simple Calculations**: Keep update functions fast

### User Experience

1. **Visual Feedback**: Show hover states, click feedback
2. **Clear Instructions**: Add text explaining interactions
3. **Reset Options**: Provide ways to reset or undo

### Code Organization

```python
class InteractiveScene(Scene):
    def construct(self):
        self.setup_ui()
        self.create_objects()
        self.add_interactions()
        self.embed()
    
    def setup_ui(self):
        # Create UI elements
        pass
    
    def create_objects(self):
        # Create main objects
        pass
    
    def add_interactions(self):
        # Add event handlers
        pass
```

## Common Patterns

### Drag and Drop

```python
def make_draggable_with_snap(obj, snap_positions):
    """Make object snap to nearest position when released"""
    
    def on_drag_end(mob):
        # Find nearest snap position
        nearest = min(snap_positions, 
                     key=lambda p: np.linalg.norm(mob.get_center() - p))
        mob.animate.move_to(nearest).run()
    
    draggable = MotionMobject(obj)
    draggable.on_drag_end = on_drag_end
    return draggable
```

### Interactive Graphs

```python
# Create draggable control points for a curve
control_points = VGroup(*[
    MotionMobject(Dot(point, color=RED))
    for point in points
])

def update_curve(curve):
    positions = [p.get_center() for p in control_points]
    new_curve = self.get_curve_through_points(positions)
    curve.become(new_curve)

curve.add_updater(update_curve)
```

## Debugging Interactive Scenes

1. **Print Debug Info**: Use print statements in event handlers
2. **Visual Debug**: Add temporary objects to show state
3. **Slow Motion**: Reduce animation speed to see issues

## Next Steps

- Explore [3D Interactive Scenes](../03_3d_animations/README.md)
- Learn [Advanced Techniques](../04_advanced_techniques/README.md)
- Build interactive math demonstrations
- Create educational tools with UI

## Project Ideas

1. **Interactive Function Plotter**: Drag to change parameters
2. **Geometry Explorer**: Manipulate shapes to explore properties
3. **Physics Simulator**: Interactive pendulum or spring system
4. **Math Game**: Drag numbers to solve equations

Remember: Interactive features make math come alive!