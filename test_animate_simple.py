from maniml import *

class TestAnimateSimple(Scene):
    def construct(self):
        # Simple test for .animate syntax
        circle = Circle(color=BLUE)
        
        # Animation 1: Create
        self.play(Create(circle))
        
        # Animation 2: Simple .animate
        self.play(circle.animate.shift(RIGHT * 2))
        
        # Animation 3: Normal animation
        self.play(FadeOut(circle))
        
        print("\n✅ Simple .animate test ready!")
        print("Test sequence:")
        print("1. Play all animations (→ →)")
        print("2. Jump back to checkpoint 1 (←)")
        print("3. Play forward (→) - should replay .animate")