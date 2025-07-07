"""
Hello World - Your First maniml Animation

This is the simplest possible maniml animation.
It creates a text object and animates it onto the screen.

Run with: maniml examples/basic/01_hello_world.py HelloWorld
"""

from maniml import *

class HelloWorld(Scene):
    def construct(self):
        # Create a text object
        text = Text("Hello, maniml!", font_size=48)
        
        # Animate the text appearing
        self.play(Write(text))
        
        # Wait for 2 seconds
        self.wait(2)
        
        # Animate the text disappearing
        self.play(FadeOut(text))