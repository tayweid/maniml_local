from maniml import *

class AxisShowcase(Scene):
    def construct(self):
        # Title
        title = Text("Axis Features Showcase", font_size=48, color=BLUE)
        self.play(Write(title))
        self.play(title.animate.scale(0.6).to_edge(UP))
        
        # 1. Basic axes with all labels
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GREY}
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")
        
        # Add numbers to axes
        axes.x_axis.add_numbers(range(-5, 6))
        axes.y_axis.add_numbers([-3, -2, -1, 1, 2, 3])
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()
        
        # 2. Plot multiple functions
        sin_graph = axes.plot(lambda x: np.sin(x), color=RED)
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)", x_val=2)
        
        cos_graph = axes.plot(lambda x: np.cos(x), color=BLUE)
        cos_label = axes.get_graph_label(cos_graph, "\\cos(x)", x_val=-2)
        
        exp_graph = axes.plot(lambda x: 0.5 * np.exp(0.3*x) - 2, color=GREEN)
        exp_label = axes.get_graph_label(exp_graph, "0.5e^{0.3x} - 2", x_val=3)
        
        self.play(
            Create(sin_graph), Write(sin_label),
            Create(cos_graph), Write(cos_label),
            Create(exp_graph), Write(exp_label),
            run_time=2
        )
        self.wait()
        
        # 3. Mark specific points
        # Intersection of sin and cos at x = π/4
        point1 = axes.coords_to_point(PI/4, np.sin(PI/4))
        dot1 = Dot(point1, color=YELLOW, radius=0.08)
        label1 = MathTex("(\\frac{\\pi}{4}, \\frac{\\sqrt{2}}{2})", font_size=24)
        label1.next_to(dot1, UR, buff=0.1)
        
        # Zero of exponential
        x_zero = np.log(4) / 0.3  # Solve 0.5*e^(0.3x) - 2 = 0
        point2 = axes.coords_to_point(x_zero, 0)
        dot2 = Dot(point2, color=YELLOW, radius=0.08)
        label2 = MathTex(f"({x_zero:.2f}, 0)", font_size=24)
        label2.next_to(dot2, DOWN, buff=0.1)
        
        self.play(
            FadeIn(dot1), Write(label1),
            FadeIn(dot2), Write(label2)
        )
        self.wait()
        
        # 4. Area under curve
        area = axes.get_area(sin_graph, x_range=[0, PI], color=RED, opacity=0.3)
        area_label = MathTex("\\int_0^{\\pi} \\sin(x)\\,dx = 2", font_size=28)
        area_label.to_edge(RIGHT).shift(UP)
        
        self.play(FadeIn(area), Write(area_label))
        self.wait()
        
        # 5. Dynamic tracking
        tracker = ValueTracker(-4)
        
        # Vertical line that follows x
        v_line = always_redraw(lambda:
            axes.get_vertical_line(
                axes.coords_to_point(tracker.get_value(), 0),
                color=PURPLE,
                line_func=DashedLine
            )
        )
        
        # Dots on each graph
        dots = VGroup(
            always_redraw(lambda: Dot(
                axes.coords_to_point(tracker.get_value(), np.sin(tracker.get_value())),
                color=RED
            )),
            always_redraw(lambda: Dot(
                axes.coords_to_point(tracker.get_value(), np.cos(tracker.get_value())),
                color=BLUE
            )),
            always_redraw(lambda: Dot(
                axes.coords_to_point(
                    tracker.get_value(), 
                    0.5 * np.exp(0.3*tracker.get_value()) - 2
                ),
                color=GREEN
            ))
        )
        
        # Value display
        value_display = always_redraw(lambda:
            VGroup(
                MathTex(f"x = {tracker.get_value():.2f}", font_size=24),
                MathTex(f"\\sin(x) = {np.sin(tracker.get_value()):.2f}", 
                       font_size=24, color=RED),
                MathTex(f"\\cos(x) = {np.cos(tracker.get_value()):.2f}", 
                       font_size=24, color=BLUE),
                MathTex(f"0.5e^{{0.3x}} - 2 = {0.5 * np.exp(0.3*tracker.get_value()) - 2:.2f}", 
                       font_size=24, color=GREEN)
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(UP)
        )
        
        self.play(
            Create(v_line),
            FadeIn(dots),
            Write(value_display),
            FadeOut(area),
            FadeOut(area_label),
            FadeOut(dot1), FadeOut(label1),
            FadeOut(dot2), FadeOut(label2)
        )
        
        # Animate tracking
        self.play(tracker.animate.set_value(4), run_time=4)
        self.play(tracker.animate.set_value(0), run_time=2)
        self.wait()
        
        # Final message
        final_text = Text("maniml: Complete Axis Control!", font_size=36, color=GOLD)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)