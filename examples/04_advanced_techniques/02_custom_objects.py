from maniml import *

class SimpleAxisDemo(Scene):
    def construct(self):
        # Create axes with labels
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y") 
        
        # Or both at once
        axis_labels = axes.get_axis_labels(x_label="Time", y_label="Value")
        
        self.play(Create(axes))
        self.play(Write(axis_labels))
        self.wait()
        
        # Plot a function
        graph = axes.plot(lambda x: np.sin(x), color=RED)
        graph_label = axes.get_graph_label(graph, "\\sin(x)", x_val=1)
        
        self.play(Create(graph), Write(graph_label))
        self.wait()
        
        # Add coordinate labels to axes
        axes.x_axis.add_numbers([-3, -2, -1, 0, 1, 2, 3])
        axes.y_axis.add_numbers([-2, -1, 0, 1, 2])
        
        self.wait()
        
        # Show a specific point
        point = axes.coords_to_point(PI/2, 1)
        dot = Dot(point, color=YELLOW)
        coord_label = MathTex("(\\pi/2, 1)").next_to(dot, UR)
        
        self.play(FadeIn(dot), Write(coord_label))
        self.wait(2)