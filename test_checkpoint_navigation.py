from maniml import *

class TestCheckpointNavigation(Scene):
    def construct(self):
        """Test checkpoint navigation with IPython implementation."""
        print("\n" + "="*60)
        print("CHECKPOINT NAVIGATION TEST")
        print("="*60)
        
        # Animation 1: Create and show circle
        print("\n[1] Creating blue circle...")
        circle = Circle(color=BLUE, radius=1)
        self.play(Create(circle))
        print(f"   Circle ID: {id(circle)}")
        print(f"   Mobjects in scene: {len(self.mobjects)}")
        
        # Animation 2: Create and show square
        print("\n[2] Creating red square...")
        square = Square(color=RED, side_length=2).shift(RIGHT * 3)
        self.play(Create(square))
        print(f"   Square ID: {id(square)}")
        print(f"   Mobjects in scene: {len(self.mobjects)}")
        
        # Animation 3: Transform circle
        print("\n[3] Moving circle left...")
        self.play(circle.animate.shift(LEFT * 3))
        print(f"   Circle position: {circle.get_center()}")
        
        # Animation 4: Transform square
        print("\n[4] Rotating square...")
        self.play(Rotate(square, PI/4))
        print(f"   Square rotation: {square.get_rotation()}")
        
        # Animation 5: Scale both
        print("\n[5] Scaling both objects...")
        self.play(
            circle.animate.scale(0.5),
            square.animate.scale(0.5)
        )
        
        print("\n" + "="*60)
        print("NAVIGATION INSTRUCTIONS:")
        print("  ← / ↑ : Go to previous animation")
        print("  → / ↓ : Go to next animation")
        print("\nTEST PROCEDURE:")
        print("1. Press ← multiple times to go back to checkpoint 0")
        print("2. Press → to play forward through all animations")
        print("3. Verify: No duplicate objects should appear")
        print("4. Verify: All transformations replay correctly")
        print("="*60 + "\n")