"""
Comprehensive test suite for 3D functionality in maniml.
Tests all 3D objects, transformations, and interactions.
"""

from maniml import *
import numpy as np


class Test3DBasicShapes(ThreeDScene):
    """Test all basic 3D shapes."""
    
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("3D Basic Shapes Test", font_size=32).to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # Test all basic shapes
        shapes = [
            Sphere(radius=0.5, color=BLUE).shift(3*LEFT + 2*UP),
            Cube(side_length=1, color=RED).shift(LEFT + 2*UP),
            Cylinder(radius=0.5, height=1, color=GREEN).shift(RIGHT + 2*UP),
            Cone(base_radius=0.5, height=1, color=YELLOW).shift(3*RIGHT + 2*UP),
            Torus(major_radius=0.8, minor_radius=0.3, color=PURPLE).shift(3*LEFT + DOWN),
            Prism(dimensions=[1, 0.5, 1.5], color=ORANGE).shift(LEFT + DOWN),
            Dodecahedron(color=TEAL).scale(0.5).shift(RIGHT + DOWN),
            Line3D(start=ORIGIN, end=2*RIGHT+UP+OUT, color=WHITE).shift(3*RIGHT + DOWN),
        ]
        
        # Add labels
        labels = []
        shape_names = ["Sphere", "Cube", "Cylinder", "Cone", "Torus", "Prism", "Dodecahedron", "Line3D"]
        for shape, name in zip(shapes, shape_names):
            label = Text(name, font_size=16).next_to(shape, DOWN, buff=0.5)
            label.fix_in_frame()
            labels.append(label)
        
        # Animate appearance
        self.play(
            *[FadeIn(shape, shift=UP) for shape in shapes],
            *[Write(label) for label in labels],
            run_time=2
        )
        
        # Test rotations
        self.play(
            *[Rotate(shape, angle=2*PI, axis=UP, run_time=3) for shape in shapes[:4]],
            *[Rotate(shape, angle=2*PI, axis=RIGHT, run_time=3) for shape in shapes[4:]]
        )
        
        self.wait()


class Test3DTransformations(ThreeDScene):
    """Test 3D transformations and animations."""
    
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES)
        
        # Create a cube to transform
        cube = Cube(side_length=2, color=BLUE)
        self.add(cube)
        
        # Test various transformations
        transformations = [
            ("Scale", lambda: cube.animate.scale(1.5)),
            ("Rotate X", lambda: cube.animate.rotate(PI/2, axis=RIGHT)),
            ("Rotate Y", lambda: cube.animate.rotate(PI/2, axis=UP)),
            ("Rotate Z", lambda: cube.animate.rotate(PI/2, axis=OUT)),
            ("Shift", lambda: cube.animate.shift(2*RIGHT + UP)),
            ("Complex", lambda: cube.animate.scale(0.7).rotate(PI/3, axis=UP+RIGHT).shift(LEFT))
        ]
        
        for name, transform in transformations:
            label = Text(f"Transform: {name}", font_size=24).to_edge(UP)
            label.fix_in_frame()
            self.play(FadeIn(label))
            self.play(transform(), run_time=1.5)
            self.play(FadeOut(label))
            self.wait(0.5)
        
        # Reset
        self.play(cube.animate.move_to(ORIGIN).scale(1).set_color(BLUE))


class Test3DSurfaces(ThreeDScene):
    """Test parametric surfaces and surface operations."""
    
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("3D Surfaces Test", font_size=32).to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # Create different surfaces
        def paraboloid(u, v):
            return np.array([u, v, u**2 + v**2])
        
        def saddle(u, v):
            return np.array([u, v, u**2 - v**2])
        
        def torus_param(u, v):
            R, r = 2, 0.5
            return np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v)
            ])
        
        # Create surfaces
        surface1 = Surface(
            paraboloid,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            color=BLUE
        ).scale(0.5).shift(3*LEFT)
        
        surface2 = Surface(
            saddle,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            color=RED
        ).scale(0.5)
        
        surface3 = Surface(
            torus_param,
            u_range=[0, TAU],
            v_range=[0, TAU],
            resolution=(30, 15),
            color=GREEN
        ).scale(0.5).shift(3*RIGHT)
        
        surfaces = VGroup(surface1, surface2, surface3)
        
        # Animate
        self.play(*[FadeIn(s) for s in surfaces])
        self.frame.add_ambient_rotation(angular_speed=0.3)
        self.wait(3)
        self.frame.clear_updaters()  # Stop rotation
        
        # Show surface deformation
        def wave_transform(point):
            x, y, z = point
            return point + 0.2 * np.sin(3*x) * UP
        
        self.play(
            surface1.animate.apply_function(wave_transform),
            run_time=2
        )
        self.wait()


class Test3DInteractive(ThreeDScene):
    """Test interactive 3D features."""
    
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Instructions
        instructions = VGroup(
            Text("Interactive 3D Test", font_size=24),
            Text("Hold 'd' + drag: Rotate view", font_size=16, color=GREY_A),
            Text("Hold 'f' + drag: Pan view", font_size=16, color=GREY_A),
            Text("Cmd/Ctrl + scroll: Zoom", font_size=16, color=GREY_A),
            Text("Click spheres to drag", font_size=16, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        instructions.fix_in_frame()
        self.add(instructions)
        
        # Create axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 2, 1]
        )
        self.add(axes)
        
        # Create interactive spheres
        spheres = VGroup()
        positions = [
            2*RIGHT + UP,
            2*LEFT + UP,
            2*UP + OUT,
            2*DOWN + IN,
            ORIGIN
        ]
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        
        for pos, color in zip(positions, colors):
            sphere = Sphere(radius=0.3, color=color)
            sphere.move_to(pos)
            
            # Make it draggable
            def create_drag_handler(obj):
                def handler(mob, event_data):
                    # Simple 2D dragging in 3D space
                    point = event_data["point"]
                    new_pos = np.array([point[0], point[1], obj.get_center()[2]])
                    obj.move_to(new_pos)
                    return False
                return handler
            
            sphere.add_mouse_drag_listner(create_drag_handler(sphere))
            sphere.add_updater(lambda m: None)
            spheres.add(sphere)
        
        self.add(spheres)
        
        # Add coordinate display
        coord_text = always_redraw(lambda: VGroup(*[
            Text(
                f"({s.get_x():.1f}, {s.get_y():.1f}, {s.get_z():.1f})",
                font_size=12
            ).move_to(s.get_center() + 0.5*DOWN).fix_in_frame()
            for s in spheres
        ]))
        self.add(coord_text)
        
        # Animate
        self.play(
            *[Rotate(s, angle=2*PI, axis=UP, run_time=3, rate_func=linear) 
              for s in spheres]
        )
        
        self.wait(5)


class Test3DCamera(ThreeDScene):
    """Test camera movements and orientations."""
    
    def construct(self):
        # Create reference objects
        axes = ThreeDAxes()
        cube = Cube(color=BLUE).scale(0.5)
        sphere = Sphere(radius=0.3, color=RED).shift(2*RIGHT)
        cone = Cone(color=GREEN).scale(0.5).shift(2*LEFT)
        
        self.add(axes, cube, sphere, cone)
        
        # Test camera movements
        movements = [
            ("Default View", {"phi": 0, "theta": 0}),
            ("Top View", {"phi": 0, "theta": 0}),
            ("Side View", {"phi": 90*DEGREES, "theta": 0}),
            ("Isometric", {"phi": 60*DEGREES, "theta": -45*DEGREES}),
            ("Custom Angle", {"phi": 45*DEGREES, "theta": 30*DEGREES}),
        ]
        
        for name, kwargs in movements:
            label = Text(f"Camera: {name}", font_size=24).to_edge(UP)
            label.fix_in_frame()
            self.add(label)
            
            self.play(
                self.camera.frame.animate.set_euler_angles(**kwargs),
                run_time=2
            )
            self.wait()
            self.remove(label)
        
        # Test zoom and focus
        self.play(self.camera.frame.animate.scale(0.5))
        self.wait()
        self.play(self.camera.frame.animate.scale(2))
        self.wait()
        self.play(self.camera.frame.animate.move_to(sphere))
        self.wait()
        self.play(self.camera.frame.animate.move_to(ORIGIN))


class Test3DComposite(ThreeDScene):
    """Test complex 3D scenes with multiple elements."""
    
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("3D Composite Scene", font_size=32).to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # Create a complex scene
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-3, 3]
        )
        self.add(axes)
        
        # Create a parametric curve
        def helix(t):
            return np.array([
                2 * np.cos(t),
                2 * np.sin(t),
                0.5 * t
            ])
        
        curve = ParametricFunction(
            helix,
            t_range=[-2*PI, 2*PI],
            color=YELLOW
        )
        
        # Create shapes along the curve
        num_shapes = 8
        shapes = VGroup()
        for i in range(num_shapes):
            t = -2*PI + i * 4*PI / (num_shapes - 1)
            pos = helix(t)
            
            if i % 3 == 0:
                shape = Sphere(radius=0.2, color=RED)
            elif i % 3 == 1:
                shape = Cube(side_length=0.3, color=BLUE)
            else:
                shape = Cone(base_radius=0.2, height=0.3, color=GREEN)
            
            shape.move_to(pos)
            shapes.add(shape)
        
        # Animate construction
        self.play(Create(curve), run_time=2)
        self.play(
            *[FadeIn(shape, scale=0.5) for shape in shapes],
            run_time=2
        )
        
        # Rotate camera around scene
        self.frame.add_ambient_rotation(angular_speed=0.4)
        
        # Animate shapes along curve
        def update_shape_position(shape, dt):
            # Move along helix
            shape.t = getattr(shape, 't', 0) + dt
            new_pos = helix(shape.t)
            shape.move_to(new_pos)
        
        for shape in shapes:
            shape.t = -2*PI + shapes.submobjects.index(shape) * 4*PI / (num_shapes - 1)
            shape.add_updater(update_shape_position)
        
        self.wait(5)
        
        # Stop updates and rotation
        for shape in shapes:
            shape.clear_updaters()
        self.frame.clear_updaters()  # Stop rotation
        
        # Final flourish
        self.play(
            *[shape.animate.scale(2).set_color(WHITE) for shape in shapes],
            curve.animate.set_color(PURPLE).set_stroke(width=8),
            run_time=2
        )
        self.wait()


# Run all tests
if __name__ == "__main__":
    # List all test scenes
    test_scenes = [
        Test3DBasicShapes,
        Test3DTransformations,
        Test3DSurfaces,
        Test3DInteractive,
        Test3DCamera,
        Test3DComposite
    ]
    
    print("Available 3D tests:")
    for i, scene in enumerate(test_scenes):
        print(f"{i+1}. {scene.__name__}")
    print("\nRun with: python -m examples.test_3d_comprehensive TestSceneName")