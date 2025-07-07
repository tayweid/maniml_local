"""
Shapes and Colors - Basic Geometric Objects

Learn how to create and style basic shapes in maniml.
This example demonstrates circles, squares, triangles, and more.

Run with: maniml examples/basic/02_shapes_and_colors.py ShapesAndColors
"""

from maniml import *

class ShapesAndColors(Scene):
    def construct(self):
        # Create title
        title = Text("Shapes and Colors", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create various shapes with different colors
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=2, color=RED, fill_opacity=0.5)
        triangle = Triangle(color=GREEN, fill_opacity=0.5)
        
        # Position shapes
        circle.shift(LEFT * 3)
        triangle.shift(RIGHT * 3)
        
        # Animate shapes appearing
        self.play(
            Create(circle),
            Create(square),
            Create(triangle),
            run_time=2
        )
        
        self.wait()
        
        # Transform shapes
        self.play(
            circle.animate.set_fill(YELLOW, opacity=0.8),
            square.animate.rotate(PI/4).scale(0.8),
            triangle.animate.shift(DOWN).set_stroke(PURPLE, width=5),
            run_time=2
        )
        
        self.wait()
        
        # Create more complex shapes
        star = Star(n=5, outer_radius=1, color=ORANGE)
        hexagon = RegularPolygon(n=6, color=PINK)
        
        star.next_to(circle, DOWN, buff=1)
        hexagon.next_to(triangle, DOWN, buff=1)
        
        self.play(
            FadeIn(star, shift=UP),
            FadeIn(hexagon, shift=UP)
        )
        
        self.wait(2)