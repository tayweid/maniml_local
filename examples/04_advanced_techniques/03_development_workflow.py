from maniml import *

class AutoReloadDemo(Scene):
    """
    Demo of auto-reload functionality.
    
    Instructions:
    1. Run: maniml auto_reload_demo.py AutoReloadDemo
    2. The scene will enter interactive mode after initial animations
    3. Edit this file and save - changes will auto-reload!
    
    Try these edits:
    - Change BLUE to GREEN on line 20
    - Change radius=1 to radius=1.5 on line 20
    - Change "Demo" to "Test" on line 17
    - Add new animations after line 26
    """
    def construct(self):
        # Title
        title = Text("Auto-Reload Demo", font_size=48)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7))
        
        # Create shapes
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        circle.name = "circle"
        self.play(Create(circle))
        
        square = Square(side_length=2, color=RED, fill_opacity=0.5)
        square.name = "square" 
        square.shift(LEFT * 3)
        self.play(Create(square))
        
        # Try changing this text
        label = Text("Edit and save me!", font_size=24)
        label.next_to(circle, DOWN)
        self.play(Write(label))
        
        # Instructions
        instructions = VGroup(
            Text("Available in interactive mode:", font_size=20),
            Text("• list_checkpoints() - Show all checkpoints", font_size=16),
            Text("• jump_to(n) - Jump to checkpoint n", font_size=16),
            Text("• checkpoint_paste() - Run clipboard code", font_size=16),
            Text("• File changes auto-reload!", font_size=16, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        self.play(Write(instructions))
        
        print("\nEntering interactive mode...")
        print("Edit this file and save to see auto-reload in action!")
        
        self.interactive_embed()
        
        # Code after interactive mode
        self.wait(2)