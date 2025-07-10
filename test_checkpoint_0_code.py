from maniml import *

class TestCheckpoint0Code(Scene):
    def construct(self):
        # Let's see what code gets executed at checkpoint 0
        print("\n[TEST] Creating circle object (line 6)")
        circle = Circle(color=BLUE)
        
        print("[TEST] Creating square object (line 9)")  
        square = Square(color=RED).shift(RIGHT * 2)
        
        print("[TEST] Playing Create(circle) - Animation 1")
        self.play(Create(circle))
        
        print("[TEST] Playing Create(square) - Animation 2")
        self.play(Create(square))
        
        print("\n[TEST] Test ready!")
        print("1. Press ← to go back to checkpoint 0")
        print("2. Press → to play forward")
        print("3. Look at the DEBUG output to see what code runs")