from maniml import *

class TestArrows(Scene):
    def construct(self):
        # Animation 1
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.wait(0.5)
        
        # Animation 2
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        self.wait(0.5)
        
        # Animation 3
        self.play(circle.animate.shift(LEFT * 2))
        self.wait(0.5)
        
        # Animation 4
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(1.5)
        )
        self.wait(0.5)
        
        print("\nUse arrow keys to navigate:")
        print("- UP/DOWN: Jump between animation states")
        print("- LEFT: Reverse to previous animation")  
        print("- RIGHT: Play next animation forward")
        
        self.wait(10)  # Give time to test arrow keys