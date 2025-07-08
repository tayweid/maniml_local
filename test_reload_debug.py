from maniml import *

class TestReloadDebug(Scene):
    def construct(self):
        # Create circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))  # Animation 1
        
        # Create square - CHANGE THIS LINE
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))  # Animation 2 - Change to FadeIn
        
        # Scale both
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(1.5)
        )  # Animation 3
        
        print("\n=== Debug Info ===")
        print(f"Total checkpoints: {len(self.animation_checkpoints)}")
        for i, cp in enumerate(self.animation_checkpoints):
            print(f"  Checkpoint {i}: line {cp[1]}")
        
        self.wait(20)  # Keep open for testing