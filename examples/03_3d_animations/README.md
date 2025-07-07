# 3D Animations in maniml

This tutorial covers creating three-dimensional scenes and animations.

## Prerequisites

- Complete [Getting Started](../01_getting_started/README.md)
- Basic understanding of 3D coordinates

## Lesson 1: Basic 3D Shapes

Introduction to 3D objects and scenes.

### Running the Example

```bash
maniml 01_basic_3d_shapes.py Basic3DShapes
```

### Creating a 3D Scene

Use `ThreeDScene` instead of `Scene`:

```python
from maniml import *

class My3DScene(ThreeDScene):
    def construct(self):
        # Your 3D content here
        pass
```

### Basic 3D Objects

```python
# Sphere
sphere = Sphere(radius=1, color=BLUE)

# Cube
cube = Cube(side_length=2, color=RED)

# Cylinder
cylinder = Cylinder(radius=0.5, height=2, color=GREEN)

# Cone
cone = Cone(base_radius=1, height=2, color=YELLOW)

# Torus (donut)
torus = Torus(major_radius=1, minor_radius=0.3)
```

### 3D Positioning

```python
# Position in 3D space
sphere.shift(LEFT * 2 + UP * 1 + OUT * 0.5)

# Or use explicit coordinates
cube.move_to([1, -1, 0.5])  # [x, y, z]
```

### Key Concepts

- **OUT/IN**: Z-axis directions (toward/away from viewer)
- **3D Axes**: ThreeDAxes for coordinate systems
- **Camera Control**: Moving viewpoint around scene

### Exercise

Create a 3D scene with:
1. A blue sphere at the origin
2. A red cube to the right
3. A green cylinder above
4. Rotate the camera to view from different angles

## Lesson 2: Camera Movement

Control the camera to create dynamic views.

### Running the Example

```bash
maniml 02_camera_movement.py CameraMovement
```

### Camera Controls

```python
# Rotate camera
self.play(
    self.frame.animate.rotate(angle=PI/4, axis=UP),
    run_time=2
)

# Move camera position
self.play(
    self.frame.animate.shift(RIGHT * 2)
)

# Zoom in/out
self.play(
    self.frame.animate.scale(0.5)  # Zoom in
)
```

### Camera Angles

Common viewing angles:

```python
# Isometric view
self.set_camera_orientation(
    phi=70 * DEGREES,
    theta=-45 * DEGREES
)

# Top-down view
self.set_camera_orientation(phi=0, theta=0)

# Side view
self.set_camera_orientation(phi=90 * DEGREES, theta=0)
```

### Fixed Objects

Keep objects fixed while camera moves:

```python
title = Text("3D Demo")
title.fix_in_frame()  # Won't rotate with camera
self.add(title)
```

### Exercise

Create a camera tour:
1. Start with front view
2. Rotate around the objects
3. Zoom in on specific object
4. Pull back to show everything

## Lesson 3: Surface Plots

Create mathematical surfaces in 3D.

### Running the Example

```bash
maniml 03_surface_plots.py SurfacePlots
```

### Parametric Surfaces

```python
# Create a parametric surface
surface = ParametricSurface(
    lambda u, v: np.array([
        u,
        v,
        np.sin(u) * np.cos(v)
    ]),
    u_range=[-3, 3],
    v_range=[-3, 3],
    resolution=(30, 30)
)
```

### Function Surfaces

Plot z = f(x, y):

```python
# Create axes
axes = ThreeDAxes(
    x_range=[-5, 5, 1],
    y_range=[-5, 5, 1],
    z_range=[-2, 2, 0.5]
)

# Plot surface
def func(x, y):
    return np.sin(x) * np.cos(y)

surface = axes.plot_surface(
    func,
    x_range=[-4, 4],
    y_range=[-4, 4],
    resolution=(20, 20),
    color=BLUE
)
```

### Surface Properties

```python
# Adjust appearance
surface.set_fill_by_gradient(BLUE, GREEN)
surface.set_opacity(0.8)
surface.set_sheen(0.3, DOWN)

# Add mesh lines
surface.set_stroke(WHITE, width=0.5)
```

### Exercise

Create visualizations for:
1. A saddle surface: z = x² - y²
2. A paraboloid: z = x² + y²
3. A wave: z = sin(√(x² + y²))

## Advanced 3D Techniques

### Combining 2D and 3D

```python
# 2D text in 3D scene
equation = MathTex(r"z = x^2 + y^2")
equation.fix_in_frame()
equation.to_corner(UL)
self.add(equation)
```

### 3D Transformations

```python
# Rotate around axis
self.play(
    Rotate(cube, angle=2*PI, axis=UP, run_time=3)
)

# Complex transformation
self.play(
    cube.animate.rotate(PI/2, axis=RIGHT)
                .shift(UP * 2)
                .scale(0.5)
)
```

### 3D Vectors

```python
# Create 3D vectors
vector = Arrow3D(
    start=ORIGIN,
    end=[1, 1, 1],
    color=RED
)

# Vector field
def vector_func(point):
    x, y, z = point
    return np.array([y, -x, 0]) * 0.1

vector_field = VectorField(
    vector_func,
    x_range=[-2, 2],
    y_range=[-2, 2],
    z_range=[-1, 1]
)
```

### 3D Animations

```python
# Animate along path
path = ParametricCurve(
    lambda t: np.array([
        np.cos(t),
        np.sin(t),
        t / (2 * PI)
    ]),
    t_range=[0, 4 * PI]
)

self.play(
    MoveAlongPath(sphere, path),
    run_time=5
)
```

## Performance Tips

1. **Resolution**: Lower resolution for faster rendering
2. **Opacity**: Transparent objects render slower
3. **Camera Moves**: Smooth camera moves look better than jumps

## Common Patterns

### 3D Scene Setup

```python
class Standard3DScene(ThreeDScene):
    def construct(self):
        # Setup
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Add axes
        axes = ThreeDAxes()
        self.add(axes)
        
        # Add title
        title = Text("3D Visualization")
        title.fix_in_frame()
        title.to_edge(UP)
        self.add(title)
        
        # Your content here
```

### Interactive 3D

Combine with interactive features:

```python
# Draggable 3D object (in 2D projection)
sphere = Sphere(radius=0.5)
draggable = MotionMobject(sphere)

# Update position based on mouse
def update_3d_position(mob):
    x, y = self.mouse_position[:2]
    mob.move_to([x, y, 0])

sphere.add_updater(update_3d_position)
```

## Debugging 3D Scenes

1. **Add Reference Objects**: Use axes or grid
2. **Check Camera**: Print camera position/orientation
3. **Simplify**: Start with one object, add complexity
4. **Use Colors**: Different colors help distinguish objects

## Next Steps

- Explore [Advanced Techniques](../04_advanced_techniques/README.md)
- Combine 3D with interactive features
- Create mathematical visualizations
- Build physics simulations

## Project Ideas

1. **3D Function Explorer**: Interactive surface plotter
2. **Vector Calculus**: Visualize gradients, divergence, curl
3. **Molecular Models**: Animate chemical structures
4. **Solar System**: Planetary motion simulation
5. **3D Fractals**: Recursive 3D structures

Remember: 3D adds depth to mathematical understanding!