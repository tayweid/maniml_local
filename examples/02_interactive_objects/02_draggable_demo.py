"""Test draggable objects in maniml."""

from maniml import *

class TestDraggableManiml(Scene):
    def construct(self):
        # Create title
        title = Text("Draggable Objects Test", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Create draggable objects
        circle = Circle(radius=0.5, color=BLUE)
        circle.shift(LEFT * 3)
        circle.add_mouse_drag_listner(lambda mob, event_data: mob.move_to(event_data["point"]))
        
        square = Square(side_length=1, color=RED)
        square.shift(ORIGIN)
        square.add_mouse_drag_listner(lambda mob, event_data: mob.move_to(event_data["point"]))
        
        dot = Dot(radius=0.2, color=YELLOW)
        dot.shift(RIGHT * 3)
        dot.add_mouse_drag_listner(lambda mob, event_data: mob.move_to(event_data["point"]))
        
        # Add labels
        label1 = Text("Drag me!", font_size=20).next_to(circle, DOWN)
        label2 = Text("Me too!", font_size=20).next_to(square, DOWN)
        label3 = Text("And me!", font_size=20).next_to(dot, DOWN)
        
        # Animate creation
        self.play(
            Create(circle),
            Create(square),
            Create(dot),
            Write(label1),
            Write(label2),
            Write(label3),
            run_time=2
        )
        
        # Keep labels updated with objects
        label1.add_updater(lambda m: m.next_to(circle, DOWN))
        label2.add_updater(lambda m: m.next_to(square, DOWN))
        label3.add_updater(lambda m: m.next_to(dot, DOWN))
        
        # Add instruction
        instruction = Text("Click and drag the objects!", font_size=24, color=GREEN)
        instruction.to_edge(DOWN)
        self.play(Write(instruction))
        
        # Enable interactivity
        self.embed()  # This keeps the scene interactive