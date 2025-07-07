"""Final comprehensive 3D test demonstrating all features."""

from maniml import *
import numpy as np

class Test3DComplete(ThreeDScene):
    def construct(self):
        # Set camera orientation
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("maniml 3D Features Demo", font_size=36, color=YELLOW)
        title.to_edge(UP).fix_in_frame()
        self.add(title)
        
        # Instructions
        instructions = Text(
            "Mouse: Hold 'd' to rotate • Hold 'f' to pan • Cmd/Ctrl + scroll to zoom",
            font_size=14,
            color=GREY_A
        )
        instructions.to_edge(DOWN).fix_in_frame()
        self.add(instructions)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 3, 1]
        )
        axes.set_stroke(opacity=0.5)
        self.add(axes)
        
        # Demonstrate all 3D shapes
        shapes_dict = {
            "Sphere": Sphere(radius=0.5, color=BLUE),
            "Cube": Cube(side_length=0.8, color=RED),
            "Cylinder": Cylinder(radius=0.4, height=0.8, color=GREEN),
            "Cone": Cone(base_radius=0.4, height=0.8, color=YELLOW),
            "Torus": Torus(major_radius=0.6, minor_radius=0.2, color=PURPLE),
            "Prism": Prism(width=0.8, height=0.6, depth=1, color=ORANGE),
            "Dot3D": Dot3D(radius=0.15, color=PINK),
            "Line3D": Line3D(start=ORIGIN, end=UP+RIGHT, color=WHITE)
        }
        
        # Position shapes in a circle
        radius = 3
        for i, (name, shape) in enumerate(shapes_dict.items()):
            angle = i * TAU / len(shapes_dict)
            position = radius * np.array([np.cos(angle), np.sin(angle), 0])
            shape.move_to(position)
            
            # Add label
            label = Text(name, font_size=12).next_to(shape, DOWN, buff=0.3)
            label.fix_in_frame()
            
            self.play(
                FadeIn(shape, scale=0.5),
                Write(label),
                run_time=0.5
            )
        
        self.wait()
        
        # Demonstrate transformations
        transform_label = Text("3D Transformations", font_size=24, color=BLUE)
        transform_label.to_corner(UR).fix_in_frame()
        self.play(FadeIn(transform_label))
        
        # Rotation around different axes
        self.play(
            *[Rotate(shape, angle=PI, axis=UP, run_time=2) 
              for shape in shapes_dict.values()]
        )
        
        self.play(
            *[Rotate(shape, angle=PI/2, axis=RIGHT, run_time=2) 
              for shape in shapes_dict.values()]
        )
        
        # Camera movement
        self.play(FadeOut(transform_label))
        camera_label = Text("Camera Movement", font_size=24, color=GREEN)
        camera_label.to_corner(UR).fix_in_frame()
        self.play(FadeIn(camera_label))
        
        # Animate camera to different positions
        self.play(
            self.frame.animate.reorient(0, 90, 0),  # Top view
            run_time=2
        )
        self.wait(0.5)
        
        self.play(
            self.frame.animate.reorient(0, 0, 0),  # Side view
            run_time=2
        )
        self.wait(0.5)
        
        self.play(
            self.frame.animate.reorient(-30, 60, 0),  # Isometric
            run_time=2
        )
        
        # Add ambient rotation
        self.frame.add_ambient_rotation(angular_speed=0.1)
        self.wait(3)
        
        # Interactive dragging demo
        self.frame.clear_updaters()
        self.play(FadeOut(camera_label))
        
        drag_label = Text("Drag the yellow sphere!", font_size=24, color=YELLOW)
        drag_label.to_corner(UR).fix_in_frame()
        self.play(FadeIn(drag_label))
        
        # Create draggable sphere
        draggable = Sphere(radius=0.8, color=YELLOW)
        draggable.move_to(ORIGIN + 2*UP)
        
        def drag_handler(mob, event_data):
            point = event_data["point"]
            # Keep z coordinate
            new_pos = np.array([point[0], point[1], mob.get_center()[2]])
            mob.move_to(new_pos)
            return False
        
        draggable.add_mouse_drag_listner(drag_handler)
        draggable.add_updater(lambda m: None)
        
        self.play(FadeIn(draggable, scale=2))
        
        # Show position
        position_label = always_redraw(lambda:
            Text(
                f"Position: ({draggable.get_x():.1f}, {draggable.get_y():.1f}, {draggable.get_z():.1f})",
                font_size=16
            ).to_edge(LEFT).to_edge(DOWN, buff=1).fix_in_frame()
        )
        self.add(position_label)
        
        self.wait(5)
        
        # Final message
        final_msg = Text(
            "maniml: ManimCE API + ManimGL Performance!",
            font_size=28,
            color=WHITE
        )
        final_msg.to_edge(DOWN, buff=2).fix_in_frame()
        self.play(
            FadeIn(final_msg, shift=UP),
            FadeOut(instructions)
        )
        
        self.wait(3)


class Test3DMinimal(ThreeDScene):
    """Minimal test to verify basic 3D functionality."""
    
    def construct(self):
        # Basic setup
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Add axes
        axes = ThreeDAxes()
        self.add(axes)
        
        # Add a cube
        cube = Cube(color=BLUE)
        self.add(cube)
        
        # Rotate it
        self.play(Rotate(cube, angle=2*PI, axis=UP+RIGHT, run_time=3))
        
        self.wait()