from maniml import *

class TestSimple(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE, radius=1)
        square = Square(color=RED, side_length=1).shift(RIGHT * 3)
        
        # Animation 1
        self.play(Create(circle))
        
        # Animation 2  
        self.play(Create(square))

        # ani 2.1
        self.play(circle.animate.scale(1.3))
        
        # Animation 3 - Scale both
        self.play(
            circle.animate.scale(1),
            square.animate.scale(2)
        )