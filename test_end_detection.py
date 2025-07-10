from maniml import *

class TestEndDetection(Scene):
    def construct(self):
        # Animation 1
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Animation 2  
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        
        # Print statements at the end
        print("End of animations")
        print("This should not cause replay")