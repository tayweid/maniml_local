from maniml import *

class TestReexecuteAnimation(Scene):
    def construct(self):
        # Animation 1: Create circle
        print(f"[TEST] Creating circle")
        circle = Circle(color=BLUE)
        print(f"[TEST] Circle id before play: {id(circle)}")
        self.play(Create(circle))
        print(f"[TEST] Circle id after play: {id(circle)}")
        
        # Animation 2: Create square  
        print(f"[TEST] Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[TEST] Square id before play: {id(square)}")
        self.play(Create(square))
        print(f"[TEST] Square id after play: {id(square)}")
        
        print("\n[TEST] Current mobjects:")
        for i, mob in enumerate(self.mobjects):
            if isinstance(mob, (Circle, Square)):
                print(f"  [{i}] {type(mob).__name__} id: {id(mob)}")
        
        print("\nPress ← to go back, then → to play forward")