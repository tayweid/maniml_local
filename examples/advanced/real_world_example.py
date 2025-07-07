#!/usr/bin/env python3
"""Practical example showing real-world usage of maniml."""

from maniml import *


class PracticalExample(Scene):
    """A practical math visualization using various animations."""
    
    def construct(self):
        # Title sequence
        title = Text("Function Transformations", font_size=56)
        subtitle = Text("Using maniml (CE API on GL Backend)", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Create coordinate system
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(axes_labels))
        
        # Original function
        def func1(x):
            return x**2
        
        graph1 = axes.plot(func1, x_range=[-2, 2], color=BLUE)
        graph1_label = MathTex("f(x) = x^2", color=BLUE).next_to(graph1, UP)
        
        self.play(Create(graph1))
        self.play(FadeIn(graph1_label, shift=DOWN))
        self.wait()
        
        # Transform to new function
        def func2(x):
            return (x - 1)**2 + 1
        
        graph2 = axes.plot(func2, x_range=[-1, 3], color=RED)
        graph2_label = MathTex("g(x) = (x-1)^2 + 1", color=RED)
        graph2_label.next_to(graph2, UP)
        
        self.play(
            Transform(graph1, graph2),
            Transform(graph1_label, graph2_label)
        )
        self.wait()
        
        # Show the transformation steps
        step_text = Text("Shift right 1, up 1", font_size=36, color=YELLOW)
        step_text.to_edge(DOWN)
        self.play(FadeIn(step_text, shift=UP))
        
        # Highlight the vertex
        vertex_dot = Dot(axes.coords_to_point(1, 1), color=YELLOW, radius=0.1)
        self.play(GrowFromCenter(vertex_dot))
        self.play(Flash(vertex_dot, color=YELLOW, line_length=0.3))
        
        # Add derivative
        self.play(FadeOut(step_text))
        
        derivative_text = MathTex("g'(x) = 2(x-1)", color=GREEN)
        derivative_text.to_edge(DOWN)
        self.play(Write(derivative_text))
        
        # Show tangent line at x=2
        x_val = 2
        y_val = func2(x_val)
        slope = 2 * (x_val - 1)
        
        tangent_line = axes.plot(
            lambda x: slope * (x - x_val) + y_val,
            x_range=[0.5, 3],
            color=GREEN
        )
        
        tangent_dot = Dot(axes.coords_to_point(x_val, y_val), color=GREEN, radius=0.08)
        
        self.play(Create(tangent_line), FadeIn(tangent_dot))
        self.play(Indicate(tangent_line))
        
        # Show area under curve
        area = axes.get_area(graph1, x_range=[0, 2], color=BLUE, opacity=0.3)
        area_text = MathTex(r"\int_0^2 g(x)\,dx", color=BLUE).next_to(area, RIGHT)
        
        self.play(FadeIn(area), Write(area_text))
        self.wait()
        
        # Clean transition to new topic
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Demonstrate geometric transformations
        self.demonstrate_geometric_transforms()
        
    def demonstrate_geometric_transforms(self):
        """Show geometric transformations."""
        title = Text("Geometric Transformations", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Create shapes
        shapes = VGroup(
            Circle(radius=0.5, color=BLUE),
            Square(side_length=1, color=RED),
            Triangle(color=GREEN)
        ).arrange(RIGHT, buff=1)
        
        self.play(AnimationGroup(
            *[GrowFromCenter(shape) for shape in shapes],
            lag_ratio=0.2
        ))
        
        # Label them
        labels = VGroup(
            Text("Circle", font_size=24),
            Text("Square", font_size=24),
            Text("Triangle", font_size=24)
        )
        
        for label, shape in zip(labels, shapes):
            label.next_to(shape, DOWN)
        
        self.play(AnimationGroup(
            *[FadeIn(label, shift=UP) for label in labels],
            lag_ratio=0.1
        ))
        
        # Apply transformations
        transform_text = Text("Applying Transformations...", font_size=36, color=YELLOW)
        transform_text.next_to(shapes, DOWN, buff=1)
        self.play(Write(transform_text))
        
        # Rotation
        self.play(
            Rotate(shapes[0], angle=PI/2),
            Rotate(shapes[1], angle=PI/4),
            Rotate(shapes[2], angle=-PI/3),
        )
        
        # Scaling
        self.play(
            Scale(shapes[0], 1.5),
            Scale(shapes[1], 0.7),
            Scale(shapes[2], 1.2),
        )
        
        # Color morphing with indication
        self.play(
            shapes[0].animate.set_color(PURPLE),
            shapes[1].animate.set_color(ORANGE),
            shapes[2].animate.set_color(PINK),
        )
        
        self.play(
            *[Wiggle(shape) for shape in shapes]
        )
        
        # Final flourish
        self.play(
            *[Circumscribe(shape, color=YELLOW) for shape in shapes]
        )
        
        final_text = Text("maniml: Fast & Familiar!", font_size=48, color=GOLD)
        self.play(
            FadeOut(shapes),
            FadeOut(labels),
            FadeOut(transform_text),
            ReplacementTransform(title, final_text)
        )
        
        self.play(final_text.animate.scale(1.2))
        self.wait(2)