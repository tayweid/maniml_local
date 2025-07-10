from maniml import *

class TestIPython(Scene):
    def construct(self):
        print("\n[TEST] Starting construct method")
        
        # Animation 1: Create circle
        print("[TEST] Creating circle")
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        print(f"[TEST] Circle created with id: {id(circle)}")
        
        # Animation 2: Create square  
        print("[TEST] Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        print(f"[TEST] Square created with id: {id(square)}")
        
        # Animation 3: Move circle
        print("[TEST] Moving circle")
        self.play(circle.animate.shift(LEFT * 2))
        print(f"[TEST] Circle moved")
        
        print("\n[TEST] Instructions:")
        print("  ← (left arrow) - Go back to previous animation")
        print("  → (right arrow) - Play next animation")
        print("  ↑ (up arrow) - Jump to previous animation instantly")
        print("  ↓ (down arrow) - Jump to next animation instantly")
        print("\n[TEST] Try pressing ← to go back to checkpoint 0, then → to play forward")
        print("[TEST] Watch for duplicate objects!")