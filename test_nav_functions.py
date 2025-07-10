from maniml import *

class TestNavFunctions(Scene):
    def construct(self):
        print("\n=== Testing jump_to_n and play_n functions ===")
        
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
        
        print("\n[TEST] Navigation Instructions:")
        print("← : Jump to previous state (no animation)")
        print("→ : Play next animation")
        print("↑ : Jump to previous state (no animation)")  
        print("↓ : Jump to next state (no animation)")
        print("\nTry: ← to go back, then → to play forward")