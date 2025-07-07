"""Test a simple fix for the dragging performance issue - maniml version."""

from maniml import *
import gc
import weakref

class CachedMotionMobject(Mobject):
    """MotionMobject that caches get_family() results."""
    
    def __init__(self, mobject):
        # Set cache attributes BEFORE calling super().__init__
        self._cached_family = None
        self._family_cached = False
        
        super().__init__()
        self.mobject = mobject
        self.mobject.add_mouse_drag_listner(self.cached_drag)
        self.mobject.add_updater(lambda m: None)
        self.add(mobject)
        
    def cached_drag(self, mob, event_data):
        """Drag handler that uses cached family."""
        mob.move_to(event_data["point"])
        return False
    
    def get_family(self, recurse=True):
        """Override to cache the family list."""
        if not self._family_cached:
            self._cached_family = super().get_family(recurse)
            self._family_cached = True
        return self._cached_family


class SimplerFix(Mobject):
    """Even simpler approach - just wrap the mobject."""
    def __init__(self, mobject):
        super().__init__()
        self.add(mobject)
        # Make the wrapped mobject draggable
        mobject.add_mouse_drag_listner(lambda m, e: m.move_to(e["point"]))
        # Add empty updater to prevent static optimization
        mobject.add_updater(lambda m: None)


class TestSimpleFix(Scene):
    def construct(self):
        # Title
        title = Text("Dragging Performance Test", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Create test objects
        positions = [LEFT * 4, ORIGIN, RIGHT * 4]
        colors = [BLUE, RED, GREEN]
        names = ["Regular", "Smart", "Cached"]
        
        dots = []
        labels = []
        
        for pos, color, name in zip(positions, colors, names):
            # Create dot
            dot = Dot(pos, radius=0.2, color=color)
            
            # Apply wrapper based on type
            if name == "Regular":
                draggable = MotionMobject(dot)
            elif name == "Smart":
                draggable = SimplerFix(dot)
            else:  # Cached
                draggable = CachedMotionMobject(dot)
            
            self.add(draggable)
            dots.append(draggable)
            
            # Add label
            label = Text(name, font_size=14, color=color).next_to(pos + DOWN * 2, DOWN)
            self.add(label)
            labels.append(label)
        
        # Instructions
        instructions = VGroup(
            Text("Test dragging performance:", font_size=20),
            Text("1. Regular MotionMobject (may get laggy)", font_size=16),
            Text("2. Simple wrapper (should stay smooth)", font_size=16),
            Text("3. Cached family (optimized)", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT)
        instructions.to_edge(DOWN)
        self.add(instructions)
        
        # Enable interactivity
        self.embed()