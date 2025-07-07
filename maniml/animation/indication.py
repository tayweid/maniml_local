"""
Indication animations with CE compatibility.
"""

import maniml.manimgl_core
from maniml.manimgl_core.animation.indication import (
    FocusOn as GLFocusOn,
    Indicate as GLIndicate,
    Flash as GLFlash,
    CircleIndicate as GLCircleIndicate,
    ShowPassingFlashAround as GLShowPassingFlashAround,
    WiggleOutThenIn as GLWiggleOutThenIn,
    ShowCreationThenDestruction as GLShowCreationThenDestruction,
    ShowCreationThenFadeOut as GLShowCreationThenFadeOut,
)
from maniml.manimgl_core.constants import *
import warnings


# Direct mappings
FocusOn = GLFocusOn
Indicate = GLIndicate
Flash = GLFlash
CircleIndicate = GLCircleIndicate
ShowPassingFlashAround = GLShowPassingFlashAround
ShowCreationThenDestruction = GLShowCreationThenDestruction
ShowCreationThenFadeOut = GLShowCreationThenFadeOut

# Wiggle maps to WiggleOutThenIn in GL
Wiggle = GLWiggleOutThenIn


# Circumscribe doesn't exist in GL, create it
from maniml.manimgl_core.animation.creation import ShowCreation as GLShowCreation

class Circumscribe(GLShowCreation):
    """CE-compatible Circumscribe - draws shape around object."""
    
    def __init__(self, mobject, shape=None, color=YELLOW, buff=0.1, **kwargs):
        if shape is None:
            from maniml.manimgl_core.mobject.geometry import Rectangle
            shape = Rectangle(color=color)
            shape.surround(mobject, buff=buff)
        
        # Initialize with the shape
        super().__init__(shape, **kwargs)