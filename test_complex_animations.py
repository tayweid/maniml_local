from maniml import *

class TestComplexAnimations(Scene):
    def construct(self):
        # Test various .animate syntax animations
        circle = Circle(color=BLUE).shift(LEFT * 2)
        square = Square(color=RED).shift(RIGHT * 2)
        text = Text("Test", color=GREEN)
        
        # Animation 1: Create objects
        self.play(Create(circle), Create(square), FadeIn(text))
        
        # Animation 2: Simple .animate movement
        self.play(circle.animate.shift(UP))
        
        # Animation 3: Multiple .animate with different properties
        self.play(
            circle.animate.scale(1.5).set_color(YELLOW),
            square.animate.rotate(PI/4).shift(DOWN),
            text.animate.scale(0.8).shift(UP * 2)
        )
        
        # Animation 4: Complex chained .animate
        self.play(
            circle.animate.shift(DOWN).scale(0.5).set_fill(BLUE, opacity=0.5),
            square.animate.move_to(ORIGIN).scale(2)
        )
        
        # Animation 5: .animate with method calls
        self.play(
            circle.animate.next_to(square, UP),
            text.animate.move_to(DOWN * 2)
        )
        
        print("\n✅ Complex animation test ready!")
        print("This tests .animate syntax without fallback to re-execution.")
        print("\nTest sequence:")
        print("1. Play all animations (→ →)")
        print("2. Jump back to checkpoint 2 (← ← ←)")
        print("3. Play forward (→) - should handle .animate")
        print("4. Jump back again (←)")
        print("5. Play forward again (→)")
        print("\nPreviously this would fall back to re-execution.")