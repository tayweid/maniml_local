"""Demonstrate that maniml now has full interactive features including MotionMobject."""

from maniml import *
from maniml.manimgl_core.mobject.mobject import Group

class TestManimlFeatures(Scene):
    def construct(self):
        # Title
        title = Text("maniml - Now Fully Featured!", font_size=48, color=YELLOW)
        subtitle = Text("All interactive objects work without external dependencies", font_size=24)
        VGroup(title, subtitle).arrange(DOWN).to_edge(UP)
        self.play(Write(title), Write(subtitle))
        
        # Demo 1: MotionMobject
        motion_title = Text("MotionMobject", font_size=32).shift(UP * 2)
        circle = Circle(radius=0.5, color=BLUE).shift(LEFT * 5)
        motion_obj = MotionMobject(circle)
        motion_label = Text("Drag me!", font_size=16).next_to(circle, DOWN)
        
        # Demo 2: Button
        button_title = Text("Button", font_size=32).shift(UP * 2)
        button_rect = RoundedRectangle(width=2, height=0.8, color=GREEN)
        button_text = Text("Click Me!", font_size=20)
        button_group = VGroup(button_rect, button_text).shift(LEFT * 2)
        
        def on_click(mob):
            # Change color on click
            colors = [GREEN, RED, BLUE, YELLOW]
            current_color = button_rect.get_color()
            current_idx = colors.index(current_color) if current_color in colors else 0
            new_color = colors[(current_idx + 1) % len(colors)]
            button_rect.set_color(new_color)
        
        button = Button(button_group, on_click=on_click)
        
        # Demo 3: Checkbox
        checkbox_title = Text("Checkbox", font_size=32).shift(UP * 2)
        checkbox = Checkbox(value=True).shift(RIGHT * 2)
        checkbox_label = Text("Toggle me!", font_size=16).next_to(checkbox, DOWN)
        
        # Demo 4: Slider
        slider_title = Text("Slider", font_size=32).shift(UP * 2)
        slider = LinearNumberSlider(
            value=5, min_value=0, max_value=10,
            rounded_rect_kwargs={"width": 3}
        ).shift(RIGHT * 5)
        slider_value = DecimalNumber(5).next_to(slider, DOWN)
        slider_value.add_updater(lambda m: m.set_value(slider.get_value()))
        
        # Animate demos one by one
        # Use Group instead of VGroup for mixed mobject types
        demos = [
            (motion_title, Group(motion_obj, motion_label)),
            (button_title, Group(button, checkbox, checkbox_label)),
            (slider_title, Group(slider, slider_value))
        ]
        
        for i, (demo_title, demo_objects) in enumerate(demos):
            if i > 0:
                # Fade out previous
                self.play(FadeOut(demos[i-1][0]), FadeOut(demos[i-1][1]))
            
            self.play(Write(demo_title))
            self.play(Create(demo_objects))
            self.wait(2)
        
        # Final message
        self.play(FadeOut(demos[-1][0]), FadeOut(demos[-1][1]))
        
        final_text = VGroup(
            Text("maniml is now fully featured!", font_size=36, color=GREEN),
            Text("✓ MotionMobject for dragging", font_size=24),
            Text("✓ Buttons, Checkboxes, Sliders", font_size=24),
            Text("✓ No external dependencies needed", font_size=24),
            Text("✓ All ManimGL interactive features included", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        final_text.move_to(ORIGIN)
        
        self.play(Write(final_text))
        
        # Enable interactivity
        self.embed()