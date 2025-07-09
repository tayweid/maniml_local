from maniml import *

class TestAnimationReplay(Scene):
    def construct(self):
        # Create a circle and square
        circle = Circle(color=BLUE).shift(LEFT * 2)
        square = Square(color=RED).shift(RIGHT * 2)
        
        print("Initial positions:")
        print(f"  Circle: {circle.get_center()}")
        print(f"  Square: {square.get_center()}")
        
        self.play(Create(circle), Create(square))
        
        # Move them to the center
        print("\nBefore move animations:")
        print(f"  Circle: {circle.get_center()}")
        print(f"  Square: {square.get_center()}")
        
        self.play(
            circle.animate.move_to(ORIGIN),
            square.animate.move_to(ORIGIN)
        )
        
        print("\nAfter move animations:")
        print(f"  Circle: {circle.get_center()}")
        print(f"  Square: {square.get_center()}")
        
        # Transform circle into square
        self.play(Transform(circle, square))
        
        print("\nAfter transform:")
        print(f"  Circle: {circle.get_center()}")
        
        # Scale and rotate
        self.play(
            circle.animate.scale(2).rotate(PI/4)
        )
        
        print("\nAfter scale/rotate:")
        print(f"  Circle: {circle.get_center()}")
        
        self.wait()
        
        print("\n" + "="*50)
        print("Test navigation:")
        print("1. Press LEFT to go back to the beginning")
        print("2. Press RIGHT to replay animations")
        print("3. Check that positions match the printed values")
        print("="*50)