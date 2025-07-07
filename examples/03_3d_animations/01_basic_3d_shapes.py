"""
Basic 3D Shapes - Introduction to 3D Scenes

This example demonstrates how to create and animate 3D objects in maniml.

Run with: maniml examples/3d/01_basic_3d_shapes.py Basic3DShapes
"""

from maniml import *

class Basic3DShapes(ThreeDScene):
    def construct(self):
        # Create title (fixed in frame so it doesn't rotate)
        title = Text("3D Shapes in maniml", font_size=36)
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        self.play(Create(axes))
        
        # Create 3D shapes
        sphere = Sphere(radius=0.8, color=BLUE)
        sphere.shift(LEFT * 2)
        
        cube = Cube(side_length=1.2, color=RED)
        
        cylinder = Cylinder(radius=0.6, height=1.5, color=GREEN)
        cylinder.shift(RIGHT * 2)
        
        cone = Cone(base_radius=0.7, height=1.5, color=YELLOW)
        cone.shift(UP * 2)
        
        # Add shapes
        self.play(
            Create(sphere),
            Create(cube),
            Create(cylinder),
            Create(cone),
            run_time=3
        )
        
        self.wait()
        
        # Rotate camera around the scene
        self.play(
            self.frame.animate.rotate(angle=PI/4, axis=UP),
            run_time=2
        )
        
        self.play(
            self.frame.animate.rotate(angle=PI/6, axis=RIGHT),
            run_time=2
        )
        
        # Animate the shapes
        self.play(
            sphere.animate.shift(UP),
            cube.animate.rotate(PI/2, axis=UP),
            cylinder.animate.scale(1.5),
            cone.animate.shift(DOWN * 2),
            run_time=2
        )
        
        self.wait()
        
        # Full rotation
        self.play(
            self.frame.animate.rotate(angle=2*PI, axis=UP),
            run_time=5
        )
        
        self.wait()