from maniml import *

class TestAutoReload(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE)
        square = Square(color=RED).shift(RIGHT * 2)
        
        # Animation 1
        self.play(Create(circle))
        self.wait(0.5)
        
        # Animation 2 - CHANGE THIS to FadeIn
        self.play(Create(square))
        self.wait(0.5)
        
        # Animation 3
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(1.5)
        )
        self.wait(0.5)
        
        print("\nEdit line 14: Change Create(square) to FadeIn(square)")
        print("The animation should replay automatically")
        self.wait(20)  # Keep open for testing