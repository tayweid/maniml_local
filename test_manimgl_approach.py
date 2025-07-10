from maniml import *

class TestManimGLApproach(Scene):
    def construct(self):
        print("\n=== Testing ManimGL-style checkpoint navigation ===")
        
        # Animation 1
        print("Animation 1: Creating circle")
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Animation 2  
        print("Animation 2: Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        
        # Animation 3
        print("Animation 3: Moving objects")
        self.play(
            circle.animate.shift(UP),
            square.animate.shift(DOWN)
        )
        
        # Animation 4
        print("Animation 4: Scaling objects")
        self.play(
            circle.animate.scale(2),
            square.animate.scale(0.5)
        )
        
        # Animation 5
        print("Animation 5: Changing colors")
        self.play(
            circle.animate.set_color(GREEN),
            square.animate.set_color(YELLOW)
        )
        
        print("\n[TEST] Navigation Instructions:")
        print("← : Jump to previous state instantly")
        print("→ : Play next animation from restored state")
        print("↑ : Jump to previous state instantly")  
        print("↓ : Jump to next state instantly")
        print("\nTry navigating back and forth!")