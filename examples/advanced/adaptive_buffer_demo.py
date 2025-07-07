from maniml import *

class AdaptiveBufferDemo(Scene):
    def construct(self):
        # Title
        title = Text("Adaptive Buffer for Axis Labels", font_size=42)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Create two sets of axes - one with tips, one without
        axes_with_tips = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=4,
            axis_config={
                "color": GREEN,
                "include_tip": True,  # Has arrow tips
            },
        ).to_edge(LEFT).shift(DOWN*0.5)
        
        axes_no_tips = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=4,
            axis_config={
                "color": BLUE,
                "include_tip": False,  # No arrow tips
            },
        ).to_edge(RIGHT).shift(DOWN*0.5)
        
        # Add numbers to both
        for axes in [axes_with_tips, axes_no_tips]:
            axes.x_axis.add_numbers([-3, -2, -1, 0, 1, 2, 3])
            axes.y_axis.add_numbers([-2, -1, 0, 1, 2])
        
        # Create axes
        self.play(Create(axes_with_tips), Create(axes_no_tips))
        
        # Add labels - adaptive buffer will automatically adjust
        labels_with_tips = axes_with_tips.get_axis_labels("x", "y")
        labels_no_tips = axes_no_tips.get_axis_labels("x", "y")
        
        # Subtitles
        sub1 = Text("With Arrow Tips", font_size=24, color=GREEN).next_to(axes_with_tips, UP)
        sub2 = Text("Without Arrow Tips", font_size=24, color=BLUE).next_to(axes_no_tips, UP)
        
        self.play(
            Write(labels_with_tips),
            Write(labels_no_tips),
            Write(sub1),
            Write(sub2),
        )
        self.wait()
        
        # Highlight the different spacing
        # Draw lines to show the buffer distance
        tip_buffer_line = DashedLine(
            axes_with_tips.coords_to_point(3, 0),
            labels_with_tips[0].get_left(),
            color=YELLOW,
            stroke_width=2
        )
        
        no_tip_buffer_line = DashedLine(
            axes_no_tips.coords_to_point(3, 0),
            labels_no_tips[0].get_left(),
            color=YELLOW,
            stroke_width=2
        )
        
        # Buffer annotations
        tip_buffer_text = Text("MED_LARGE_BUFF", font_size=16, color=YELLOW).next_to(tip_buffer_line, UP, buff=0.1)
        no_tip_buffer_text = Text("MED_SMALL_BUFF", font_size=16, color=YELLOW).next_to(no_tip_buffer_line, UP, buff=0.1)
        
        self.play(
            Create(tip_buffer_line),
            Create(no_tip_buffer_line),
            Write(tip_buffer_text),
            Write(no_tip_buffer_text),
        )
        self.wait()
        
        # Clean up annotations
        self.play(
            FadeOut(tip_buffer_line),
            FadeOut(no_tip_buffer_line),
            FadeOut(tip_buffer_text),
            FadeOut(no_tip_buffer_text),
        )
        
        # Show with longer labels
        self.play(
            FadeOut(labels_with_tips),
            FadeOut(labels_no_tips),
        )
        
        long_labels_with_tips = axes_with_tips.get_axis_labels("Time (s)", "Distance (m)")
        long_labels_no_tips = axes_no_tips.get_axis_labels("Time (s)", "Distance (m)")
        
        self.play(
            Write(long_labels_with_tips),
            Write(long_labels_no_tips),
        )
        self.wait()
        
        # Add functions to show full context
        func1 = axes_with_tips.plot(lambda x: 0.5*x + 0.5, color=GREEN_E)
        func2 = axes_no_tips.plot(lambda x: -0.3*x**2 + 1.5, color=BLUE_E)
        
        self.play(Create(func1), Create(func2))
        self.wait()
        
        # Final message showing the benefit
        final_message = Text(
            "Adaptive buffer prevents overlap with arrows\nwhile keeping labels close when possible!",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(final_message))
        self.wait(2)
        
        # Zoom in on the tips to show the spacing clearly
        frame = self.camera.frame
        
        # Focus on axes with tips
        self.play(
            frame.animate.set_height(2).move_to(axes_with_tips.coords_to_point(3, 0))
        )
        self.wait()
        
        # Focus on axes without tips
        self.play(
            frame.animate.move_to(axes_no_tips.coords_to_point(3, 0))
        )
        self.wait()
        
        # Reset view
        self.play(
            frame.animate.set_height(8).move_to(ORIGIN)
        )
        self.wait()