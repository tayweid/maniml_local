from maniml import *

class CorrectAxisLabels(Scene):
    def construct(self):
        # Title
        title = Text("Proper Axis Label Placement", font_size=42)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Create axes
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-2, 4, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE, "include_tip": True},
        )
        
        # Add numbers
        axes.x_axis.add_numbers(range(-3, 6))
        axes.y_axis.add_numbers(range(-2, 5))
        
        # Get axis labels - they should appear at the positive ends
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # Also show custom positioning if needed
        custom_x_label = axes.get_x_axis_label("Time (s)", edge=RIGHT, direction=UP)
        custom_y_label = axes.get_y_axis_label("Height (m)", edge=UP, direction=LEFT)
        
        self.play(Create(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait()
        
        # Transform to custom labels
        self.play(
            Transform(x_label, custom_x_label),
            Transform(y_label, custom_y_label)
        )
        self.wait()
        
        # Plot a function to show context
        func = axes.plot(lambda x: 0.5 * x + 1, color=GREEN)
        func_label = axes.get_graph_label(func, "f(x) = 0.5x + 1", x_val=3)
        
        self.play(Create(func), Write(func_label))
        self.wait()
        
        # Show both styles with get_axis_labels
        self.play(
            FadeOut(x_label), FadeOut(y_label),
            FadeOut(func), FadeOut(func_label)
        )
        
        # Using get_axis_labels method
        axis_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Plot multiple functions
        sin_graph = axes.plot(lambda x: 2 * np.sin(x), color=RED)
        cos_graph = axes.plot(lambda x: 2 * np.cos(x), color=YELLOW)
        
        self.play(
            Write(axis_labels),
            Create(sin_graph),
            Create(cos_graph)
        )
        
        # Add graph labels
        sin_label = axes.get_graph_label(sin_graph, "2\\sin(x)", x_val=1)
        cos_label = axes.get_graph_label(cos_graph, "2\\cos(x)", x_val=-1)
        
        self.play(Write(sin_label), Write(cos_label))
        self.wait(2)
        
        # Final message
        final_text = Text("Axis labels at positive ends!", font_size=36, color=GREEN)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait()