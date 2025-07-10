from maniml import *

class TestCheckpoint0Debug(Scene):
    def construct(self):
        print("\n[DEBUG] Starting construct")
        
        # Animation 1: Create circle
        circle = Circle(color=BLUE)
        print(f"[DEBUG] Before Create(circle): mobjects={len(self.mobjects)}")
        self.play(Create(circle))
        print(f"[DEBUG] After Create(circle): mobjects={len(self.mobjects)}")
        
        # Animation 2: Create square
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[DEBUG] Before Create(square): mobjects={len(self.mobjects)}")
        self.play(Create(square))
        print(f"[DEBUG] After Create(square): mobjects={len(self.mobjects)}")
        
        # Animation 3: Fade out
        print(f"[DEBUG] Before FadeOut: mobjects={len(self.mobjects)}")
        self.play(FadeOut(circle), FadeOut(square))
        print(f"[DEBUG] After FadeOut: mobjects={len(self.mobjects)}")
        
        print("\n✅ Test ready!")
        print("1. Let it play through")
        print("2. Jump back to checkpoint 0 (press ← until at start)")
        print("3. Play forward (press →)")
        print("4. Watch the debug output for mobject counts")