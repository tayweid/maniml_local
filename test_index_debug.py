from maniml import *

class TestIndexDebug(Scene):
    def construct(self):
        print("\n[DEBUG] === CONSTRUCT CALLED ===")
        print(f"[DEBUG] current_checkpoint = {self.current_checkpoint}")
        print(f"[DEBUG] tight = {self.tight}")
        print(f"[DEBUG] Number of checkpoints = {len(self.checkpoints)}")
        print(f"[DEBUG] Number of mobjects = {len(self.mobjects)}")
        
        # Print checkpoint info
        for i, cp in enumerate(self.checkpoints):
            print(f"[DEBUG] Checkpoint {i}: line={cp[1]}")
        
        # Animation 1: Create circle
        print(f"\n[DEBUG] About to create circle")
        circle = Circle(color=BLUE)
        print(f"[DEBUG] Circle object created, mobjects before play = {len(self.mobjects)}")
        self.play(Create(circle))
        print(f"[DEBUG] After play, mobjects = {len(self.mobjects)}")
        print(f"[DEBUG] After play, current_checkpoint = {self.current_checkpoint}")
        
        # Animation 2: Create square
        print(f"\n[DEBUG] About to create square")
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[DEBUG] Square object created, mobjects before play = {len(self.mobjects)}")
        self.play(Create(square))
        print(f"[DEBUG] After play, mobjects = {len(self.mobjects)}")
        print(f"[DEBUG] After play, current_checkpoint = {self.current_checkpoint}")
        
        print("\n✅ Test ready! Try:")
        print("1. Press ← to go back to checkpoint 0")
        print("2. Press → to play forward")
        print("3. Watch the debug output")