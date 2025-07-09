from maniml import *

class TestBasicCheckpoint(Scene):
    def construct(self):
        # Only use simple animations to test the recreation approach
        circle = Circle(color=BLUE)
        square = Square(color=RED).shift(RIGHT * 3)
        
        # Animation 1
        self.play(Create(circle))
        
        # Animation 2
        self.play(Create(square))
        
        # Animation 3
        self.play(FadeOut(circle), FadeOut(square))
        
        print("\n✅ Basic checkpoint test ready!")
        print("Test sequence:")
        print("1. Play all animations (→ →)")
        print("2. Jump back to start (← ←)")
        print("3. Play forward (→)")
        print("4. Jump back (←)")
        print("5. Play forward again (→)")
        print("\nThis uses only simple animations that can be recreated.")