from maniml import *

class AxisLabelsExtended(Scene):
    def construct(self):
        # Title
        title = Text("Axis Labels as Extensions", font_size=42)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Create axes with clear range
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={
                "color": BLUE,
                "include_tip": True,
            },
        )
        
        # Add numbers
        axes.x_axis.add_numbers(range(-4, 5))
        axes.y_axis.add_numbers(range(-3, 4))
        
        self.play(Create(axes))
        
        # Show where the labels go - as if axes continued
        # Draw faint extensions to show the concept
        x_extension = DashedLine(
            axes.coords_to_point(4, 0),
            axes.coords_to_point(5, 0),
            color=BLUE,
            stroke_opacity=0.3
        )
        y_extension = DashedLine(
            axes.coords_to_point(0, 3),
            axes.coords_to_point(0, 3.5),
            color=BLUE,
            stroke_opacity=0.3
        )
        
        self.play(Create(x_extension), Create(y_extension))
        
        # Add the axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        self.play(Write(x_label), Write(y_label))
        self.wait()
        
        # Show with more descriptive labels
        new_x_label = axes.get_x_axis_label("Time (seconds)")
        new_y_label = axes.get_y_axis_label("Distance (meters)")
        
        self.play(
            Transform(x_label, new_x_label),
            Transform(y_label, new_y_label)
        )
        self.wait()
        
        # Plot a function to show context
        func = axes.plot(lambda x: 0.2 * x**2 - 1, color=GREEN)
        func_label = axes.get_graph_label(func, "d = 0.2t^2 - 1", x_val=2)
        
        self.play(Create(func), Write(func_label))
        self.wait()
        
        # Show that labels stay in place with multiple graphs
        sin_func = axes.plot(lambda x: 2 * np.sin(x), color=RED)
        sin_label = axes.get_graph_label(sin_func, "d = 2\\sin(t)", x_val=-2)
        
        self.play(Create(sin_func), Write(sin_label))
        self.wait()
        
        # Highlight the axis label positions
        x_label_box = SurroundingRectangle(x_label, color=YELLOW, buff=0.1)
        y_label_box = SurroundingRectangle(y_label, color=YELLOW, buff=0.1)
        
        note = Text(
            "Labels positioned as axis extensions",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(
            Create(x_label_box),
            Create(y_label_box),
            Write(note)
        )
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(x_label_box),
            FadeOut(y_label_box),
            FadeOut(note)
        )
        
        # Final message
        final = Text(
            "Clean and mathematical!",
            font_size=36,
            color=GREEN
        ).to_edge(DOWN)
        
        self.play(Write(final))
        self.wait()