from maniml import *

class TestLineTracking(Scene):
    def construct(self):
        print("\n=== Testing Line Tracking ===")
        
        # Animation 1 on line 8
        circle = Circle(color=BLUE)
        self.play(Create(circle))  # Line 9
        
        # Animation 2 starts on line 13
        square = Square(color=RED)
        self.play(
            Create(square),  # Line 14
            circle.animate.shift(LEFT)  # Line 15
        )  # Line 16
        
        # Animation 3 on line 19
        self.play(circle.animate.scale(2))
        
        # Animation 4 starts on line 23
        triangle = Triangle(color=YELLOW)
        self.play(
            Create(triangle),
            run_time=2
        )  # Line 26
        
        print("Use arrow keys to navigate!")
        self.interactive_embed()