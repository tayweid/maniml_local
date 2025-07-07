"""Specific edge case tests for maniml compatibility"""

from maniml import *
import numpy as np

class TestAPICompatibility(Scene):
    """Test API differences between ManimCE and ManimGL"""
    def construct(self):
        results = []
        
        # Test 1: arrange_in_grid parameters
        try:
            shapes = VGroup(*[Circle(radius=0.2) for _ in range(6)])
            shapes.arrange_in_grid(2, 3)  # ManimGL style: n_rows, n_cols
            self.add(shapes)
            results.append("✓ arrange_in_grid works with n_rows, n_cols")
        except Exception as e:
            results.append(f"✗ arrange_in_grid: {e}")
        
        self.clear()
        
        # Test 2: Text weight parameter
        try:
            bold_text = Text("Bold", weight=BOLD)
            self.add(bold_text)
            results.append("✓ Text weight parameter works")
        except Exception as e:
            results.append(f"✗ Text weight: {e}")
            
        self.clear()
        
        # Test 3: Animation lag_ratio
        try:
            circles = VGroup(*[Circle(radius=0.2) for _ in range(3)]).arrange(RIGHT)
            self.play(Create(circles, lag_ratio=0.5))
            results.append("✓ lag_ratio in animations works")
        except Exception as e:
            results.append(f"✗ lag_ratio: {e}")
            
        self.clear()
        
        # Show results
        result_text = VGroup(*[
            Text(result, font_size=20, color=GREEN if result.startswith("✓") else RED)
            for result in results
        ]).arrange(DOWN, aligned_edge=LEFT)
        self.add(result_text)
        self.wait(2)


class TestColorHandling(Scene):
    """Test color parameter handling"""
    def construct(self):
        # Test various color formats
        colors_to_test = [
            ("Hex string", "#FF0000", Circle),
            ("Color constant", RED, Square),
            ("RGB tuple", (0, 1, 0), Triangle),
            ("RGBA tuple", (0, 0, 1, 0.5), RegularPolygon),
            ("Named color", "yellow", Dot),
        ]
        
        shapes = VGroup()
        for i, (name, color, shape_class) in enumerate(colors_to_test):
            try:
                if shape_class == RegularPolygon:
                    shape = shape_class(n=6, color=color)
                elif shape_class == Dot:
                    shape = shape_class(radius=0.2, color=color)
                else:
                    shape = shape_class(color=color)
                shape.scale(0.5)
                shapes.add(shape)
            except Exception as e:
                print(f"Color test failed for {name}: {e}")
                # Add placeholder
                shapes.add(Square(color=GREY).scale(0.5))
        
        shapes.arrange(RIGHT, buff=0.5)
        self.play(Create(shapes))
        self.wait()


class TestTransformEdgeCases(Scene):
    """Test transform edge cases"""
    def construct(self):
        # Test 1: Transform between different mobject types
        circle = Circle(color=BLUE)
        tex = MathTex("x^2", color=RED)
        
        self.play(Create(circle))
        self.play(Transform(circle, tex))  # Should work
        self.wait()
        
        # Test 2: Transform with mismatched point counts
        line = Line(LEFT, RIGHT)
        triangle = Triangle()
        
        self.play(Transform(circle, line))
        self.play(Transform(circle, triangle))
        self.wait()


class TestEmptyObjects(Scene):
    """Test handling of empty objects"""
    def construct(self):
        # Empty VGroup
        empty_vgroup = VGroup()
        self.play(Create(empty_vgroup))  # Should not crash
        
        # VGroup with None elements (filtered out)
        mixed_group = VGroup()
        mixed_group.add(Circle())
        mixed_group.add(None)  # Should be ignored
        mixed_group.add(Square())
        
        self.play(Create(mixed_group))
        self.wait()


class TestLargeNumbers(Scene):
    """Test handling of extreme values"""
    def construct(self):
        # Very large coordinates
        far_dot = Dot(point=np.array([1000, 1000, 0]))
        self.add(far_dot)  # Should be off-screen but not crash
        
        # Very small scale
        tiny_circle = Circle().scale(0.001)
        self.add(tiny_circle)
        
        # Large scale
        huge_square = Square().scale(100)
        self.add(huge_square)
        
        # Zoom to normal view
        normal_shapes = VGroup(
            Circle(color=BLUE),
            Square(color=RED),
            Triangle(color=GREEN)
        ).arrange(RIGHT)
        
        self.play(Create(normal_shapes))
        self.wait()


class TestAnimationEdgeCases(Scene):
    """Test animation edge cases"""
    def construct(self):
        circle = Circle()
        
        # Zero duration animation
        self.play(Create(circle), run_time=0)
        
        # Negative run_time (should be clamped to 0)
        try:
            self.play(circle.animate.shift(RIGHT), run_time=-1)
        except:
            pass
        
        # Very long animation (interrupted)
        self.play(circle.animate.shift(LEFT * 2), run_time=0.1)
        
        # Multiple simultaneous transforms
        square = Square(color=RED)
        triangle = Triangle(color=GREEN)
        
        self.play(
            Transform(circle, square),
            Transform(circle.copy(), triangle),  # Copy to avoid conflict
            run_time=1
        )
        self.wait()


class TestUpdaterEdgeCases(Scene):
    """Test updater edge cases"""
    def construct(self):
        # Updater that modifies the object
        circle = Circle()
        
        def bad_updater(mob, dt):
            # This could cause issues if not handled properly
            mob.scale(1 + 0.1 * dt)
            if mob.get_width() > 5:
                mob.scale(0.1)
        
        circle.add_updater(bad_updater)
        self.add(circle)
        self.wait(3)
        circle.remove_updater(bad_updater)
        
        # Updater with value tracker
        tracker = ValueTracker(0)
        number = DecimalNumber(0)
        
        def update_number(mob):
            val = tracker.get_value()
            # Edge case: very large number
            if val > 1e10:
                val = 0
            mob.set_value(val)
        
        number.add_updater(update_number)
        self.add(number)
        self.play(tracker.animate.set_value(1e11), run_time=2)
        self.wait()


class TestZIndexing(Scene):
    """Test z-index ordering"""
    def construct(self):
        # Create overlapping shapes with different z-indices
        back = Square(color=RED, fill_opacity=0.8).scale(2)
        middle = Circle(color=GREEN, fill_opacity=0.8).scale(1.5)
        front = Triangle(color=BLUE, fill_opacity=0.8)
        
        # Set z-indices
        back.set_z_index(-1)
        middle.set_z_index(0)
        front.set_z_index(1)
        
        # Add in wrong order to test z-index
        self.add(front, back, middle)
        
        # Animate to show layering
        self.play(
            back.animate.shift(LEFT),
            middle.animate.shift(ORIGIN),
            front.animate.shift(RIGHT),
        )
        self.wait()


class TestStringInputs(Scene):
    """Test string parsing in various parameters"""
    def construct(self):
        # Color strings
        circle1 = Circle(color="red")
        circle2 = Circle(color="blue")
        circle3 = Circle(color="#00FF00")
        
        shapes = VGroup(circle1, circle2, circle3).arrange(RIGHT)
        self.play(Create(shapes))
        
        # Direction strings (if supported)
        try:
            text = Text("Test").to_edge("UP")  # Might not work
        except:
            text = Text("Test").to_edge(UP)  # Fallback
        
        self.add(text)
        self.wait()


# Run all edge case tests
if __name__ == "__main__":
    tests = [
        TestAPICompatibility,
        TestColorHandling,
        TestTransformEdgeCases,
        TestEmptyObjects,
        TestLargeNumbers,
        TestAnimationEdgeCases,
        TestUpdaterEdgeCases,
        TestZIndexing,
        TestStringInputs,
    ]
    
    print("Edge case tests available:")
    for i, test in enumerate(tests):
        print(f"  {i+1}. {test.__name__}")
    
    print("\nRun with: maniml test_maniml_edge_cases.py <TestName>")