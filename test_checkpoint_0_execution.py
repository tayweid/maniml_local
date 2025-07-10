from maniml import *

class TestCheckpoint0Execution(Scene):
    def construct(self):
        print("\n[EXEC] construct() called - this should print every time code re-executes")
        
        # Counter to track executions
        if not hasattr(self, 'execution_count'):
            self.execution_count = 0
        self.execution_count += 1
        print(f"[EXEC] Execution #{self.execution_count}")
        
        # Animation 1: Create circle
        print(f"[EXEC] About to create circle (execution #{self.execution_count})")
        circle = Circle(color=BLUE)
        print(f"[EXEC] Circle created: {circle}")
        print(f"[EXEC] Mobjects before Create: {len(self.mobjects)}")
        self.play(Create(circle))
        print(f"[EXEC] Mobjects after Create: {len(self.mobjects)}")
        
        # Animation 2: Create square
        print(f"\n[EXEC] About to create square (execution #{self.execution_count})")
        square = Square(color=RED).shift(RIGHT * 2)
        print(f"[EXEC] Square created: {square}")
        print(f"[EXEC] Mobjects before Create: {len(self.mobjects)}")
        self.play(Create(square))
        print(f"[EXEC] Mobjects after Create: {len(self.mobjects)}")
        
        print("\n✅ Execution tracking test ready!")
        print("Instructions:")
        print("1. Let it play through all animations")
        print("2. Press ← to go back to checkpoint 0")
        print("3. Press → to play forward")
        print("4. Watch the [EXEC] messages to see if code re-executes")
        print("\nIf re-execution happens, you should see:")
        print("- 'construct() called' again")
        print("- 'Execution #2'")
        print("- New circle/square objects being created")