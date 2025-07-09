from maniml import *

class TestSingleReplay(Scene):
    def construct(self):
        # Very simple test
        circle = Circle(color=BLUE)
        
        print("Creating circle")
        self.play(Create(circle))
        
        print("Moving circle right")
        self.play(circle.animate.shift(RIGHT * 2))
        
        self.wait()
        
        print("\nTest:")
        print("1. Press LEFT to go back to start") 
        print("2. Press RIGHT to replay first animation")
        print("3. Should see ONE circle being created, not two")