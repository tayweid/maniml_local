from maniml import *

class InteractiveBezier(Scene):
    def construct(self):
        # Title
        title = Text("Interactive Bezier Curve", font_size=28).to_edge(UP)
        self.add(title)
        
        # Control points
        control_points = [
            np.array([-3, -2, 0]),
            np.array([-1, 2, 0]),
            np.array([1, 2, 0]),
            np.array([3, -2, 0])
        ]
        
        # Create draggable control points
        control_dots = []
        for i, point in enumerate(control_points):
            dot = Dot(point=point, radius=0.12, color=YELLOW)
            label = Text(f"P{i}", font_size=16).next_to(dot, DOWN, buff=0.2)
            
            # Make the dot draggable
            def create_drag_handler(idx, lbl):
                def handler(mob, event_data):
                    mob.move_to(event_data["point"])
                    lbl.next_to(mob, DOWN, buff=0.2)
                    # Update the curve
                    self.update_bezier_curve()
                    return False
                return handler
            
            dot.add_mouse_drag_listner(create_drag_handler(i, label))
            dot.add_updater(lambda m: None)  # Required for interactivity
            
            control_dots.append(dot)
            self.add(dot, label)
        
        # Store control dots for curve updates
        self.control_dots = control_dots
        
        # Create initial bezier curve
        self.bezier_curve = self.create_bezier_curve()
        self.add(self.bezier_curve)
        
        # Add control lines
        self.control_lines = VGroup()
        for i in range(len(control_dots) - 1):
            line = always_redraw(lambda i=i: 
                Line(
                    self.control_dots[i].get_center(),
                    self.control_dots[i+1].get_center(),
                    stroke_color=GREY,
                    stroke_width=1
                )
            )
            self.control_lines.add(line)
        self.add(self.control_lines)
        
        # Add t parameter slider
        t_tracker = ValueTracker(0.5)
        
        # Create slider
        slider_group = VGroup()
        slider_line = Line(LEFT * 3, RIGHT * 3).shift(DOWN * 3)
        slider_dot = Dot(radius=0.1, color=BLUE).move_to(slider_line.point_from_proportion(0.5))
        
        # Make slider draggable
        def slider_handler(mob, event_data):
            # Constrain to slider line
            x = event_data["point"][0]
            x = np.clip(x, -3, 3)
            mob.set_x(x)
            # Update t value
            t = (x + 3) / 6  # Map [-3, 3] to [0, 1]
            t_tracker.set_value(t)
            return False
        
        slider_dot.add_mouse_drag_listner(slider_handler)
        slider_dot.add_updater(lambda m: None)
        
        slider_label = Text("t = ", font_size=20).next_to(slider_line, LEFT)
        t_value = always_redraw(lambda: 
            DecimalNumber(t_tracker.get_value(), num_decimal_places=2)
            .next_to(slider_label, RIGHT)
        )
        
        slider_group.add(slider_line, slider_dot, slider_label, t_value)
        self.add(slider_group)
        
        # Add point on curve at parameter t
        curve_point = always_redraw(lambda:
            Dot(
                self.bezier_curve.point_from_proportion(t_tracker.get_value()),
                radius=0.08,
                color=RED
            )
        )
        self.add(curve_point)
        
        # Instructions
        instructions = VGroup(
            Text("Drag yellow dots to reshape curve", font_size=16),
            Text("Drag blue dot to change parameter t", font_size=16),
            Text("Cmd/Ctrl + drag to pan", font_size=14, color=GREY_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL)
        self.add(instructions)
        
        self.wait(10)
    
    def create_bezier_curve(self):
        """Create a bezier curve from current control points"""
        points = [dot.get_center() for dot in self.control_dots]
        curve = VMobject()
        curve.set_points_as_corners(points)
        curve.make_smooth()
        curve.set_stroke(BLUE, width=3)
        return curve
    
    def update_bezier_curve(self):
        """Update the bezier curve when control points move"""
        new_curve = self.create_bezier_curve()
        self.bezier_curve.become(new_curve)