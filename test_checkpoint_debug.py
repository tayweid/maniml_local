from maniml import *

class TestCheckpointDebug(Scene):
    def construct(self):
        # Animation 0: Create circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))  # Checkpoint 0 created AFTER this
        
        # Animation 1: Move circle
        self.play(circle.animate.shift(RIGHT * 2))  # Checkpoint 1 created AFTER this
        
        # Animation 2: Scale circle
        self.play(circle.animate.scale(0.5))  # Checkpoint 2 created AFTER this
        
        print("\nCheckpoint mapping:")
        print("Checkpoint 0: State AFTER Create(circle)")
        print("Checkpoint 1: State AFTER shift(RIGHT * 2)")
        print("Checkpoint 2: State AFTER scale(0.5)")
        print("\nTo replay scale animation, we need to restore to checkpoint 1, not 2!")
        
        self.wait(10)