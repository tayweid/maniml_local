"""Simple 3D test to verify basic functionality."""

from maniml import *

class Simple3DTest(ThreeDScene):
    def construct(self):
        # Set camera
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Create axes
        axes = ThreeDAxes()
        self.add(axes)
        
        # Test each shape with correct constructors
        # Sphere - takes radius
        sphere = Sphere(radius=0.5, color=BLUE)
        sphere.shift(2*LEFT)
        
        # Cube - takes side_length
        cube = Cube(side_length=1, color=RED)
        
        # Cylinder - takes height and radius
        cylinder = Cylinder(height=1, radius=0.5, color=GREEN)
        cylinder.shift(2*RIGHT)
        
        # Cone - uses CE-compatible wrapper
        cone = Cone(base_radius=0.5, height=1, color=YELLOW)
        cone.shift(2*UP)
        
        # Torus - takes major_radius and minor_radius (CE style)
        torus = Torus(major_radius=0.8, minor_radius=0.3, color=PURPLE)
        torus.shift(2*DOWN)
        
        # Add all
        self.add(sphere, cube, cylinder, cone, torus)
        
        # Simple rotation
        self.play(
            Rotate(sphere, angle=2*PI, axis=UP),
            Rotate(cube, angle=2*PI, axis=RIGHT),
            Rotate(cylinder, angle=2*PI, axis=OUT),
            run_time=3
        )
        
        self.wait()


class TestDraggable3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES)
        
        # Title
        title = Text("Drag the sphere!", font_size=24).to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # Create a draggable sphere
        sphere = Sphere(radius=0.5, color=BLUE)
        
        def drag_handler(mob, event_data):
            point = event_data["point"]
            # Keep z coordinate
            new_pos = np.array([point[0], point[1], mob.get_center()[2]])
            mob.move_to(new_pos)
            return False
        
        sphere.add_mouse_drag_listner(drag_handler)
        sphere.add_updater(lambda m: None)
        
        self.add(sphere)
        
        # Add axes for reference
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-2, 2]
        )
        axes.set_stroke(opacity=0.5)
        self.add(axes)
        
        # Show coordinates
        coord_label = always_redraw(lambda:
            Text(
                f"Position: ({sphere.get_x():.1f}, {sphere.get_y():.1f}, {sphere.get_z():.1f})",
                font_size=16
            ).to_edge(DOWN).fix_in_frame()
        )
        self.add(coord_label)
        
        self.wait(10)


class Test3DPrism(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Test Prism with CE-compatible parameters
        prism1 = Prism(dimensions=[2, 1, 3], color=BLUE)
        prism1.shift(2*LEFT)
        
        prism2 = Prism(width=1, height=2, depth=1.5, color=RED)
        prism2.shift(2*RIGHT)
        
        self.add(prism1, prism2)
        
        # Rotate to show 3D nature
        self.play(
            Rotate(prism1, angle=2*PI, axis=UP),
            Rotate(prism2, angle=2*PI, axis=RIGHT),
            run_time=3
        )
        
        self.wait()


class TestDot3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Create axes
        axes = ThreeDAxes()
        self.add(axes)
        
        # Test Dot3D at various positions
        dots = VGroup()
        positions = [
            [2, 0, 0],    # x-axis
            [0, 2, 0],    # y-axis
            [0, 0, 2],    # z-axis
            [1, 1, 1],    # diagonal
            [-1, -1, -1], # opposite diagonal
        ]
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        
        for pos, color in zip(positions, colors):
            dot = Dot3D(point=pos, radius=0.1, color=color)
            dots.add(dot)
        
        self.add(dots)
        
        # Animate camera rotation to show 3D positions
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        self.wait()


class Test3DSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Create a parametric surface
        def paraboloid(u, v):
            return np.array([u, v, u**2 + v**2])
        
        surface = Surface(
            paraboloid,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            color=BLUE,
            fill_opacity=0.8
        )
        surface.scale(0.5)
        
        self.add(surface)
        
        # Rotate to show shape
        self.play(Rotate(surface, angle=2*PI, axis=UP, run_time=3))
        
        # Test ParametricSurface (should be same as Surface)
        def saddle(u, v):
            return np.array([u, v, u**2 - v**2])
        
        param_surface = ParametricSurface(
            saddle,
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(15, 15),
            color=RED,
            fill_opacity=0.8
        )
        param_surface.scale(0.5).shift(3*RIGHT)
        
        self.play(FadeIn(param_surface))
        self.wait(2)