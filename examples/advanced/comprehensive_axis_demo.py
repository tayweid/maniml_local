from maniml import *

class ComprehensiveAxisDemo(Scene):
    def construct(self):
        # Title
        title = Text("Comprehensive Axis Features", font_size=48)
        subtitle = Text("Labels, Grids, Tracking, and More!", font_size=24)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # 1. Different axis styles
        text1 = Text("1. Axis Styles", font_size=36).to_edge(UP)
        self.play(Write(text1))
        
        # Standard axes
        axes1 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"color": BLUE},
        ).to_edge(LEFT).shift(DOWN*0.5)
        
        label1 = Text("Standard", font_size=20).next_to(axes1, DOWN)
        
        # Axes with tips
        axes2 = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            axis_config={"color": GREEN, "include_tip": True},
        ).to_edge(RIGHT).shift(DOWN*0.5)
        
        label2 = Text("With Tips", font_size=20).next_to(axes2, DOWN)
        
        self.play(
            Create(axes1), Write(label1),
            Create(axes2), Write(label2)
        )
        self.wait()
        
        # Clear
        self.play(
            FadeOut(axes1), FadeOut(label1),
            FadeOut(axes2), FadeOut(label2),
            FadeOut(text1)
        )
        
        # 2. Labels and numbers
        text2 = Text("2. Labels and Numbers", font_size=36).to_edge(UP)
        self.play(Write(text2))
        
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
        )
        
        # Axis labels
        axis_labels = axes.get_axis_labels(
            x_label="x\\text{-axis}", 
            y_label="y\\text{-axis}"
        )
        
        # Add numbers
        axes.x_axis.add_numbers([-4, -2, 0, 2, 4])
        axes.y_axis.add_numbers([-3, -1, 1, 3])
        
        self.play(Create(axes), Write(axis_labels))
        self.wait()
        
        # 3. Function with labeled points
        func = axes.plot(lambda x: 0.25 * x**2 - 2, color=YELLOW)
        func_label = axes.get_graph_label(func, "f(x) = \\frac{1}{4}x^2 - 2")
        
        # Mark specific points
        points = [
            (-2, -1),
            (0, -2),
            (2, -1)
        ]
        
        dots = VGroup()
        labels = VGroup()
        
        for x, y in points:
            dot = Dot(axes.coords_to_point(x, y), color=RED)
            label = MathTex(f"({x}, {y})").scale(0.6).next_to(dot, UR, buff=0.1)
            dots.add(dot)
            labels.add(label)
        
        self.play(Create(func), Write(func_label))
        self.play(
            *[FadeIn(dot) for dot in dots],
            *[Write(label) for label in labels]
        )
        self.wait()
        
        # Clear for next demo
        self.play(
            FadeOut(func), FadeOut(func_label),
            FadeOut(dots), FadeOut(labels),
            FadeOut(axes), FadeOut(axis_labels),
            FadeOut(text2)
        )
        
        # 4. NumberPlane with grid
        text3 = Text("3. NumberPlane Grid", font_size=36).to_edge(UP)
        self.play(Write(text3))
        
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={"color": WHITE},
        )
        
        # Plot parametric curve
        curve = plane.plot_parametric_curve(
            lambda t: np.array([
                3 * np.cos(t),
                2 * np.sin(t),
                0
            ]),
            t_range=[0, 2*PI],
            color=PINK
        )
        
        self.play(Create(plane))
        self.play(Create(curve))
        self.wait()
        
        # 5. Dynamic tracking
        self.play(FadeOut(text3))
        text4 = Text("4. Dynamic Tracking", font_size=36).to_edge(UP)
        self.play(Write(text4))
        
        # Create tracker
        t_tracker = ValueTracker(0)
        
        # Moving dot
        moving_dot = always_redraw(lambda:
            Dot(
                plane.coords_to_point(
                    3 * np.cos(t_tracker.get_value()),
                    2 * np.sin(t_tracker.get_value())
                ),
                color=YELLOW
            )
        )
        
        # Coordinate display
        coord_text = always_redraw(lambda:
            MathTex(
                f"({3 * np.cos(t_tracker.get_value()):.2f}, "
                f"{2 * np.sin(t_tracker.get_value()):.2f})"
            ).to_edge(RIGHT).shift(UP)
        )
        
        # Tangent vector
        def get_tangent():
            t = t_tracker.get_value()
            start = plane.coords_to_point(3 * np.cos(t), 2 * np.sin(t))
            # Derivative of parametric curve
            dx_dt = -3 * np.sin(t)
            dy_dt = 2 * np.cos(t)
            # Normalize
            mag = np.sqrt(dx_dt**2 + dy_dt**2)
            if mag > 0:
                dx_dt /= mag
                dy_dt /= mag
            end = start + np.array([dx_dt, dy_dt, 0])
            return Arrow(start, end, color=GREEN, buff=0)
        
        tangent = always_redraw(get_tangent)
        
        self.play(
            FadeIn(moving_dot),
            Write(coord_text),
            Create(tangent)
        )
        
        # Animate motion
        self.play(t_tracker.animate.set_value(2*PI), run_time=4)
        self.wait()
        
        # Final message
        final = Text("maniml: Full Axis Control!", font_size=42)
        final.to_edge(DOWN)
        self.play(Write(final))
        self.wait(2)