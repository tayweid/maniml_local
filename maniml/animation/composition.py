"""
Composition animations with CE compatibility.
"""

import maniml.manimgl_core
from maniml.manimgl_core.animation.composition import (
    AnimationGroup as GLAnimationGroup,
    Succession as GLSuccession,
    LaggedStart as GLLaggedStart,
    LaggedStartMap as GLLaggedStartMap,
)
from maniml.manimgl_core.animation.fading import FadeIn
import warnings


# Direct mappings
AnimationGroup = GLAnimationGroup
Succession = GLSuccession
LaggedStart = GLLaggedStart
# LaggedStartMap needs special handling
class LaggedStartMap(GLLaggedStartMap):
    """CE-compatible LaggedStartMap."""
    
    def __init__(self, AnimClass, mobjects, **kwargs):
        # CE passes animation class and mobjects (could be list or VGroup)
        # GL expects animation function and group
        
        # Convert mobjects to VGroup if it's a list
        from maniml.manimgl_core.mobject.types.vectorized_mobject import VGroup
        if isinstance(mobjects, list):
            group = VGroup(*mobjects)
        else:
            group = mobjects
            
        # Create animation function from class
        if isinstance(AnimClass, type):
            anim_func = lambda m: AnimClass(m)
        else:
            anim_func = AnimClass
            
        super().__init__(anim_func, group, **kwargs)


class Wait(maniml.manimgl_core.animation.animation.Animation):
    """CE-compatible Wait animation."""
    
    def __init__(self, duration=1.0, stop_condition=None, **kwargs):
        # Create a dummy mobject
        from maniml.manimgl_core.mobject.mobject import Mobject
        dummy = Mobject()
        
        kwargs['run_time'] = duration
        super().__init__(dummy, **kwargs)
        
        self.stop_condition = stop_condition
    
    def begin(self):
        super().begin()
        if self.stop_condition:
            warnings.warn(
                "maniml: Wait with stop_condition not fully supported.",
                UserWarning
            )
    
    def interpolate_mobject(self, alpha):
        # Do nothing - just wait
        pass


class EmptyAnimation(maniml.manimgl_core.animation.animation.Animation):
    """CE-compatible EmptyAnimation - does nothing."""
    
    def __init__(self, mobject=None, **kwargs):
        if mobject is None:
            from maniml.manimgl_core.mobject.mobject import Mobject
            mobject = Mobject()
            
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha):
        # Do nothing
        pass