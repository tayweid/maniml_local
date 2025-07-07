from maniml import *

class InteractiveTest(Scene):
    def construct(self):

        # Create some initial objects
        title = Text("Interactive Embedding Tests", font_size=48)
        self.play(Create(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Create a circle
        circle = Circle(radius=3, color=BLUE, fill_opacity=0.5)
        circle.name = "circle"  # Give it a name for easy access in interactive mode
        self.play(Create(circle))
        
        # Create a triangle (to test what persists)
        triangle = Triangle(color=GREEN, fill_opacity=0.5).scale(0.7)
        triangle.name = "triangle"
        triangle.next_to(circle, LEFT, buff=1)
        self.play(Create(triangle))
        
        # Create a square - CHANGE THIS TO Circle
        square = Square(side_length=2, color=RED, fill_opacity=0.5)
        square.name = "square"
        square.next_to(circle, RIGHT, buff=1)
        self.play(Create(square))

        # Create a square - CHANGE THIS TO Circle
        square2 = Square(side_length=2, color=YELLOW, fill_opacity=0.5)
        square2.name = "square"
        square2.next_to(circle, DOWN, buff=0)
        self.play(Create(square2))
        
        self.interactive_embed()