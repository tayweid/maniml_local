from maniml import *

class TestTwoExec(Scene):
    def construct(self):
        print("[TEST] Starting construct")
        
        # Animation 1: Create circle
        print("[TEST] Creating circle")
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        print(f"[TEST] Circle created, id: {id(circle)}")
        
        # Animation 2: Create square  
        print("[TEST] Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        print(f"[TEST] Square created, id: {id(square)}")
        
        print("\n[TEST] Press ← to go back to checkpoint 0")
        print("[TEST] Then press → to play forward")
        print("[TEST] Watch for duplicate objects")