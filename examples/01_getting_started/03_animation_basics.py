"""
Animation Basics - Common Animation Types

This example demonstrates the fundamental animation types available in maniml.
Learn how to create, transform, and animate objects in various ways.

Run with: maniml examples/basic/03_animation_basics.py AnimationBasics
"""

from maniml import *

class AnimationBasics(Scene):
    def construct(self):
        # Title
        title = Text("Animation Types", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # 1. Create Animation
        create_label = Text("Create", font_size=24).shift(LEFT * 5 + UP * 2)
        circle1 = Circle(color=BLUE).shift(LEFT * 5)
        
        self.play(Write(create_label))
        self.play(Create(circle1))
        self.wait(0.5)
        
        # 2. FadeIn/FadeOut
        fade_label = Text("Fade", font_size=24).shift(LEFT * 2.5 + UP * 2)
        square1 = Square(color=RED).shift(LEFT * 2.5)
        
        self.play(Write(fade_label))
        self.play(FadeIn(square1, shift=UP))
        self.wait(0.5)
        self.play(FadeOut(square1, shift=DOWN))
        self.play(FadeIn(square1))
        
        # 3. Transform
        transform_label = Text("Transform", font_size=24).shift(UP * 2)
        shape1 = Circle(color=GREEN)
        shape2 = Square(color=GREEN)
        
        self.play(Write(transform_label))
        self.play(Create(shape1))
        self.wait(0.5)
        self.play(Transform(shape1, shape2))
        
        # 4. Rotate
        rotate_label = Text("Rotate", font_size=24).shift(RIGHT * 2.5 + UP * 2)
        triangle1 = Triangle(color=YELLOW).shift(RIGHT * 2.5)
        
        self.play(Write(rotate_label))
        self.play(Create(triangle1))
        self.play(Rotate(triangle1, angle=2*PI))
        
        # 5. Scale
        scale_label = Text("Scale", font_size=24).shift(RIGHT * 5 + UP * 2)
        hex1 = RegularPolygon(6, color=PURPLE).shift(RIGHT * 5).scale(0.5)
        
        self.play(Write(scale_label))
        self.play(Create(hex1))
        self.play(hex1.animate.scale(2))
        self.play(hex1.animate.scale(0.5))
        
        self.wait()
        
        # 6. Complex animations
        complex_label = Text("Complex Animations", font_size=24)
        complex_label.next_to(title, DOWN)
        
        self.play(
            FadeOut(VGroup(create_label, fade_label, transform_label, 
                          rotate_label, scale_label)),
            Write(complex_label)
        )
        
        # Move all shapes to center
        all_shapes = VGroup(circle1, square1, shape1, triangle1, hex1)
        self.play(all_shapes.animate.arrange(RIGHT, buff=0.5).shift(DOWN))
        
        # Simultaneous animations
        self.play(
            circle1.animate.set_color(PINK).shift(UP),
            square1.animate.rotate(PI/4).scale(1.5),
            shape1.animate.set_fill(BLUE, opacity=0.5),
            triangle1.animate.flip(),
            hex1.animate.rotate(PI).set_stroke(WHITE, width=5),
            run_time=2
        )
        
        self.wait(2)