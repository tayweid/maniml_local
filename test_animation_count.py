from maniml import *

class TestAnimationCount(Scene):
    def construct(self):
        print("\n=== Test: Animation Count-Based Navigation ===")
        
        # Animation 1
        print("Animation 1: Creating circle")
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Animation 2  
        print("Animation 2: Creating square")
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        
        # Animation 3
        print("Animation 3: Moving objects")
        self.play(
            circle.animate.shift(UP),
            square.animate.shift(DOWN)
        )
        
        print("\n[TEST] Instructions:")
        print("1. Press ← to go back to checkpoint 0")
        print("2. Press → repeatedly to play forward")
        print("3. Verify animations play in order without duplicates")