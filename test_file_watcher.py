from maniml import *

class TestFileWatcher(Scene):
    def construct(self):
        # Enable auto-reload
        self.auto_reload_enabled = True
        
        # Animation 1: Create circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.wait(0.5)
        
        # Animation 2: Create square
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(square))
        self.wait(0.5)
        
        # Animation 3: Move circle
        self.play(circle.animate.shift(LEFT * 2))
        self.wait(0.5)
        
        # Animation 4: Scale both
        self.play(
            circle.animate.scale(0.5),  # Try changing to 0.3
            square.animate.scale(1.5)   # Try changing to 2.0
        )
        self.wait(0.5)
        
        print("\n=== File watcher enabled ===")
        print("Edit this file and save to see auto-reload")
        print("Try changing the scale values in Animation 4")
        print("Only affected animations should replay!")
        
        self.wait(30)  # Keep scene open for testing