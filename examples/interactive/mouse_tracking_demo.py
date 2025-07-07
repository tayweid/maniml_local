from maniml import *

class CursorFixDemo(Scene):
    """Demonstrates the spinning cursor fix in maniml."""
    
    def construct(self):
        # Title
        title = Text("maniml Cursor Fix Demo", font_size=48)
        subtitle = Text(
            "The cursor should remain normal (not spinning) between animations",
            font_size=24,
            color=GRAY
        )
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)  # Cursor should be normal during this wait
        
        self.play(
            FadeOut(subtitle),
            title.animate.scale(0.6).to_edge(UP)
        )
        
        # Create some shapes
        shapes = VGroup(
            Circle(radius=0.8, color=BLUE, fill_opacity=0.7),
            Square(side_length=1.6, color=RED, fill_opacity=0.7),
            Triangle(color=GREEN, fill_opacity=0.7).scale(0.8),
        ).arrange(RIGHT, buff=1)
        
        # Animate shapes one by one with waits between
        for i, shape in enumerate(shapes):
            self.play(FadeIn(shape, scale=0.5))
            self.wait(1)  # Check cursor during each wait
            
            # Add a label
            label = Text(f"Shape {i+1}", font_size=20)
            label.next_to(shape, DOWN)
            self.play(Write(label))
            self.wait(0.5)
        
        # Interactive checkpoint
        info = Text(
            "Check the cursor - it should NOT be spinning!\nPress Ctrl-D to continue...",
            font_size=28,
            color=YELLOW
        )
        info.to_edge(DOWN)
        self.play(Write(info))
        
        # Pause for interaction
        self.interactive_embed()
        
        self.play(FadeOut(info))
        
        # Some transformations
        self.play(
            shapes[0].animate.shift(UP),
            shapes[1].animate.rotate(PI/4),
            shapes[2].animate.shift(DOWN),
        )
        self.wait(1)
        
        # Long wait to observe cursor
        wait_text = Text("Waiting 3 seconds - cursor should stay normal", font_size=24)
        wait_text.to_edge(DOWN)
        self.play(Write(wait_text))
        self.wait(3)
        
        self.play(FadeOut(wait_text))
        
        # Final message
        success = Text("✓ Cursor fix working!", font_size=36, color=GREEN)
        success.next_to(shapes, DOWN, buff=1)
        self.play(Write(success))
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class QuickCursorTest(Scene):
    """Quick test to verify cursor doesn't spin."""
    
    def construct(self):
        text = Text("Watch the cursor!", font_size=48)
        self.play(Write(text))
        
        # Multiple short waits - cursor should stay normal
        for i in range(5):
            self.wait(0.5)
            self.play(text.animate.rotate(PI/10))
        
        self.wait(2)  # Final wait
        self.play(FadeOut(text))