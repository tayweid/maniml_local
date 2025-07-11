from maniml import *

class TestMultilinePlay(Scene):
    def construct(self):
        print("\n=== Testing Multi-line play() Navigation ===")
        print("[DEBUG] Testing line tracking injection")
        
        # Animation 1: Single line
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Animation 2: Multi-line with two animations
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(
            Create(square),
            circle.animate.shift(LEFT)
        )
        
        # Animation 3: Multi-line with complex animations
        self.play(
            circle.animate.scale(2).set_color(GREEN),
            square.animate.rotate(PI/4).shift(UP),
            run_time=2
        )
        
        # Animation 4: Another multi-line
        triangle = Triangle(color=YELLOW).shift(DOWN * 2)
        self.play(
            Create(triangle),
            circle.animate.shift(RIGHT * 2),
            square.animate.shift(LEFT * 2),
            lag_ratio=0.5
        )
        
        # Animation 5: Single line again
        self.play(FadeOut(triangle))
        
        print("\n[TEST] Try navigating with arrow keys!")
        print("Multi-line play() calls should work correctly")
        self.interactive_embed()