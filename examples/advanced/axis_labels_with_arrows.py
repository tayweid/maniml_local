from maniml import *

class AxisLabelsWithArrows(Scene):
    def construct(self):
        # Title
        title = Text("Axis Labels with Arrow Tips", font_size=42)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Create three sets of axes to show comparison
        # 1. Without tips
        axes1 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "color": BLUE,
                "include_tip": False,
            },
        ).to_edge(LEFT).shift(DOWN*0.5)
        
        # 2. With tips and proper buffer
        axes2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "color": GREEN,
                "include_tip": True,
            },
        ).center().shift(DOWN*0.5)
        
        # 3. With tips and custom buffer
        axes3 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "color": RED,
                "include_tip": True,
            },
        ).to_edge(RIGHT).shift(DOWN*0.5)
        
        # Add numbers to all
        for axes in [axes1, axes2, axes3]:
            axes.x_axis.add_numbers([-2, -1, 0, 1, 2])
            axes.y_axis.add_numbers([-2, -1, 0, 1, 2])
        
        # Create all axes
        self.play(
            Create(axes1),
            Create(axes2),
            Create(axes3),
        )
        
        # Add labels
        labels1 = axes1.get_axis_labels("x", "y")
        labels2 = axes2.get_axis_labels("x", "y")
        # Custom buffer for comparison
        x_label3 = axes3.get_x_axis_label("x", buff=LARGE_BUFF)
        y_label3 = axes3.get_y_axis_label("y", buff=LARGE_BUFF)
        labels3 = VGroup(x_label3, y_label3)
        
        # Subtitles
        sub1 = Text("No Tips", font_size=20, color=BLUE).next_to(axes1, UP)
        sub2 = Text("Default Buffer", font_size=20, color=GREEN).next_to(axes2, UP)
        sub3 = Text("Extra Buffer", font_size=20, color=RED).next_to(axes3, UP)
        
        self.play(
            Write(labels1),
            Write(labels2),
            Write(labels3),
            Write(sub1),
            Write(sub2),
            Write(sub3),
        )
        self.wait()
        
        # Highlight the good spacing
        highlight = SurroundingRectangle(
            VGroup(axes2, labels2),
            color=YELLOW,
            buff=0.2
        )
        note = Text(
            "Good spacing prevents overlap!",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Create(highlight), Write(note))
        self.wait()
        
        # Clear and show with longer labels
        self.play(
            FadeOut(highlight),
            FadeOut(note),
            FadeOut(labels1),
            FadeOut(labels2),
            FadeOut(labels3),
        )
        
        # Show with longer labels
        long_labels1 = axes1.get_axis_labels("Time (s)", "Height (m)")
        long_labels2 = axes2.get_axis_labels("Time (s)", "Height (m)")
        long_labels3 = axes3.get_axis_labels("Time (s)", "Height (m)")
        
        self.play(
            Write(long_labels1),
            Write(long_labels2),
            Write(long_labels3),
        )
        
        # Add some functions to show context
        func1 = axes1.plot(lambda x: 0.5*x + 0.5, color=BLUE_E)
        func2 = axes2.plot(lambda x: -0.3*x**2 + 1, color=GREEN_E)
        func3 = axes3.plot(lambda x: np.sin(2*x), color=RED_E)
        
        self.play(
            Create(func1),
            Create(func2),
            Create(func3),
        )
        
        self.wait(2)
        
        # Final message
        final = Text(
            "MED_LARGE_BUFF provides ideal spacing!",
            font_size=32,
            color=GREEN
        ).to_edge(DOWN)
        
        self.play(Write(final))
        self.wait()