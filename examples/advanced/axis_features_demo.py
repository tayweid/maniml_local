from maniml import *

class AxisFeaturesDemo(Scene):
    def construct(self):
        # Title
        title = Text("Axis Features in maniml", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP).scale(0.7))
        
        # 1. Basic axes with labels
        axes1 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={
                "color": BLUE,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2,
            },
            x_axis_config={
                "numbers_to_include": np.arange(-3, 4, 1),
                "numbers_with_elongated_ticks": [-2, 0, 2],
            },
            y_axis_config={
                "numbers_to_include": np.arange(-2, 3, 1),
            }
        )
        axes1.to_edge(LEFT).shift(DOWN * 0.5)
        
        # Add axis labels
        x_label = axes1.get_x_axis_label("x", edge=DOWN, direction=DOWN)
        y_label = axes1.get_y_axis_label("y", edge=LEFT, direction=LEFT)
        
        # Or use get_axis_labels for both at once
        axis_labels = axes1.get_axis_labels(x_label="Time (s)", y_label="Position (m)")
        
        self.play(Create(axes1), Write(axis_labels))
        self.wait()
        
        # 2. Plot with custom labels
        graph = axes1.plot(lambda x: np.sin(2*x), color=RED)
        graph_label = axes1.get_graph_label(
            graph, 
            label="f(x) = \\sin(2x)",
            x_val=1,
            direction=UP,
            buff=0.2
        )
        
        self.play(Create(graph), Write(graph_label))
        self.wait()
        
        # 3. NumberPlane with grid
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4.5,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        plane.to_edge(RIGHT).shift(DOWN * 0.5)
        
        self.play(
            Transform(axes1, plane),
            FadeOut(graph),
            FadeOut(graph_label),
            FadeOut(axis_labels)
        )
        self.wait()
        
        # 4. Advanced plotting features
        advanced_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            x_length=10,
            y_length=6,
            axis_config={"color": GREEN},
        )
        advanced_axes.shift(DOWN * 0.5)
        
        # Add custom tick marks
        advanced_axes.x_axis.add_numbers([0, 2.5, 5, 7.5, 10])
        advanced_axes.y_axis.add_numbers([0, 25, 50, 75, 100])
        
        self.play(Transform(axes1, advanced_axes))
        self.wait()
        
        # Plot multiple functions
        exp_graph = advanced_axes.plot(lambda x: 2**x, color=BLUE)
        quad_graph = advanced_axes.plot(lambda x: x**2, color=YELLOW)
        linear_graph = advanced_axes.plot(lambda x: 10*x, color=GREEN)
        
        # Labels for each
        exp_label = advanced_axes.get_graph_label(exp_graph, "2^x", x_val=8)
        quad_label = advanced_axes.get_graph_label(quad_graph, "x^2", x_val=9)
        linear_label = advanced_axes.get_graph_label(linear_graph, "10x", x_val=5)
        
        self.play(
            Create(exp_graph), Write(exp_label),
            Create(quad_graph), Write(quad_label),
            Create(linear_graph), Write(linear_label),
        )
        self.wait()
        
        # 5. Coordinate labels at specific points
        point1 = advanced_axes.coords_to_point(5, 50)
        point2 = advanced_axes.coords_to_point(7, 49)
        
        dot1 = Dot(point1, color=RED)
        dot2 = Dot(point2, color=RED)
        
        coord_label1 = MathTex("(5, 50)").next_to(dot1, UR, buff=0.1).scale(0.7)
        coord_label2 = MathTex("(7, 49)").next_to(dot2, UR, buff=0.1).scale(0.7)
        
        self.play(
            FadeIn(dot1), Write(coord_label1),
            FadeIn(dot2), Write(coord_label2)
        )
        self.wait()
        
        # 6. Input tracking with label
        x_tracker = ValueTracker(3)
        
        # Create a vertical line that follows x
        v_line = always_redraw(lambda: 
            advanced_axes.get_vertical_line(
                advanced_axes.input_to_graph_point(x_tracker.get_value(), exp_graph),
                color=PURPLE
            )
        )
        
        # Create a label showing the value
        value_label = always_redraw(lambda:
            MathTex(f"x = {x_tracker.get_value():.1f}").next_to(
                advanced_axes.coords_to_point(x_tracker.get_value(), 0), 
                DOWN
            ).scale(0.7)
        )
        
        self.play(Create(v_line), Write(value_label))
        self.play(x_tracker.animate.set_value(8), run_time=3)
        self.play(x_tracker.animate.set_value(1), run_time=3)
        self.wait()
        
        # Final message
        final_text = Text("Full axis control with maniml!", font_size=36)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)


class GridAndTickDemo(Scene):
    def construct(self):
        # Show different axis styles
        title = Text("Grid and Tick Mark Options", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Style 1: Dense grid with minor ticks
        axes1 = Axes(
            x_range=[-5, 5, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"color": BLUE_E},
            x_axis_config={
                "numbers_to_include": range(-5, 6),
                "numbers_with_elongated_ticks": [-5, 0, 5],
                "longer_tick_multiple": 1.5,
            }
        )
        axes1.to_edge(LEFT).shift(UP)
        label1 = Text("Dense Grid", font_size=24).next_to(axes1, DOWN)
        
        # Add grid lines manually
        grid1 = NumberPlane(
            x_range=[-5, 5, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=5,
            y_length=3,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 0.5,
                "stroke_opacity": 0.3,
            },
            faded_line_ratio=2,
        )
        grid1.move_to(axes1)
        
        self.play(Create(grid1), Create(axes1), Write(label1))
        
        # Style 2: Minimal axes
        axes2 = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            x_length=5,
            y_length=3,
            axis_config={
                "color": GREEN,
                "include_tip": False,
            },
            x_axis_config={
                "numbers_to_include": [0, 5, 10],
            },
            y_axis_config={
                "numbers_to_include": [0, 50, 100],
            }
        )
        axes2.to_edge(RIGHT).shift(UP)
        label2 = Text("Minimal", font_size=24).next_to(axes2, DOWN)
        
        self.play(Create(axes2), Write(label2))
        
        # Style 3: Custom styling
        axes3 = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=3,
            axis_config={
                "color": YELLOW,
                "stroke_width": 3,
            },
        )
        axes3.shift(DOWN * 2)
        
        # Add custom labels for pi values
        pi_labels = VGroup()
        for n in range(-4, 5):
            if n == 0:
                label = MathTex("0")
            elif n == 1:
                label = MathTex("\\pi")
            elif n == -1:
                label = MathTex("-\\pi")
            else:
                label = MathTex(f"{n}\\pi")
            label.scale(0.5)
            label.next_to(axes3.coords_to_point(n * PI/2, 0), DOWN)
            pi_labels.add(label)
        
        label3 = Text("Custom π Labels", font_size=24).next_to(axes3, DOWN, buff=0.5)
        
        self.play(Create(axes3), Write(pi_labels), Write(label3))
        
        # Plot trig functions
        sin_graph = axes3.plot(lambda x: np.sin(x), color=RED)
        cos_graph = axes3.plot(lambda x: np.cos(x), color=BLUE)
        
        self.play(Create(sin_graph), Create(cos_graph))
        self.wait(2)


class CoordinateTrackingDemo(Scene):
    def construct(self):
        # Interactive coordinate display
        title = Text("Interactive Coordinate Tracking", font_size=42)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Create axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True},
        )
        axes.add_coordinates()  # This adds coordinate labels to the axes
        
        self.play(Create(axes))
        
        # Create multiple graphs
        graphs = VGroup(
            axes.plot(lambda x: 0.1 * x**3 - x, color=BLUE),
            axes.plot(lambda x: np.sin(x), color=RED),
            axes.plot(lambda x: 0.5 * x, color=GREEN),
        )
        
        graph_labels = VGroup(
            axes.get_graph_label(graphs[0], "f(x) = 0.1x^3 - x", x_val=-2),
            axes.get_graph_label(graphs[1], "g(x) = \\sin(x)", x_val=3),
            axes.get_graph_label(graphs[2], "h(x) = 0.5x", x_val=4),
        )
        
        self.play(
            *[Create(g) for g in graphs],
            *[Write(l) for l in graph_labels]
        )
        
        # Create tracking system
        x_tracker = ValueTracker(-3)
        
        # Dots on each graph
        dots = VGroup(*[
            always_redraw(lambda g=graph: Dot(
                axes.input_to_graph_point(x_tracker.get_value(), g),
                color=g.get_color()
            ))
            for graph in graphs
        ])
        
        # Vertical line
        v_line = always_redraw(lambda:
            DashedLine(
                axes.coords_to_point(x_tracker.get_value(), -3),
                axes.coords_to_point(x_tracker.get_value(), 3),
                color=GREY
            )
        )
        
        # Coordinate display
        coord_display = always_redraw(lambda:
            VGroup(*[
                MathTex(
                    f"({x_tracker.get_value():.1f}, "
                    f"{graph.underlying_function(x_tracker.get_value()):.2f})",
                    color=graph.get_color()
                ).scale(0.6)
                for graph in graphs
            ]).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        )
        
        # x-value display
        x_display = always_redraw(lambda:
            MathTex(f"x = {x_tracker.get_value():.2f}").next_to(
                axes.coords_to_point(x_tracker.get_value(), 0), DOWN
            ).scale(0.7)
        )
        
        self.play(
            FadeIn(dots),
            Create(v_line),
            Write(coord_display),
            Write(x_display)
        )
        
        # Animate tracking
        self.play(x_tracker.animate.set_value(3), run_time=5)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.play(x_tracker.animate.set_value(0), run_time=2)
        
        self.wait(2)