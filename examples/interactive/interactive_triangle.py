from maniml import *
from manimlib.mobject.interactive import MotionMobject

class InteractiveTriangle(Scene):
    def construct(self):
        # Title
        title = Text("Drag the vertices to reshape the triangle", font_size=24)
        title.to_edge(UP)
        self.add(title)
        
        # Initial triangle vertices
        vertices = [
            np.array([-2, -1, 0]),  # Bottom left
            np.array([2, -1, 0]),   # Bottom right
            np.array([0, 2, 0])     # Top
        ]
        
        # Create the triangle
        triangle = Polygon(*vertices, color=BLUE, fill_opacity=0.3)
        self.add(triangle)
        
        # Create draggable dots for vertices
        vertex_dots = []
        for i, vertex in enumerate(vertices):
            # Create a dot at each vertex
            dot = Dot(point=vertex, radius=0.15, color=YELLOW)
            
            # Create a custom drag handler that updates the triangle
            def create_drag_handler(index):
                def drag_handler(mob, event_data):
                    # Move the dot to the mouse position
                    new_pos = event_data["point"]
                    mob.move_to(new_pos)
                    
                    # Update the triangle's vertices
                    new_vertices = []
                    for j, vdot in enumerate(vertex_dots):
                        new_vertices.append(vdot.get_center())
                    
                    # Recreate the triangle with new vertices
                    triangle.set_points_as_corners([*new_vertices, new_vertices[0]])
                    
                    return False
                return drag_handler
            
            # Add the drag listener to the dot
            dot.add_mouse_drag_listner(create_drag_handler(i))
            
            # Make sure the dot updates (required for interactivity)
            dot.add_updater(lambda m: None)
            
            vertex_dots.append(dot)
            self.add(dot)
        
        # Add edge lines that update with the triangle
        edges = VGroup()
        for i in range(3):
            edge = Line(
                vertex_dots[i].get_center(),
                vertex_dots[(i + 1) % 3].get_center(),
                color=GREEN,
                stroke_width=2
            )
            
            # Add updater to keep edge connected to dots
            def create_edge_updater(start_idx, end_idx):
                def update_edge(line):
                    line.put_start_and_end_on(
                        vertex_dots[start_idx].get_center(),
                        vertex_dots[end_idx].get_center()
                    )
                return update_edge
            
            edge.add_updater(create_edge_updater(i, (i + 1) % 3))
            edges.add(edge)
        
        # Add edges behind the triangle
        self.remove(triangle)
        self.add(edges)
        self.add(triangle)
        
        # Add some text showing coordinates
        coord_text = VGroup()
        for i, dot in enumerate(vertex_dots):
            label = Text(f"V{i+1}", font_size=16).next_to(dot, DOWN, buff=0.3)
            coord = always_redraw(lambda d=dot, idx=i: 
                Text(
                    f"({d.get_x():.1f}, {d.get_y():.1f})", 
                    font_size=14
                ).next_to(vertex_dots[idx], DOWN, buff=0.5)
            )
            coord_text.add(label, coord)
        self.add(coord_text)
        
        # Instructions
        instructions = VGroup(
            Text("Drag the dots to reshape the triangle", font_size=18),
            Text("Cmd/Ctrl + drag to pan, Cmd/Ctrl + scroll to zoom", font_size=14, color=GREY_A)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add(instructions)
        
        # Add area calculation
        area_text = always_redraw(lambda: 
            Text(
                f"Area: {self.calculate_triangle_area(vertex_dots):.2f}",
                font_size=20
            ).to_corner(UR)
        )
        self.add(area_text)
        
        self.wait(10)
    
    def calculate_triangle_area(self, vertex_dots):
        """Calculate area of triangle using cross product formula"""
        p1 = vertex_dots[0].get_center()
        p2 = vertex_dots[1].get_center()
        p3 = vertex_dots[2].get_center()
        
        # Area = 0.5 * |AB × AC|
        ab = p2 - p1
        ac = p3 - p1
        area = 0.5 * abs(ab[0] * ac[1] - ab[1] * ac[0])
        return area