#!/usr/bin/env python3
"""
Test plotting and graphing functions on coordinate systems in maniml.
"""

from maniml import *


class BasicPlottingTest(Scene):
    """Test basic function plotting on 2D axes."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
            y_axis_config={"numbers_to_include": np.arange(-2, 3, 1)},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(axes_labels))
        self.wait()
        
        # Plot various functions
        # Linear function
        linear = axes.plot(lambda x: 0.5 * x + 1, color=GREEN)
        linear_label = axes.get_graph_label(linear, label="y = 0.5x + 1")
        
        self.play(Create(linear))
        self.play(Write(linear_label))
        self.wait()
        
        # Quadratic function
        quadratic = axes.plot(lambda x: x**2 - 1, color=YELLOW)
        quad_label = axes.get_graph_label(quadratic, label="y = x^2 - 1", x_val=-2)
        
        self.play(Create(quadratic))
        self.play(Write(quad_label))
        self.wait()
        
        # Sine function
        sine = axes.plot(lambda x: np.sin(x), color=RED)
        sine_label = axes.get_graph_label(sine, label="y = \\sin(x)", x_val=1.5)
        
        self.play(Create(sine))
        self.play(Write(sine_label))
        self.wait()
        
        # Clear and fade out
        self.play(
            FadeOut(linear), FadeOut(linear_label),
            FadeOut(quadratic), FadeOut(quad_label),
            FadeOut(sine), FadeOut(sine_label),
        )
        self.wait()


class ParametricPlottingTest(Scene):
    """Test parametric curves and advanced plotting."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": GREY},
        )
        
        self.play(Create(axes))
        
        # Parametric circle
        circle_param = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=BLUE
        )
        
        self.play(Create(circle_param))
        self.wait()
        
        # Lissajous curve
        lissajous = axes.plot_parametric_curve(
            lambda t: np.array([3 * np.sin(2 * t), 3 * np.sin(3 * t), 0]),
            t_range=[0, 2 * PI],
            color=PURPLE
        )
        
        self.play(Transform(circle_param, lissajous))
        self.wait()
        
        # Spiral
        spiral = axes.plot_parametric_curve(
            lambda t: np.array([t * np.cos(t), t * np.sin(t), 0]),
            t_range=[0, 4 * PI],
            color=ORANGE
        )
        
        self.play(Transform(circle_param, spiral))
        self.wait()


class AreaUnderCurveTest(Scene):
    """Test plotting areas under curves and Riemann sums."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            axis_config={"color": BLUE},
        )
        
        self.play(Create(axes))
        
        # Plot function
        func = axes.plot(lambda x: 0.1 * x**2 + 1, color=GREEN)
        func_label = axes.get_graph_label(func, label="f(x) = 0.1x^2 + 1")
        
        self.play(Create(func), Write(func_label))
        self.wait()
        
        # Show area under curve
        area = axes.get_area(func, x_range=[1, 4], color=BLUE, opacity=0.5)
        
        self.play(FadeIn(area))
        self.wait()
        
        # Show Riemann rectangles
        riemann_rects = axes.get_riemann_rectangles(
            func,
            x_range=[1, 4],
            n_iterations=6,
            color=YELLOW,
            fill_opacity=0.5,
            stroke_width=1,
            stroke_color=WHITE
        )
        
        self.play(Transform(area, riemann_rects))
        self.wait()
        
        # Increase number of rectangles
        finer_rects = axes.get_riemann_rectangles(
            func,
            x_range=[1, 4],
            n_iterations=20,
            color=YELLOW,
            fill_opacity=0.5,
            stroke_width=0.5,
            stroke_color=WHITE
        )
        
        self.play(Transform(area, finer_rects))
        self.wait()


class DerivativeVisualizationTest(Scene):
    """Test derivative visualization with tangent lines."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            axis_config={"color": GREY},
        )
        
        self.play(Create(axes))
        
        # Plot function
        func = axes.plot(lambda x: 0.5 * x**2, color=BLUE)
        func_label = axes.get_graph_label(func, label="f(x) = 0.5x^2", x_val=2)
        
        self.play(Create(func), Write(func_label))
        self.wait()
        
        # Create moving dot
        x_tracker = ValueTracker(1)
        
        dot = always_redraw(lambda: Dot(
            axes.input_to_graph_point(x_tracker.get_value(), func),
            color=YELLOW
        ))
        
        # Create tangent line
        def get_tangent_line():
            x = x_tracker.get_value()
            # Derivative of 0.5x^2 is x
            slope = x
            
            # Get point on curve
            point = axes.input_to_graph_point(x, func)
            
            # Create tangent line
            tangent = axes.get_tangent_line(x, func, length=4)
            tangent.set_color(RED)
            return tangent
        
        tangent_line = always_redraw(get_tangent_line)
        
        # Add slope label
        slope_label = always_redraw(lambda: MathTex(
            f"m = {x_tracker.get_value():.1f}",
            color=RED
        ).next_to(tangent_line, UP))
        
        self.play(
            FadeIn(dot),
            Create(tangent_line),
            Write(slope_label)
        )
        self.wait()
        
        # Animate the dot moving
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()
        self.play(x_tracker.animate.set_value(2), run_time=3)
        self.wait()


class PolarPlottingTest(Scene):
    """Test plotting in polar coordinates."""
    
    def construct(self):
        # Create polar plane
        polar_plane = PolarPlane(
            azimuth_units="PI radians",
            size=6,
            azimuth_compact_fraction=False,
            azimuth_offset=0,
        )
        
        self.play(Create(polar_plane))
        self.wait()
        
        # Plot rose curve
        rose = polar_plane.plot_polar_graph(
            lambda theta: 2 * np.cos(3 * theta),
            theta_range=[0, 2 * PI],
            color=PINK
        )
        
        self.play(Create(rose))
        self.wait()
        
        # Plot spiral
        spiral = polar_plane.plot_polar_graph(
            lambda theta: 0.5 * theta,
            theta_range=[0, 4 * PI],
            color=BLUE
        )
        
        self.play(Transform(rose, spiral))
        self.wait()
        
        # Plot cardioid
        cardioid = polar_plane.plot_polar_graph(
            lambda theta: 1 + np.cos(theta),
            theta_range=[0, 2 * PI],
            color=RED
        )
        
        self.play(Transform(rose, cardioid))
        self.wait()


class MultipleGraphsTest(Scene):
    """Test plotting multiple graphs with intersections and transformations."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY},
        )
        
        self.play(Create(axes))
        
        # Plot multiple functions
        linear = axes.plot(lambda x: 0.5 * x, color=BLUE, use_smoothing=False)
        parabola = axes.plot(lambda x: 0.2 * x**2 - 1, color=GREEN)
        cubic = axes.plot(lambda x: 0.05 * x**3, color=RED)
        
        # Labels
        linear_label = axes.get_graph_label(linear, "y = 0.5x", x_val=3)
        parabola_label = axes.get_graph_label(parabola, "y = 0.2x^2 - 1", x_val=-3)
        cubic_label = axes.get_graph_label(cubic, "y = 0.05x^3", x_val=2)
        
        # Animate creation
        self.play(
            Create(linear), Write(linear_label),
            Create(parabola), Write(parabola_label),
            Create(cubic), Write(cubic_label),
        )
        self.wait()
        
        # Mark intersection points
        # Find approximate intersections
        intersection1 = Dot(axes.coords_to_point(0, 0), color=YELLOW)
        intersection2 = Dot(axes.coords_to_point(2.24, 1.12), color=YELLOW)  # Approximate
        
        self.play(
            FadeIn(intersection1),
            FadeIn(intersection2),
        )
        self.wait()
        
        # Transform one function to another
        transformed = axes.plot(lambda x: np.sin(x), color=PURPLE)
        self.play(Transform(parabola, transformed))
        self.wait()


class ImplicitPlotTest(Scene):
    """Test implicit curves and level sets."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY},
        )
        
        self.play(Create(axes))
        
        # Create implicit circle x^2 + y^2 = 4
        # We'll approximate with parametric
        circle = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=BLUE
        )
        circle_label = MathTex("x^2 + y^2 = 4", color=BLUE).to_corner(UR)
        
        self.play(Create(circle), Write(circle_label))
        self.wait()
        
        # Create ellipse (x/3)^2 + (y/2)^2 = 1
        ellipse = axes.plot_parametric_curve(
            lambda t: np.array([3 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=GREEN
        )
        ellipse_label = MathTex("\\frac{x^2}{9} + \\frac{y^2}{4} = 1", color=GREEN).to_corner(UR)
        
        self.play(
            Transform(circle, ellipse),
            Transform(circle_label, ellipse_label)
        )
        self.wait()
        
        # Create hyperbola x^2 - y^2 = 1
        # Right branch
        hyperbola_right = axes.plot_parametric_curve(
            lambda t: np.array([np.cosh(t), np.sinh(t), 0]),
            t_range=[-2, 2],
            color=RED
        )
        # Left branch
        hyperbola_left = axes.plot_parametric_curve(
            lambda t: np.array([-np.cosh(t), np.sinh(t), 0]),
            t_range=[-2, 2],
            color=RED
        )
        hyperbola_label = MathTex("x^2 - y^2 = 1", color=RED).to_corner(UR)
        
        self.play(
            Transform(circle, hyperbola_right),
            Create(hyperbola_left),
            Transform(circle_label, hyperbola_label)
        )
        self.wait()


class VectorFieldTest(Scene):
    """Test vector fields on coordinate systems."""
    
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": GREY},
        )
        
        self.play(Create(axes))
        
        # Create vector field
        def field_func(pos):
            x, y = pos[:2]
            return np.array([-y, x, 0]) * 0.3
        
        # Create arrows for vector field
        vectors = VGroup()
        for x in np.arange(-3.5, 4, 1):
            for y in np.arange(-3.5, 4, 1):
                start = axes.coords_to_point(x, y)
                vec = field_func(start)
                if np.linalg.norm(vec) > 0.1:
                    arrow = Arrow(
                        start, start + vec,
                        color=BLUE,
                        buff=0,
                        max_stroke_width_to_length_ratio=10,
                        max_tip_length_to_length_ratio=0.3,
                    )
                    vectors.add(arrow)
        
        self.play(Create(vectors), run_time=2)
        self.wait()
        
        # Add a curve that follows the field
        curve = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Create(curve))
        self.wait()
        
        # Show that vectors are tangent to curve
        dot = Dot(color=RED)
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, curve), run_time=4)
        self.wait()


if __name__ == "__main__":
    # Run tests individually
    # Uncomment the test you want to run
    
    # BasicPlottingTest().run()
    # ParametricPlottingTest().run()
    # AreaUnderCurveTest().run()
    # DerivativeVisualizationTest().run()
    # PolarPlottingTest().run()
    # MultipleGraphsTest().run()
    # ImplicitPlotTest().run()
    # VectorFieldTest().run()
    
    # Run first test by default
    # BasicPlottingTest().run()
    # ParametricPlottingTest().run()
    # AreaUnderCurveTest().run()
    # DerivativeVisualizationTest().run()
    # PolarPlottingTest().run()
    MultipleGraphsTest().run()