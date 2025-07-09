from maniml import *

class TestStaleReferenceFix(Scene):
    def construct(self):
        # Create objects with clear names
        circle = Circle(color=BLUE, radius=1).shift(LEFT * 2)
        square = Square(color=RED, side_length=1.5).shift(RIGHT * 2)
        
        # Animation 1: Create circle
        self.play(Create(circle))
        
        # Animation 2: Create square
        self.play(Create(square))
        
        # Animation 3: Move both
        self.play(
            circle.animate.shift(UP),
            square.animate.shift(DOWN)
        )
        
        # Animation 4: Transform colors
        self.play(
            circle.animate.set_fill(BLUE, opacity=0.5),
            square.animate.set_fill(RED, opacity=0.5)
        )
        
        # Animation 5: Scale
        self.play(
            circle.animate.scale(1.5),
            square.animate.scale(0.8)
        )
        
        print("\n✅ Test ready!")
        print("Try this sequence:")
        print("1. Play forward to end (→ →)")
        print("2. Jump back to checkpoint 2 (← ← ←)")
        print("3. Play forward (→)")
        print("4. Jump back again (←)")
        print("5. Play forward again (→)")
        print("\nPreviously this would glitch on step 5. Should work now!")