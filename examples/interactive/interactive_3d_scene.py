from maniml import *

class Interactive3DScene(ThreeDScene):
    def construct(self):
        # Title
        title = Text("Interactive 3D Scene", font_size=36)
        title.to_edge(UP).fix_in_frame()
        self.add(title)
        
        # Instructions
        instructions = VGroup(
            Text("Mouse Controls:", font_size=20),
            Text("• Hold 'd' + move mouse: Rotate camera", font_size=16),
            Text("• Hold 'f' + move mouse: Pan camera", font_size=16),
            Text("• Cmd/Ctrl + scroll: Zoom", font_size=16),
            Text("• Click dots to drag them", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        instructions.to_corner(UL).fix_in_frame()
        self.add(instructions)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 3, 1],
            x_length=10,
            y_length=10,
            z_length=6,
        )
        axes.add_coordinates()
        self.add(axes)
        
        # Create some 3D shapes
        sphere = Sphere(radius=0.5, color=BLUE)
        sphere.shift(3*RIGHT + 2*UP)
        
        cube = Cube(side_length=1, color=RED)
        cube.shift(3*LEFT + 2*UP)
        
        cone = Cone(base_radius=0.5, height=1, color=GREEN)
        cone.shift(2*IN)
        
        cylinder = Cylinder(radius=0.3, height=1.5, color=YELLOW)
        cylinder.shift(2*OUT)
        
        # Add all shapes
        shapes = VGroup(sphere, cube, cone, cylinder)
        self.add(shapes)
        
        # Create draggable control points
        control_points = []
        for i, shape in enumerate(shapes):
            # Create a dot at the shape's position
            dot = Dot3D(
                point=shape.get_center(),
                radius=0.15,
                color=WHITE
            )
            
            # Create drag handler
            def create_drag_handler(shape_ref, dot_ref):
                def drag_handler(mob, event_data):
                    # Get the 3D position from the mouse point
                    # This is a simplified version - in real 3D you'd need ray casting
                    new_pos = event_data["point"]
                    # Keep the original z-coordinate for simplicity
                    new_3d_pos = np.array([new_pos[0], new_pos[1], dot_ref.get_center()[2]])
                    
                    # Move both dot and shape
                    dot_ref.move_to(new_3d_pos)
                    shape_ref.move_to(new_3d_pos)
                    
                    return False
                return drag_handler
            
            # Add drag listener
            dot.add_mouse_drag_listner(create_drag_handler(shape, dot))
            dot.add_updater(lambda m: None)  # Prevent static optimization
            
            control_points.append(dot)
            self.add(dot)
        
        # Add some animated rotation to make it more dynamic
        self.play(
            Rotate(sphere, angle=2*PI, axis=UP, run_time=4),
            Rotate(cube, angle=2*PI, axis=RIGHT, run_time=4),
            Rotate(cone, angle=2*PI, axis=OUT, run_time=4),
            Rotate(cylinder, angle=2*PI, axis=UP+RIGHT, run_time=4),
            rate_func=linear
        )
        
        # Create a polyhedron showcase
        polyhedra = VGroup(
            Tetrahedron().scale(0.5).shift(4*RIGHT),
            Octahedron().scale(0.5).shift(4*RIGHT + 2*IN),
            Dodecahedron().scale(0.3).shift(4*LEFT),
            Icosahedron().scale(0.4).shift(4*LEFT + 2*IN)
        )
        polyhedra.set_color_by_gradient(BLUE, PURPLE, PINK)
        
        self.play(
            *[FadeIn(p, shift=UP) for p in polyhedra],
            run_time=2
        )
        
        # Animate camera movement to show 3D perspective
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        
        # Show coordinate labels that track the shapes
        coord_labels = VGroup()
        for i, (shape, dot) in enumerate(zip(shapes, control_points)):
            label = always_redraw(lambda s=shape, idx=i: 
                Text(
                    f"Shape {idx+1}: ({s.get_x():.1f}, {s.get_y():.1f}, {s.get_z():.1f})",
                    font_size=14
                ).next_to(control_points[idx], DOWN, buff=0.5).fix_in_frame()
            )
            coord_labels.add(label)
        self.add(coord_labels)
        
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # Create a 3D surface
        def func(u, v):
            return np.array([
                u,
                v,
                0.5 * np.sin(2*u) * np.cos(2*v)
            ])
        
        surface = Surface(
            func,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            color=TEAL,
            fill_opacity=0.8
        )
        surface.shift(DOWN)
        
        self.play(FadeIn(surface))
        self.play(
            Rotate(surface, angle=PI/2, axis=UP, run_time=3)
        )
        
        # Final message
        final_text = Text(
            "Try dragging the white dots and rotating the camera!",
            font_size=24,
            color=YELLOW
        )
        final_text.to_edge(DOWN).fix_in_frame()
        self.play(FadeIn(final_text))
        
        self.wait(10)


class Simple3DExample(ThreeDScene):
    """A simpler 3D example to test basic functionality."""
    
    def construct(self):
        # Set up camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # Create axes
        axes = ThreeDAxes()
        self.add(axes)
        
        # Create a simple sphere
        sphere = Sphere(radius=1, color=BLUE)
        self.add(sphere)
        
        # Create a draggable dot
        dot = Dot3D(radius=0.2, color=YELLOW)
        dot.shift(2*RIGHT + UP)
        
        def drag_handler(mob, event_data):
            # Simple 2D dragging in 3D space
            point = event_data["point"]
            mob.move_to(np.array([point[0], point[1], mob.get_center()[2]]))
            return False
        
        dot.add_mouse_drag_listner(drag_handler)
        dot.add_updater(lambda m: None)
        self.add(dot)
        
        # Animate
        self.play(Rotate(sphere, angle=2*PI, axis=UP, run_time=3))
        
        # Add text
        text = Text("Drag the yellow dot!").scale(0.7)
        text.to_edge(UP).fix_in_frame()
        self.add(text)
        
        self.wait(5)