from maniml import *

class TestMutabilityFix(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Move it to the right
        self.play(circle.animate.shift(RIGHT * 2))
        
        # Change its color
        self.play(circle.animate.set_color(RED))
        
        # Create a square that references the circle's position
        square = Square(color=GREEN).next_to(circle, DOWN)
        self.play(Create(square))
        
        # Move both together
        group = VGroup(circle, square)
        self.play(group.animate.shift(LEFT * 4))
        
        # Test with a list of mobjects
        dots = [Dot(color=YELLOW).shift(UP * i) for i in range(3)]
        self.play(*[Create(dot) for dot in dots])
        
        # Mutate the dots
        for dot in dots:
            dot.shift(RIGHT)
        self.play(*[dot.animate.set_color(PURPLE) for dot in dots])
        
        self.wait()