from maniml import *

class TestSimple(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE, radius=1)
        square = Square(color=RED, side_length=1).shift(RIGHT * 3)
        
        print("Initial circle radius:", circle.get_width() / 2)
        print("Initial square side:", square.get_width())
        
        # Animation 1
        self.play(Create(circle))
        self.wait(0.5)
        
        # Animation 2  
        self.play(Create(square))
        self.wait(0.5)
        
        # Animation 3 - Scale both
        print("\nBefore scale animation:")
        print("Circle radius:", circle.get_width() / 2)
        print("Square side:", square.get_width())
        
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(1.5)
        )
        
        print("\nAfter scale animation:")
        print("Circle radius:", circle.get_width() / 2)
        print("Square side:", square.get_width())
        
        self.wait(0.5)