from maniml import *

class DebugCheckpoints(Scene):
    def construct(self):
        # Override play to print more info
        original_play = self.play
        def debug_play(*args, **kwargs):
            import inspect
            frame = inspect.currentframe().f_back
            print(f"\n[DEBUG] play() called at line {frame.f_lineno}")
            result = original_play(*args, **kwargs)
            print(f"[DEBUG] Checkpoint created: index={self.current_animation_index}, count={len(self.animation_checkpoints)}")
            return result
        self.play = debug_play
        
        # Animation 1
        circle = Circle()
        self.play(Create(circle))  # Line 18
        
        # Animation 2  
        self.play(circle.animate.shift(RIGHT))  # Line 21
        
        # Animation 3 - Multi-line
        self.play(
            circle.animate.scale(0.5),
            circle.animate.set_color(RED)
        )  # Lines 24-27
        
        print("\n[SUMMARY] Checkpoints created:")
        for i, cp in enumerate(self.animation_checkpoints):
            print(f"  Checkpoint {i}: line {cp[1]}")
            
        self.wait(5)