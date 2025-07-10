from maniml import *

class TestIPythonSimple(Scene):
    def construct(self):
        # Test with just two animations
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        print(f"Circle created, id: {id(circle)}")
        
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        print(f"Square created, id: {id(square)}")
        
        print("\nPress ← to go back, then → to go forward")
        print("Both objects should be visible, no duplicates")