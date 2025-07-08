from maniml import *

class TestReloadFix(Scene):
    def construct(self):
        # Create objects - these need to be available after reload
        circle = Circle(color=BLUE)
        square = Square(color=RED).shift(RIGHT * 2)
        
        # Animation 1
        self.play(Create(circle))
        
        # Animation 2 - EDIT THIS to FadeIn
        self.play(Create(square))
        
        # Animation 3
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(1.5)
        )
        
        print("Edit line 13: Change Create(square) to FadeIn(square)")
        print("Save the file and watch the reload")
        
        self.wait(20)