from maniml import *

class TestObjectIdentity(Scene):
    def construct(self):
        print("\n[TEST] Creating circle")
        circle = Circle(color=BLUE)
        print(f"[TEST] Circle id: {id(circle)}")
        
        print("\n[TEST] Playing Create(circle)")
        self.play(Create(circle))
        print(f"[TEST] After Create - Circle id: {id(circle)}")
        print(f"[TEST] Mobjects in scene:")
        for i, mob in enumerate(self.mobjects):
            if isinstance(mob, Circle):
                print(f"  [{i}] Circle id: {id(mob)}")
        
        print("\n[TEST] Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[TEST] Square id: {id(square)}")
        
        print("\n[TEST] Playing Create(square)")
        self.play(Create(square))
        
        print(f"\n[TEST] Final state:")
        print(f"[TEST] Circle var id: {id(circle)}")
        print(f"[TEST] Square var id: {id(square)}")
        print(f"[TEST] Mobjects in scene:")
        for i, mob in enumerate(self.mobjects):
            if isinstance(mob, (Circle, Square)):
                print(f"  [{i}] {type(mob).__name__} id: {id(mob)}")
        
        print("\n[TEST] Instructions:")
        print("1. Press ← to go back")
        print("2. Press → to play forward")
        print("3. Watch the object IDs")