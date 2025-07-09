from maniml import *

class TestReplayFix(Scene):
    def construct(self):
        # Simple test case
        circle = Circle(color=BLUE)
        
        print("Animation 1: Create circle")
        self.play(Create(circle))
        
        print("Animation 2: Move right and scale")  
        self.play(circle.animate.shift(RIGHT * 2).scale(2))
        
        print("Animation 3: Move up")
        self.play(circle.animate.shift(UP * 2))
        
        self.wait()
        
        print("\nTest instructions:")
        print("1. Go back to start (LEFT arrow)")
        print("2. Play animation 2 (RIGHT arrow)")
        print("3. It should ONLY move right and scale, NOT move up")