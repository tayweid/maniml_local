from maniml import *

class CheckpointDemo(Scene):
    def construct(self):
        # Create title
        title = Text("Checkpoint System Demo", font_size=48)
        self.play(Write(title))
        
        # Move title up
        self.play(title.animate.to_edge(UP))
        
        # Create shapes
        circle = Circle(color=BLUE).shift(LEFT * 2)
        square = Square(color=RED).shift(RIGHT * 2)
        
        # Show shapes
        self.play(Create(circle), Create(square))
        
        # Transform shapes
        self.play(
            circle.animate.set_fill(BLUE, opacity=0.5),
            square.animate.set_fill(RED, opacity=0.5)
        )
        
        # Add text
        instructions = VGroup(
            Text("Use arrow keys to navigate:", font_size=24),
            Text("← → Play animations", font_size=20),
            Text("↑ ↓ Jump between checkpoints", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT).shift(DOWN * 2)
        
        self.play(Write(instructions))
        
        # Final animation
        self.play(
            circle.animate.scale(1.5).rotate(PI/4),
            square.animate.scale(0.5).rotate(-PI/4)
        )
        
        print("\n✅ Checkpoint system ready!")
        print("Try these keys:")
        print("  → Play next animation")
        print("  ← Jump to previous checkpoint") 
        print("  ↓ Jump to next checkpoint")
        print("  ↑ Jump to previous checkpoint")
        print("\nEdit this file to test auto-reload!")