"""Test to identify what's accumulating during dragging."""

from maniml import *
from manimlib.mobject.interactive import MotionMobject
from manimlib.event_handler import EVENT_DISPATCHER
import gc
import sys

class TestAccumulation(Scene):
    """Monitor various metrics to identify what's accumulating."""
    
    def construct(self):
        # Title
        title = Text("Accumulation Test", font_size=20).to_edge(UP)
        self.add(title)
        
        # Create draggable dot using MotionMobject
        dot = Dot(radius=0.2, color=YELLOW)
        draggable = MotionMobject(dot)
        self.add(draggable)
        
        # Metrics tracking
        self.frame_count = 0
        self.drag_count = 0
        self.last_pos = dot.get_center().copy()
        
        # Monitor various counts
        metrics = VGroup(
            Text("Frame: 0", font_size=12),
            Text("Drags: 0", font_size=12),
            Text("Mobjects: 0", font_size=12),
            Text("Event Listeners: 0", font_size=12),
            Text("Updaters: 0", font_size=12),
            Text("Family Size: 0", font_size=12),
            Text("Objects in GC: 0", font_size=12),
            Text("", font_size=12),  # Spacer
            Text("Drag the dot and watch counts", font_size=14, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        
        def update_metrics(m):
            self.frame_count += 1
            
            # Check if dot moved (indicating drag)
            current_pos = dot.get_center()
            if not np.array_equal(current_pos, self.last_pos):
                self.drag_count += 1
                self.last_pos = current_pos.copy()
            
            # Count various things
            mobject_count = len(self.mobjects)
            listener_count = len(EVENT_DISPATCHER)
            
            # Count updaters in the scene
            updater_count = 0
            for mob in self.mobjects:
                if hasattr(mob, 'updaters'):
                    updater_count += len(mob.updaters)
            
            # Get family size of draggable
            family_size = len(draggable.get_family()) if hasattr(draggable, 'get_family') else 0
            
            # Count objects tracked by garbage collector
            gc_count = len(gc.get_objects())
            
            # Update display
            m[0].become(Text(f"Frame: {self.frame_count}", font_size=12))
            m[1].become(Text(f"Drags: {self.drag_count}", font_size=12))
            m[2].become(Text(f"Mobjects: {mobject_count}", font_size=12))
            m[3].become(Text(f"Event Listeners: {listener_count}", font_size=12))
            m[4].become(Text(f"Updaters: {updater_count}", font_size=12))
            m[5].become(Text(f"Family Size: {family_size}", font_size=12))
            m[6].become(Text(f"Objects in GC: {gc_count}", font_size=12))
            
            m.arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        
        metrics.add_updater(update_metrics)
        self.add(metrics)
        
        # Add manual garbage collection button
        gc_button = Rectangle(width=2, height=0.6, fill_color=BLUE, fill_opacity=0.5)
        gc_text = Text("Force GC", font_size=14)
        gc_group = VGroup(gc_button, gc_text).to_corner(DR)
        
        def gc_handler(mob, event_data):
            gc.collect()
            return False
        
        gc_button.add_mouse_press_listner(gc_handler)
        gc_button.add_updater(lambda m: None)
        self.add(gc_group)
        
        self.wait(60)


class TestMemoryProfile(Scene):
    """Profile memory usage during dragging."""
    
    def construct(self):
        import tracemalloc
        tracemalloc.start()
        
        # Title
        title = Text("Memory Profile Test", font_size=20).to_edge(UP)
        self.add(title)
        
        # Create multiple draggable objects
        dots = VGroup()
        for i in range(3):
            dot = Dot(radius=0.15, color=[RED, GREEN, BLUE][i])
            dot.move_to([LEFT * 2, ORIGIN, RIGHT * 2][i])
            draggable = MotionMobject(dot)
            dots.add(draggable)
        
        self.add(dots)
        
        # Memory tracking
        self.frame_count = 0
        self.snapshots = []
        self.baseline = tracemalloc.take_snapshot()
        
        # Display
        memory_info = VGroup(
            Text("Frame: 0", font_size=12),
            Text("Memory: 0 MB", font_size=12),
            Text("Peak: 0 MB", font_size=12),
            Text("Allocations: 0", font_size=12),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        
        def update_memory(m):
            self.frame_count += 1
            
            # Get current memory usage
            current, peak = tracemalloc.get_traced_memory()
            current_mb = current / 1024 / 1024
            peak_mb = peak / 1024 / 1024
            
            # Take snapshot every 100 frames
            if self.frame_count % 100 == 0:
                snapshot = tracemalloc.take_snapshot()
                self.snapshots.append(snapshot)
                
                # Compare to baseline
                if len(self.snapshots) > 1:
                    stats = snapshot.compare_to(self.baseline, 'lineno')
                    top_stats = stats[:5]  # Top 5 differences
                    
                    print(f"\n--- Frame {self.frame_count} Memory Diff ---")
                    for stat in top_stats:
                        print(stat)
            
            # Update display
            m[0].become(Text(f"Frame: {self.frame_count}", font_size=12))
            m[1].become(Text(f"Memory: {current_mb:.1f} MB", font_size=12))
            m[2].become(Text(f"Peak: {peak_mb:.1f} MB", font_size=12))
            m[3].become(Text(f"Snapshots: {len(self.snapshots)}", font_size=12))
            
            m.arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        
        memory_info.add_updater(update_memory)
        self.add(memory_info)
        
        self.add(Text("Drag dots and watch memory usage", font_size=14).to_edge(DOWN))
        
        self.wait(60)