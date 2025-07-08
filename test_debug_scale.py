from maniml import *

class TestDebugScale(Scene):
    def construct(self):
        circle = Circle(color=BLUE, radius=1)
        
        print(f"Initial circle width: {circle.get_width()}")
        self.play(Create(circle))
        
        print(f"\nBefore scale - circle width: {circle.get_width()}")
        self.play(circle.animate.scale(0.5))
        print(f"After scale - circle width: {circle.get_width()}")
        
        print("\nPress RIGHT arrow to replay the scale animation")
        print("It should show:")
        print("  Before: 2.0")
        print("  After: 1.0")
        
        self.wait(10)