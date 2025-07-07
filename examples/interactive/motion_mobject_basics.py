"""Test MotionMobject with maniml"""

from maniml import *

class TestMotionMobject(Scene):
    def construct(self):
        # Create title
        title = Text("MotionMobject Test", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Create draggable objects using MotionMobject
        circle = Circle(radius=0.5, color=BLUE)
        circle.shift(LEFT * 3)
        draggable_circle = MotionMobject(circle)
        
        square = Square(side_length=1, color=RED)
        square.shift(ORIGIN)
        draggable_square = MotionMobject(square)
        
        dot = Dot(radius=0.2, color=YELLOW)
        dot.shift(RIGHT * 3)
        draggable_dot = MotionMobject(dot)
        
        # Add labels
        label1 = Text("Drag me!", font_size=20).next_to(circle, DOWN)
        label2 = Text("Me too!", font_size=20).next_to(square, DOWN)
        label3 = Text("And me!", font_size=20).next_to(dot, DOWN)
        
        # Animate creation
        self.play(
            Create(draggable_circle),
            Create(draggable_square),
            Create(draggable_dot),
            Write(label1),
            Write(label2),
            Write(label3),
            run_time=2
        )
        
        # Keep labels updated with objects
        label1.add_updater(lambda m: m.next_to(draggable_circle, DOWN))
        label2.add_updater(lambda m: m.next_to(draggable_square, DOWN))
        label3.add_updater(lambda m: m.next_to(draggable_dot, DOWN))
        
        # Add instruction
        instruction = Text("Click and drag the objects using MotionMobject!", font_size=24, color=GREEN)
        instruction.to_edge(DOWN)
        self.play(Write(instruction))
        
        # Enable interactivity
        self.embed()  # This keeps the scene interactive