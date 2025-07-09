from maniml import *

class TestDuplicateObjects(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE, radius=1)
        self.play(Create(circle))
        
        # Add a label to count objects
        text = Text("Objects in scene: 1", font_size=24).to_edge(DOWN)
        self.add(text)
        
        # Move the circle
        self.play(circle.animate.shift(LEFT * 2))
        
        # Create a square
        square = Square(color=RED, side_length=1.5).shift(RIGHT * 2)
        self.play(Create(square))
        
        # Update label
        self.remove(text)
        text = Text("Objects in scene: 2", font_size=24).to_edge(DOWN)
        self.add(text)
        
        # Transform both
        self.play(
            circle.animate.set_fill(BLUE, opacity=0.5),
            square.animate.set_fill(RED, opacity=0.5)
        )
        
        print("\n✅ Test complete!")
        print("Navigate with arrow keys and check for duplicate objects:")
        print("- Jump back to checkpoint 1 (←)")
        print("- Play forward (→)")
        print("- Check if you see duplicate circles or squares")