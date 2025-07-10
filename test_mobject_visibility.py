from maniml import *

class TestMobjectVisibility(Scene):
    def construct(self):
        print("\n[TEST] Creating circle")
        circle = Circle(color=BLUE)
        print(f"[TEST] Circle created: {circle}")
        print(f"[TEST] Circle opacity: {circle.get_fill_opacity()}, {circle.get_stroke_opacity()}")
        
        print("\n[TEST] Playing Create(circle)")
        self.play(Create(circle))
        print(f"[TEST] After Create: Circle in mobjects? {circle in self.mobjects}")
        print(f"[TEST] Circle opacity after: {circle.get_fill_opacity()}, {circle.get_stroke_opacity()}")
        
        print("\n[TEST] Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[TEST] Square created: {square}")
        
        print("\n[TEST] Playing Create(square)")
        self.play(Create(square))
        
        print(f"\n[TEST] Final mobjects count: {len(self.mobjects)}")
        for i, mob in enumerate(self.mobjects):
            if hasattr(mob, 'get_stroke_opacity'):
                print(f"  [{i}] {type(mob).__name__} - stroke opacity: {mob.get_stroke_opacity()}")
            else:
                print(f"  [{i}] {type(mob).__name__}")
        
        print("\n[TEST] Instructions:")
        print("1. Press ← to go back to checkpoint 0")
        print("2. Press → to play forward")
        print("3. Check if you see both circle and square")