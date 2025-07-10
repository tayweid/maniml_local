from maniml import *

class TestDuplicateDebug(Scene):
    def construct(self):
        print("\n[TEST] === CONSTRUCT CALLED ===")
        
        # Animation 1: Create circle
        circle = Circle(color=BLUE)
        print(f"[TEST] Before Create(circle)")
        self.play(Create(circle))
        print(f"[TEST] After Create(circle)")
        
        # Animation 2: Create square
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[TEST] Before Create(square)")
        self.play(Create(square))
        print(f"[TEST] After Create(square)")
        
        print("\n[TEST] Done with construct")
        print("Instructions:")
        print("1. Let animations play through")
        print("2. Press ← to go back to checkpoint 0")
        print("3. Press → to play forward")
        print("4. Watch for duplicate circles in the debug output")