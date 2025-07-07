"""Comprehensive edge case tests for maniml"""

from maniml import *
import numpy as np

class Test1_BasicShapes(Scene):
    """Test basic shape creation and animation"""
    def construct(self):
        title = Text("Test 1: Basic Shapes", font_size=24).to_edge(UP)
        self.add(title)
        
        # Test various shapes
        shapes = VGroup(
            Circle(radius=0.5, color=BLUE),
            Square(side_length=1, color=RED),
            Rectangle(width=1.5, height=0.8, color=GREEN),
            Triangle(color=YELLOW),
            RegularPolygon(n=5, color=PURPLE),
            Dot(radius=0.1, color=WHITE),
            Ellipse(width=1.2, height=0.6, color=ORANGE),
        ).arrange_in_grid(2, 4, buff=0.5)  # n_rows, n_cols
        
        self.play(Create(shapes, lag_ratio=0.1))
        self.wait()


class Test2_Animations(Scene):
    """Test various animation types"""
    def construct(self):
        title = Text("Test 2: Animations", font_size=24).to_edge(UP)
        self.add(title)
        
        circle = Circle(color=BLUE)
        
        # Test different animations
        self.play(Create(circle))
        self.play(circle.animate.scale(2))
        self.play(circle.animate.shift(RIGHT * 2))
        self.play(Rotate(circle, PI))
        self.play(circle.animate.set_color(RED))
        self.play(FadeOut(circle))
        
        # Test transform
        square = Square(color=GREEN)
        triangle = Triangle(color=YELLOW)
        self.play(FadeIn(square))
        self.play(Transform(square, triangle))
        self.wait()


class Test3_Text(Scene):
    """Test text rendering"""
    def construct(self):
        title = Text("Test 3: Text Rendering", font_size=24).to_edge(UP)
        self.add(title)
        
        # Various text styles
        texts = VGroup(
            Text("Regular text"),
            Text("Bold text", weight=BOLD),
            Text("Italic text", slant=ITALIC),
            Text("Small text", font_size=20),
            Text("Large text", font_size=40),
            Text("Colored text", color=BLUE),
        ).arrange(DOWN, buff=0.3)
        
        self.play(Write(texts, lag_ratio=0.2))
        self.wait()


class Test4_LaTeX(Scene):
    """Test LaTeX rendering"""
    def construct(self):
        title = Text("Test 4: LaTeX", font_size=24).to_edge(UP)
        self.add(title)
        
        # Math expressions
        equations = VGroup(
            MathTex(r"x^2 + y^2 = r^2"),
            MathTex(r"\int_0^\infty e^{-x} dx = 1"),
            MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}"),
            MathTex(r"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}"),
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(equations, lag_ratio=0.3))
        self.wait()


class Test5_Interactive(Scene):
    """Test interactive features"""
    def construct(self):
        title = Text("Test 5: Interactive Objects", font_size=24).to_edge(UP)
        self.add(title)
        
        # MotionMobject
        circle = Circle(radius=0.5, color=BLUE)
        circle.shift(LEFT * 3)
        draggable = MotionMobject(circle)
        
        # Button
        button_rect = Rectangle(width=2, height=0.8, color=GREEN)
        button_text = Text("Click Me!", font_size=20)
        button_group = VGroup(button_rect, button_text)
        
        click_count = 0
        def on_click(mob):
            nonlocal click_count
            click_count += 1
            colors = [GREEN, RED, BLUE, YELLOW]
            button_rect.set_color(colors[click_count % len(colors)])
        
        button = Button(button_group, on_click=on_click)
        
        # Slider
        slider = LinearNumberSlider(
            value=5, min_value=0, max_value=10,
            rounded_rect_kwargs={"width": 3}
        ).shift(RIGHT * 2)
        
        self.add(draggable, button, slider)
        
        instructions = Text("Drag circle, click button, move slider", font_size=16).to_edge(DOWN)
        self.add(instructions)
        
        self.embed()


class Test6_CoordinateSystems(Scene):
    """Test coordinate systems"""
    def construct(self):
        title = Text("Test 6: Coordinate Systems", font_size=24).to_edge(UP)
        self.add(title)
        
        # NumberLine
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
        ).shift(UP * 2)
        
        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
        ).shift(DOWN * 1.5)
        
        # Plot function
        graph = axes.plot(lambda x: x**2 - 1, x_range=[-2, 2], color=BLUE)
        
        self.play(Create(number_line))
        self.play(Create(axes))
        self.play(Create(graph))
        self.wait()


class Test7_3DScene(ThreeDScene):
    """Test 3D rendering"""
    def construct(self):
        title = Text("Test 7: 3D Scene", font_size=24).to_edge(UP)
        # In ManimGL, use fix_in_frame instead
        title.fix_in_frame()
        self.add(title)
        
        # 3D objects
        sphere = Sphere(radius=1, color=BLUE)
        cube = Cube(side_length=1.5, color=RED)
        cylinder = Cylinder(radius=0.5, height=2, color=GREEN)
        
        sphere.shift(LEFT * 3)
        cube.shift(ORIGIN)
        cylinder.shift(RIGHT * 3)
        
        self.play(Create(sphere), Create(cube), Create(cylinder))
        
        # Rotate camera - use frame instead of camera in ManimGL
        self.play(self.frame.animate.rotate(PI/4, axis=UP), run_time=2)
        self.wait(2)


class Test8_VGroup(Scene):
    """Test VGroup operations"""
    def construct(self):
        title = Text("Test 8: VGroup Operations", font_size=24).to_edge(UP)
        self.add(title)
        
        # Create group
        circles = VGroup(*[
            Circle(radius=0.3, color=color)
            for color in [RED, GREEN, BLUE, YELLOW]
        ])
        circles.arrange(RIGHT, buff=0.5)
        
        self.play(Create(circles))
        self.play(circles.animate.scale(1.5))
        self.play(circles.animate.arrange(DOWN))
        self.play(circles.animate.arrange_in_grid(2, 2))  # n_rows, n_cols
        self.wait()


class Test9_Updaters(Scene):
    """Test updater functions"""
    def construct(self):
        title = Text("Test 9: Updaters", font_size=24).to_edge(UP)
        self.add(title)
        
        # Value tracker
        tracker = ValueTracker(0)
        
        # Number that updates
        number = DecimalNumber(0).scale(2)
        number.add_updater(lambda m: m.set_value(tracker.get_value()))
        
        # Circle that changes size
        circle = Circle(color=BLUE)
        circle.add_updater(lambda m: m.set_width(tracker.get_value() + 1))
        
        self.add(number, circle)
        self.play(tracker.animate.set_value(5), run_time=3)
        self.wait()


class Test10_EdgeCases(Scene):
    """Test edge cases and potential errors"""
    def construct(self):
        title = Text("Test 10: Edge Cases", font_size=24).to_edge(UP)
        self.add(title)
        
        # Empty VGroup
        empty_group = VGroup()
        self.play(Create(empty_group))  # Should not crash
        
        # Very small object
        tiny_dot = Dot(radius=0.001)
        self.play(Create(tiny_dot))
        
        # Zero-duration animation
        circle = Circle()
        self.play(Create(circle), run_time=0)
        
        # Negative scaling
        square = Square()
        self.play(Create(square))
        self.play(square.animate.scale(-1))  # Should flip
        
        # Very large number
        big_text = Text(str(10**100), font_size=12)
        self.play(Write(big_text))
        
        self.wait()


class TestAll(Scene):
    """Run all tests in sequence"""
    def construct(self):
        tests = [
            ("Basic Shapes", Test1_BasicShapes),
            ("Animations", Test2_Animations),
            ("Text", Test3_Text),
            ("LaTeX", Test4_LaTeX),
            ("Interactive", Test5_Interactive),
            ("Coordinates", Test6_CoordinateSystems),
            ("3D Scene", Test7_3DScene),
            ("VGroup", Test8_VGroup),
            ("Updaters", Test9_Updaters),
            ("Edge Cases", Test10_EdgeCases),
        ]
        
        for i, (name, test_class) in enumerate(tests):
            print(f"\n{'='*50}")
            print(f"Running Test {i+1}: {name}")
            print('='*50)
            
            try:
                if name == "3D Scene":
                    # Skip 3D test in this combined run
                    print("Skipping 3D test in combined run")
                    continue
                
                # Run the test
                scene = test_class()
                scene.construct()
                print(f"✓ Test {i+1} passed: {name}")
            except Exception as e:
                print(f"✗ Test {i+1} failed: {name}")
                print(f"  Error: {e}")
                import traceback
                traceback.print_exc()


# Individual test runners
if __name__ == "__main__":
    print("Run individual tests with:")
    print("  maniml test_edge_cases.py Test1_BasicShapes")
    print("  maniml test_edge_cases.py Test2_Animations")
    print("  etc...")
    print("\nOr run all tests with:")
    print("  maniml test_edge_cases.py TestAll")