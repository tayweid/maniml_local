from maniml import *

class TestMouseInteraction(Scene):
    def construct(self):
        # Create some objects to interact with
        circle = Circle(radius=1, color=BLUE).shift(LEFT * 3)
        square = Square(side_length=2, color=RED)
        triangle = Triangle(color=GREEN).shift(RIGHT * 3)
        
        # Add names for easier tracking
        circle.name = "circle"
        square.name = "square"
        triangle.name = "triangle"
        
        # Add objects to scene
        self.add(circle, square, triangle)
        self.wait(1)
        
        # Create a draggable object using MotionMobject
        from manimlib.mobject.interactive import MotionMobject
        text = Text("Drag me!", color=YELLOW).shift(UP * 2)
        draggable_text = MotionMobject(text)
        self.add(draggable_text)
        self.wait(1)
        
        # Add some animations to test arrow key navigation
        self.play(circle.animate.scale(1.5))
        self.play(square.animate.rotate(PI/4))
        self.play(triangle.animate.shift(DOWN))
        
        # Instructions
        instructions = Text(
            "Keys: s=select, g=grab, h=horizontal, v=vertical, t=resize, c=color",
            font_size=24
        ).to_edge(DOWN)
        self.add(instructions)
        
        self.wait(5)