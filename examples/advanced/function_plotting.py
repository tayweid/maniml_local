from maniml import *

class SimplePlottingDemo(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
            y_axis_config={"numbers_to_include": np.arange(-2, 3, 1)},
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Plot functions
        graph1 = axes.plot(lambda x: np.sin(x), color=RED)
        graph1_label = axes.get_graph_label(graph1, label="\\sin(x)", x_val=1.5)
        
        graph2 = axes.plot(lambda x: np.cos(x), color=GREEN)
        graph2_label = axes.get_graph_label(graph2, label="\\cos(x)", x_val=-1.5)
        
        # Animate
        self.play(Create(axes), Write(axes_labels))
        self.wait()
        
        self.play(Create(graph1), Write(graph1_label))
        self.wait()
        
        self.play(Create(graph2), Write(graph2_label))
        self.wait()
        
        # Show area under sine curve
        area = axes.get_area(graph1, x_range=[0, PI], color=BLUE, opacity=0.5)
        self.play(FadeIn(area))
        self.wait()
        
        self.play(FadeOut(area))
        self.wait()