from maniml import *

class TestSimple(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE, radius=1)
        square = Square(color=RED, side_length=1).shift(RIGHT * 3)
        
        # Animation 1
        self.play(Create(circle))

        # Animation 2  
        self.play(FadeIn(square))
        
        # Animation 3 - Move objects
        self.play(
            circle.animate.shift(UP),
            square.animate.shift(DOWN)
        )

        # Animation 4 - Scale both again
        self.play(
            circle.animate.scale(2),
            square.animate.scale(2)
        )

        # ani 2.1
        self.play(circle.animate.scale(0.3))

        # Animation 5 - Move objects  
        self.play(
            circle.animate.shift(UP*0.1),
            square.animate.shift(DOWN*0.2)
        )