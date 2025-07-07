from maniml import *

class AxisLabelComparison(Scene):
    def construct(self):
        # Create two sets of axes side by side
        axes1 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": BLUE},
        ).to_edge(LEFT)
        
        axes2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": GREEN},
        ).to_edge(RIGHT)
        
        # Add numbers
        for axes in [axes1, axes2]:
            axes.x_axis.add_numbers([-2, -1, 0, 1, 2])
            axes.y_axis.add_numbers([-2, -1, 0, 1, 2])
        
        # Show both axes
        self.play(Create(axes1), Create(axes2))
        
        # Labels with default positioning (at positive ends)
        labels1 = axes1.get_axis_labels(x_label="x", y_label="y")
        
        # Labels with custom positioning (wrong way)
        x_label2_wrong = axes2.get_x_axis_label("x", edge=DOWN, direction=DOWN)
        y_label2_wrong = axes2.get_y_axis_label("y", edge=LEFT, direction=LEFT)
        labels2_wrong = VGroup(x_label2_wrong, y_label2_wrong)
        
        # Add titles
        title1 = Text("Correct", font_size=24, color=BLUE).next_to(axes1, UP)
        title2 = Text("Wrong", font_size=24, color=RED).next_to(axes2, UP)
        
        self.play(
            Write(labels1),
            Write(labels2_wrong),
            Write(title1),
            Write(title2)
        )
        self.wait(2)
        
        # Fix the wrong one
        self.play(
            FadeOut(labels2_wrong),
            FadeOut(title2)
        )
        
        # Show correct positioning on right axes too
        labels2 = axes2.get_axis_labels(x_label="x", y_label="y")
        title2_new = Text("Also Correct", font_size=24, color=GREEN).next_to(axes2, UP)
        
        self.play(
            Write(labels2),
            Write(title2_new)
        )
        
        # Add some context with functions
        func1 = axes1.plot(lambda x: x**2 - 1, color=YELLOW)
        func2 = axes2.plot(lambda x: np.sin(2*x), color=PURPLE)
        
        self.play(Create(func1), Create(func2))
        
        # Main message
        message = Text(
            "Axis labels belong at the positive ends!",
            font_size=32
        ).to_edge(DOWN)
        
        self.play(Write(message))
        self.wait(2)