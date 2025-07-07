"""Test 3D surfaces specifically."""

from maniml import *
import numpy as np

class TestSimpleSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Create axes for reference
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1]
        )
        self.add(axes)
        
        # Method 1: Create a sphere using built-in
        sphere = Sphere(radius=1, color=BLUE)
        sphere.shift(2*LEFT)
        self.add(sphere)
        
        # Method 2: Create a torus
        torus = Torus(major_radius=1, minor_radius=0.3, color=RED)
        torus.shift(2*RIGHT)
        self.add(torus)
        
        # Animate - add ambient rotation
        self.frame.add_ambient_rotation(angular_speed=0.2)
        self.wait(3)
        self.frame.clear_updaters()  # Stop rotation
        
        self.wait()


class TestParametricSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES)
        
        # Note: In ManimGL, parametric surfaces are created differently
        # For now, we'll use the built-in 3D shapes
        
        # Create a variety of 3D shapes
        shapes = [
            Sphere(radius=0.5, color=BLUE).shift(2*LEFT + UP),
            Cube(side_length=1, color=RED).shift(2*RIGHT + UP),
            Cylinder(radius=0.5, height=1, color=GREEN).shift(2*LEFT + DOWN),
            Cone(base_radius=0.5, height=1, color=YELLOW).shift(2*RIGHT + DOWN),
        ]
        
        for shape in shapes:
            self.add(shape)
        
        # Animate all together
        self.play(
            *[Rotate(shape, angle=2*PI, axis=UP, run_time=3) for shape in shapes]
        )
        
        self.wait()


class TestComplexSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Create a grid of 3D objects
        grid = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (i + j) % 2 == 0:
                    obj = Sphere(radius=0.2, color=BLUE)
                else:
                    obj = Cube(side_length=0.3, color=RED)
                obj.shift(i*RIGHT + j*UP)
                grid.append(obj)
        
        # Add all at once
        for obj in grid:
            self.add(obj)
        
        # Wave animation
        for i, obj in enumerate(grid):
            obj.shift(0.5 * np.sin(i * 0.3) * OUT)
        
        # Rotate camera
        self.frame.add_ambient_rotation(angular_speed=0.3)
        self.wait(4)
        self.frame.clear_updaters()  # Stop rotation
        
        self.wait()