from maniml import *

class PlottingShowcase(Scene):
    def construct(self):
        # Title
        title = Text("maniml Plotting Demo", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GREY},
            x_axis_config={"numbers_to_include": [-4, -2, 0, 2, 4]},
            y_axis_config={"numbers_to_include": [-3, -1, 1, 3]},
        )
        axes.shift(DOWN * 0.5)
        
        self.play(Create(axes))
        
        # Plot a parabola
        parabola = axes.plot(lambda x: 0.25 * x**2 - 2, color=BLUE)
        parabola_label = axes.get_graph_label(parabola, "y = \\frac{1}{4}x^2 - 2", x_val=3)
        
        self.play(Create(parabola), Write(parabola_label))
        self.wait()
        
        # Show tangent line at x=2
        x_tracker = ValueTracker(2)
        
        def get_tangent():
            x = x_tracker.get_value()
            tangent = axes.get_tangent_line(x, parabola, length=4)
            tangent.set_color(YELLOW)
            return tangent
            
        tangent = always_redraw(get_tangent)
        
        # Add a dot that follows the curve
        dot = always_redraw(lambda: Dot(
            axes.input_to_graph_point(x_tracker.get_value(), parabola),
            color=RED
        ))
        
        self.play(Create(tangent), FadeIn(dot))
        self.wait()
        
        # Animate the tangent line moving
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.play(x_tracker.animate.set_value(3), run_time=3)
        self.wait()
        
        # Show area under curve
        area = axes.get_area(parabola, x_range=[-2, 2], color=GREEN, opacity=0.5)
        self.play(FadeIn(area))
        self.wait()
        
        # Show Riemann rectangles
        rects = axes.get_riemann_rectangles(
            parabola, 
            x_range=[-2, 2], 
            n_iterations=8,
            color=ORANGE,
            fill_opacity=0.5
        )
        
        self.play(Transform(area, rects))
        self.wait()
        
        # Clear and show parametric curve
        self.play(
            FadeOut(area), FadeOut(tangent), FadeOut(dot),
            FadeOut(parabola), FadeOut(parabola_label)
        )
        
        # Parametric spiral
        spiral = axes.plot_parametric_curve(
            lambda t: np.array([
                t * np.cos(t),
                t * np.sin(t),
                0
            ]),
            t_range=[0, 4 * PI],
            color=PURPLE
        )
        
        self.play(Create(spiral), run_time=3)
        self.wait()
        
        # Final message
        final_text = Text("maniml: CE API + GL Speed!", font_size=36)
        final_text.next_to(axes, DOWN)
        
        self.play(Write(final_text))
        self.wait(2)