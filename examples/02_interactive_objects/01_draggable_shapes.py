"""
Draggable Shapes - Interactive Objects

This example shows how to create draggable objects using MotionMobject.
Click and drag the shapes around the screen!

Run with: maniml examples/interactive/01_draggable_shapes.py DraggableShapes
"""

from maniml import *

class DraggableShapes(Scene):
    def construct(self):
        # Create title
        title = Text("Drag the shapes!", font_size=32)
        title.to_edge(UP)
        self.add(title)
        
        # Create instructions
        instructions = Text(
            "Click and drag to move shapes. Press 'q' to quit.",
            font_size=16
        )
        instructions.to_edge(DOWN)
        self.add(instructions)
        
        # Create draggable shapes
        shapes = VGroup()
        
        # Draggable circle
        circle = Circle(radius=0.8, color=BLUE, fill_opacity=0.7)
        circle.shift(LEFT * 3)
        draggable_circle = MotionMobject(circle)
        shapes.add(draggable_circle)
        
        # Draggable square
        square = Square(side_length=1.5, color=RED, fill_opacity=0.7)
        draggable_square = MotionMobject(square)
        shapes.add(draggable_square)
        
        # Draggable triangle
        triangle = Triangle(color=GREEN, fill_opacity=0.7)
        triangle.scale(1.2).shift(RIGHT * 3)
        draggable_triangle = MotionMobject(triangle)
        shapes.add(draggable_triangle)
        
        # Add labels to shapes
        circle_label = Text("Circle", font_size=20)
        circle_label.move_to(circle)
        circle.add(circle_label)
        
        square_label = Text("Square", font_size=20)
        square_label.move_to(square)
        square.add(square_label)
        
        triangle_label = Text("Triangle", font_size=20)
        triangle_label.move_to(triangle)
        triangle.add(triangle_label)
        
        # Animate shapes appearing
        self.play(
            LaggedStart(
                *[FadeIn(shape, scale=0.5) for shape in shapes],
                lag_ratio=0.2
            )
        )
        
        # Enter interactive mode
        self.embed()