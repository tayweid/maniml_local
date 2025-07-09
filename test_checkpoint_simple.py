from maniml import *

class TestCheckpointSimple(Scene):
    def construct(self):
        # Create a circle at the center
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Move it to the right
        # This mutation should not affect previous checkpoint
        circle.shift(RIGHT * 2)
        self.play(circle.animate.scale(2))
        
        # Create text that depends on circle's position
        text = Text("Hello").next_to(circle, UP)
        self.play(Write(text))
        
        self.wait()