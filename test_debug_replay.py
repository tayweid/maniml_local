from maniml import *

class TestDebugReplay(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE).shift(LEFT * 2)
        square = Square(color=RED).shift(RIGHT * 2)
        
        print("=== Animation 1: Create ===")
        self.play(Create(circle), Create(square))
        
        print("=== Animation 2: Move to center ===")
        self.play(
            circle.animate.move_to(ORIGIN),
            square.animate.move_to(ORIGIN)
        )
        
        print("=== Animation 3: Transform ===")
        self.play(Transform(circle, square))
        
        print("=== Animation 4: Scale ===")
        self.play(circle.animate.scale(2))
        
        self.wait()
        
        print("\nNow test:")
        print("1. Press LEFT to go back")
        print("2. Press RIGHT to see which animations play")