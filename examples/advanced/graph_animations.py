#!/usr/bin/env python3
"""Test graph theory visualizations in maniml."""

from maniml import *
import numpy as np


class BasicGraphTest(Scene):
    """Test basic graph creation and manipulation."""
    
    def construct(self):
        title = Text("Graph Theory Visualizations", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        
        # Test 1: Basic graph creation
        self.test_basic_graph()
        
        # Test 2: Directed graphs
        self.test_directed_graph()
        
        # Test 3: Graph animations
        self.test_graph_animations()
        
        # Test 4: Graph layouts
        self.test_graph_layouts()
        
        # Test 5: Graph algorithms visualization
        self.test_graph_algorithms()
        
    def test_basic_graph(self):
        """Test basic undirected graph."""
        subtitle = Text("Basic Undirected Graph", font_size=36, color=YELLOW)
        subtitle.to_edge(UP)
        self.play(FadeIn(subtitle))
        
        # Create vertices
        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)]
        
        # Try to create graph using Graph class if available
        try:
            from maniml.mobject.graph import Graph
            
            graph = Graph(
                vertices,
                edges,
                layout="circular",
                vertex_config={"color": BLUE, "radius": 0.3},
                edge_config={"color": WHITE}
            )
            
            self.play(Create(graph))
            self.wait()
            
            # Highlight a vertex
            self.play(graph.vertices[1].animate.set_color(RED))
            self.wait()
            
            # Add labels
            labels = graph.add_vertex_labels({
                1: "A", 2: "B", 3: "C", 4: "D", 5: "E"
            })
            self.play(Write(labels))
            self.wait()
            
            self.play(FadeOut(graph), FadeOut(labels))
            
        except ImportError:
            # Fallback: Create graph manually
            warning = Text("Graph class not available, using manual creation", 
                          font_size=24, color=RED)
            warning.next_to(subtitle, DOWN)
            self.play(FadeIn(warning))
            
            # Create vertices manually
            vertex_objects = {}
            positions = {
                1: np.array([-2, 0, 0]),
                2: np.array([-1, 1.5, 0]),
                3: np.array([1, 1.5, 0]),
                4: np.array([2, 0, 0]),
                5: np.array([0, -1.5, 0])
            }
            
            for v, pos in positions.items():
                circle = Circle(radius=0.3, color=BLUE)
                circle.move_to(pos)
                label = Text(str(v), font_size=24)
                label.move_to(circle.get_center())
                vertex_objects[v] = VGroup(circle, label)
            
            # Create edges manually
            edge_objects = []
            for v1, v2 in edges:
                edge = Line(
                    vertex_objects[v1][0].get_center(),
                    vertex_objects[v2][0].get_center(),
                    color=WHITE
                )
                edge_objects.append(edge)
            
            # Animate creation
            self.play(*[Create(v) for v in vertex_objects.values()])
            self.play(*[Create(e) for e in edge_objects])
            self.wait()
            
            # Highlight path
            path_edges = [(1, 2), (2, 4), (4, 5)]
            for v1, v2 in path_edges:
                for edge in edge_objects:
                    start = edge.get_start()
                    end = edge.get_end()
                    v1_pos = vertex_objects[v1][0].get_center()
                    v2_pos = vertex_objects[v2][0].get_center()
                    
                    if (np.allclose(start, v1_pos) and np.allclose(end, v2_pos)) or \
                       (np.allclose(start, v2_pos) and np.allclose(end, v1_pos)):
                        self.play(edge.animate.set_color(RED))
                        break
            
            self.wait()
            self.play(FadeOut(warning))
            self.play(*[FadeOut(v) for v in vertex_objects.values()],
                     *[FadeOut(e) for e in edge_objects])
        
        self.play(FadeOut(subtitle))
        
    def test_directed_graph(self):
        """Test directed graph with arrows."""
        subtitle = Text("Directed Graph", font_size=36, color=YELLOW)
        subtitle.to_edge(UP)
        self.play(FadeIn(subtitle))
        
        # Create directed graph manually with arrows
        vertices = {
            "A": np.array([-2, 1, 0]),
            "B": np.array([0, 2, 0]),
            "C": np.array([2, 1, 0]),
            "D": np.array([0, -1, 0])
        }
        
        # Create vertex objects
        vertex_objects = {}
        for name, pos in vertices.items():
            circle = Circle(radius=0.4, color=GREEN)
            circle.move_to(pos)
            label = Text(name, font_size=32)
            label.move_to(circle.get_center())
            vertex_objects[name] = VGroup(circle, label)
        
        # Create directed edges with arrows
        directed_edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "A"),
            ("B", "D")
        ]
        
        edge_objects = []
        for start, end in directed_edges:
            arrow = Arrow(
                vertex_objects[start][0].get_center(),
                vertex_objects[end][0].get_center(),
                color=WHITE,
                buff=0.4
            )
            edge_objects.append(arrow)
        
        # Animate creation
        self.play(*[GrowFromCenter(v) for v in vertex_objects.values()])
        self.play(*[GrowArrow(e) for e in edge_objects])
        self.wait()
        
        # Animate traversal
        for arrow in edge_objects[:4]:  # Cycle through A->B->C->D->A
            self.play(arrow.animate.set_color(YELLOW), run_time=0.5)
        self.wait()
        
        self.play(*[FadeOut(v) for v in vertex_objects.values()],
                 *[FadeOut(e) for e in edge_objects])
        self.play(FadeOut(subtitle))
        
    def test_graph_animations(self):
        """Test various graph animations."""
        subtitle = Text("Graph Animations", font_size=36, color=YELLOW)
        subtitle.to_edge(UP)
        self.play(FadeIn(subtitle))
        
        # Create a tree structure
        root_pos = np.array([0, 2, 0])
        
        # Tree nodes
        nodes = {}
        positions = {
            1: root_pos,
            2: root_pos + np.array([-2, -1.5, 0]),
            3: root_pos + np.array([2, -1.5, 0]),
            4: root_pos + np.array([-3, -3, 0]),
            5: root_pos + np.array([-1, -3, 0]),
            6: root_pos + np.array([1, -3, 0]),
            7: root_pos + np.array([3, -3, 0])
        }
        
        for i, pos in positions.items():
            node = Dot(point=pos, radius=0.2, color=BLUE)
            label = Text(str(i), font_size=20, color=WHITE)
            label.move_to(node.get_center())
            nodes[i] = VGroup(node, label)
        
        # Tree edges
        tree_edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
        edges = []
        
        for parent, child in tree_edges:
            edge = Line(
                nodes[parent][0].get_center(),
                nodes[child][0].get_center(),
                color=GRAY
            )
            edges.append(edge)
        
        # Animate tree growth
        self.play(FadeIn(nodes[1]))
        
        for i, (parent, child) in enumerate(tree_edges):
            self.play(
                Create(edges[i]),
                FadeIn(nodes[child]),
                run_time=0.5
            )
        
        self.wait()
        
        # Breadth-first search animation
        bfs_text = Text("BFS Traversal", font_size=24, color=GREEN)
        bfs_text.to_edge(DOWN)
        self.play(Write(bfs_text))
        
        # BFS order: 1, 2, 3, 4, 5, 6, 7
        bfs_order = [1, 2, 3, 4, 5, 6, 7]
        for node_id in bfs_order:
            self.play(
                nodes[node_id][0].animate.set_color(GREEN),
                run_time=0.3
            )
        
        self.wait()
        self.play(FadeOut(bfs_text))
        
        # Clean up
        self.play(*[FadeOut(nodes[i]) for i in nodes.keys()],
                 *[FadeOut(e) for e in edges])
        self.play(FadeOut(subtitle))
        
    def test_graph_layouts(self):
        """Test different graph layout algorithms."""
        subtitle = Text("Graph Layouts", font_size=36, color=YELLOW)
        subtitle.to_edge(UP)
        self.play(FadeIn(subtitle))
        
        # Create same graph with different layouts
        n_vertices = 6
        vertices = list(range(n_vertices))
        
        # Create a connected graph
        edges = []
        for i in range(n_vertices):
            for j in range(i + 1, n_vertices):
                if np.random.random() < 0.4:  # 40% chance of edge
                    edges.append((i, j))
        
        # Ensure connected
        for i in range(n_vertices - 1):
            if not any((i, i+1) in edges or (i+1, i) in edges for e in edges):
                edges.append((i, i + 1))
        
        # Layout 1: Circular
        layout_text = Text("Circular Layout", font_size=24)
        layout_text.next_to(subtitle, DOWN)
        self.play(Write(layout_text))
        
        vertex_objects = {}
        edge_objects = []
        
        # Circular positions
        for i in range(n_vertices):
            angle = 2 * PI * i / n_vertices
            pos = 2 * np.array([np.cos(angle), np.sin(angle), 0])
            
            vertex = Circle(radius=0.3, color=ORANGE)
            vertex.move_to(pos)
            label = Text(str(i), font_size=24)
            label.move_to(vertex.get_center())
            vertex_objects[i] = VGroup(vertex, label)
        
        for v1, v2 in edges:
            edge = Line(
                vertex_objects[v1][0].get_center(),
                vertex_objects[v2][0].get_center(),
                color=GRAY
            )
            edge_objects.append(edge)
        
        self.play(*[Create(v) for v in vertex_objects.values()])
        self.play(*[Create(e) for e in edge_objects], run_time=0.5)
        self.wait()
        
        # Transform to grid layout
        self.play(FadeOut(layout_text))
        layout_text = Text("Grid Layout", font_size=24)
        layout_text.next_to(subtitle, DOWN)
        self.play(Write(layout_text))
        
        # Grid positions
        grid_positions = {}
        cols = 3
        for i in range(n_vertices):
            row = i // cols
            col = i % cols
            pos = np.array([col * 1.5 - 1.5, -row * 1.5 + 1, 0])
            grid_positions[i] = pos
        
        # Animate transition
        animations = []
        for i, new_pos in grid_positions.items():
            animations.append(vertex_objects[i].animate.move_to(new_pos))
        
        # Update edges
        for j, (v1, v2) in enumerate(edges):
            new_edge = Line(
                grid_positions[v1],
                grid_positions[v2],
                color=GRAY
            )
            animations.append(Transform(edge_objects[j], new_edge))
        
        self.play(*animations)
        self.wait()
        
        # Clean up
        self.play(
            *[FadeOut(v) for v in vertex_objects.values()],
            *[FadeOut(e) for e in edge_objects],
            FadeOut(layout_text)
        )
        self.play(FadeOut(subtitle))
        
    def test_graph_algorithms(self):
        """Test graph algorithm visualizations."""
        subtitle = Text("Graph Algorithms", font_size=36, color=YELLOW)
        subtitle.to_edge(UP)
        self.play(FadeIn(subtitle))
        
        # Create a weighted graph for shortest path
        vertices = ["A", "B", "C", "D", "E"]
        positions = {
            "A": np.array([-3, 0, 0]),
            "B": np.array([-1.5, 1.5, 0]),
            "C": np.array([0, 0, 0]),
            "D": np.array([1.5, 1.5, 0]),
            "E": np.array([3, 0, 0])
        }
        
        # Create vertices
        vertex_objects = {}
        for name, pos in positions.items():
            vertex = Circle(radius=0.4, color=BLUE)
            vertex.move_to(pos)
            label = Text(name, font_size=28)
            label.move_to(vertex.get_center())
            vertex_objects[name] = VGroup(vertex, label)
        
        # Weighted edges
        weighted_edges = [
            ("A", "B", 2),
            ("A", "C", 4),
            ("B", "C", 1),
            ("B", "D", 3),
            ("C", "D", 2),
            ("C", "E", 5),
            ("D", "E", 1)
        ]
        
        edge_objects = []
        weight_labels = []
        
        for start, end, weight in weighted_edges:
            edge = Line(
                vertex_objects[start][0].get_center(),
                vertex_objects[end][0].get_center(),
                color=WHITE
            )
            edge_objects.append(edge)
            
            # Add weight label
            mid_point = edge.get_center()
            weight_label = Text(str(weight), font_size=20, color=YELLOW)
            weight_label.move_to(mid_point)
            weight_label.shift(UP * 0.2)
            weight_labels.append(weight_label)
        
        # Create graph
        self.play(*[Create(v) for v in vertex_objects.values()])
        self.play(*[Create(e) for e in edge_objects])
        self.play(*[FadeIn(w) for w in weight_labels])
        
        # Dijkstra's algorithm visualization
        dijkstra_text = Text("Dijkstra's Shortest Path: A to E", font_size=24, color=GREEN)
        dijkstra_text.to_edge(DOWN)
        self.play(Write(dijkstra_text))
        
        # Shortest path: A -> B -> C -> D -> E
        shortest_path = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]
        path_vertices = ["A", "B", "C", "D", "E"]
        
        # Highlight start vertex
        self.play(vertex_objects["A"][0].animate.set_color(GREEN))
        
        # Animate path discovery
        for i, vertex in enumerate(path_vertices[1:], 1):
            # Find edge
            prev_vertex = path_vertices[i-1]
            for j, (start, end, _) in enumerate(weighted_edges):
                if (start == prev_vertex and end == vertex) or \
                   (start == vertex and end == prev_vertex):
                    self.play(
                        edge_objects[j].animate.set_color(GREEN),
                        vertex_objects[vertex][0].animate.set_color(GREEN),
                        run_time=0.7
                    )
                    break
        
        self.wait(2)
        
        # Show total distance
        total_text = Text("Total Distance: 7", font_size=28, color=GREEN)
        total_text.next_to(dijkstra_text, UP)
        self.play(Write(total_text))
        self.wait()
        
        # Clean up
        self.play(
            *[FadeOut(v) for v in vertex_objects.values()],
            *[FadeOut(e) for e in edge_objects],
            *[FadeOut(w) for w in weight_labels],
            FadeOut(dijkstra_text),
            FadeOut(total_text),
            FadeOut(subtitle)
        )
        
        # Final message
        final = Text("Graph Theory Complete!", font_size=48, color=GOLD)
        self.play(Write(final))
        self.wait()


class NetworkGraphTest(Scene):
    """Test network/social graph visualizations."""
    
    def construct(self):
        title = Text("Network Graph Visualization", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP).scale(0.7))
        
        # Create a social network graph
        people = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"]
        
        # Random positions in a rough circle
        positions = {}
        n = len(people)
        for i, person in enumerate(people):
            angle = 2 * PI * i / n + PI/6  # Offset for better layout
            radius = 2.5
            positions[person] = radius * np.array([np.cos(angle), np.sin(angle), 0])
        
        # Create person nodes
        person_nodes = {}
        for person, pos in positions.items():
            # Create icon (circle with initial)
            circle = Circle(radius=0.5, color=BLUE, fill_opacity=0.7)
            circle.move_to(pos)
            
            initial = Text(person[0], font_size=36, color=WHITE)
            initial.move_to(circle.get_center())
            
            name = Text(person, font_size=18)
            name.next_to(circle, DOWN, buff=0.1)
            
            person_nodes[person] = VGroup(circle, initial, name)
        
        # Define connections (friendships)
        connections = [
            ("Alice", "Bob"),
            ("Alice", "Carol"),
            ("Bob", "Carol"),
            ("Bob", "Dave"),
            ("Carol", "Eve"),
            ("Dave", "Eve"),
            ("Dave", "Frank"),
            ("Eve", "Frank")
        ]
        
        # Create connection lines
        connection_lines = []
        for person1, person2 in connections:
            line = Line(
                person_nodes[person1][0].get_center(),
                person_nodes[person2][0].get_center(),
                color=GRAY,
                stroke_width=2
            )
            connection_lines.append(line)
        
        # Animate network creation
        self.play(*[GrowFromCenter(node) for node in person_nodes.values()])
        self.play(*[Create(line) for line in connection_lines])
        self.wait()
        
        # Demonstrate influence spreading
        influence_text = Text("Influence Spreading", font_size=28, color=YELLOW)
        influence_text.to_edge(DOWN)
        self.play(Write(influence_text))
        
        # Start influence from Alice
        influenced = {"Alice"}
        self.play(person_nodes["Alice"][0].animate.set_color(RED))
        
        # Spread influence through network
        rounds = [
            ["Bob", "Carol"],  # Round 1: Alice's direct connections
            ["Dave", "Eve"],   # Round 2: Second degree connections
            ["Frank"]          # Round 3: Third degree connections
        ]
        
        for round_num, round_people in enumerate(rounds, 1):
            round_text = Text(f"Round {round_num}", font_size=20, color=WHITE)
            round_text.next_to(influence_text, UP)
            self.play(FadeIn(round_text))
            
            animations = []
            for person in round_people:
                if person not in influenced:
                    animations.append(person_nodes[person][0].animate.set_color(RED))
                    influenced.add(person)
                    
                    # Highlight connections
                    for i, (p1, p2) in enumerate(connections):
                        if (p1 in influenced and p2 == person) or \
                           (p2 in influenced and p1 == person):
                            animations.append(connection_lines[i].animate.set_color(ORANGE))
            
            self.play(*animations)
            self.wait(0.5)
            self.play(FadeOut(round_text))
        
        self.wait()
        
        # Show network statistics
        stats_text = VGroup(
            Text("Network Statistics:", font_size=24, color=WHITE),
            Text(f"Nodes: {len(people)}", font_size=20),
            Text(f"Edges: {len(connections)}", font_size=20),
            Text(f"Avg Degree: {2*len(connections)/len(people):.1f}", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT)
        stats_text.to_edge(LEFT).shift(DOWN)
        
        self.play(Write(stats_text))
        self.wait(2)
        
        # Clean up
        self.play(
            *[FadeOut(node) for node in person_nodes.values()],
            *[FadeOut(line) for line in connection_lines],
            FadeOut(influence_text),
            FadeOut(stats_text),
            FadeOut(title)
        )


class GraphMatrixTest(Scene):
    """Test graph representations using matrices."""
    
    def construct(self):
        title = Text("Graph Matrix Representations", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP).scale(0.7))
        
        # Create a simple graph
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        
        # Create graph visualization
        graph_title = Text("Graph", font_size=32)
        graph_title.to_edge(LEFT).shift(UP * 2)
        self.play(Write(graph_title))
        
        # Position vertices in a square
        positions = {
            1: np.array([-4, 0.5, 0]),
            2: np.array([-2.5, 0.5, 0]),
            3: np.array([-4, -1, 0]),
            4: np.array([-2.5, -1, 0])
        }
        
        vertex_objects = {}
        for v, pos in positions.items():
            circle = Circle(radius=0.3, color=BLUE)
            circle.move_to(pos)
            label = Text(str(v), font_size=24)
            label.move_to(circle.get_center())
            vertex_objects[v] = VGroup(circle, label)
        
        edge_objects = []
        for v1, v2 in edges:
            edge = Line(
                vertex_objects[v1][0].get_center(),
                vertex_objects[v2][0].get_center(),
                color=WHITE
            )
            edge_objects.append(edge)
        
        self.play(*[Create(v) for v in vertex_objects.values()])
        self.play(*[Create(e) for e in edge_objects])
        
        # Create adjacency matrix
        matrix_title = Text("Adjacency Matrix", font_size=32)
        matrix_title.to_edge(RIGHT).shift(UP * 2)
        self.play(Write(matrix_title))
        
        # Build adjacency matrix
        n = len(vertices)
        adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        for v1, v2 in edges:
            adj_matrix[v1-1][v2-1] = 1
            adj_matrix[v2-1][v1-1] = 1  # Undirected graph
        
        # Create matrix visual
        matrix_group = VGroup()
        matrix_pos = np.array([2, -0.5, 0])
        cell_size = 0.6
        
        # Add row/column labels
        for i in range(n):
            # Row labels
            row_label = Text(str(i+1), font_size=20, color=YELLOW)
            row_label.move_to(matrix_pos + np.array([-cell_size, -i*cell_size, 0]))
            matrix_group.add(row_label)
            
            # Column labels
            col_label = Text(str(i+1), font_size=20, color=YELLOW)
            col_label.move_to(matrix_pos + np.array([i*cell_size, cell_size, 0]))
            matrix_group.add(col_label)
        
        # Create matrix cells
        matrix_cells = []
        for i in range(n):
            row_cells = []
            for j in range(n):
                cell = Square(side_length=cell_size * 0.9)
                cell.move_to(matrix_pos + np.array([j*cell_size, -i*cell_size, 0]))
                
                value = Text(str(adj_matrix[i][j]), font_size=24)
                value.move_to(cell.get_center())
                
                if adj_matrix[i][j] == 1:
                    cell.set_fill(GREEN, opacity=0.3)
                    value.set_color(GREEN)
                else:
                    cell.set_fill(BLACK, opacity=0.3)
                    value.set_color(WHITE)
                
                cell_group = VGroup(cell, value)
                row_cells.append(cell_group)
                matrix_group.add(cell_group)
            matrix_cells.append(row_cells)
        
        self.play(Create(matrix_group))
        self.wait()
        
        # Highlight correspondence
        highlight_text = Text("Edge (2,3) ↔ Matrix[2][3] = 1", font_size=24, color=YELLOW)
        highlight_text.to_edge(DOWN)
        self.play(Write(highlight_text))
        
        # Find edge (2,3)
        for edge in edge_objects:
            start = edge.get_start()
            end = edge.get_end()
            v2_pos = vertex_objects[2][0].get_center()
            v3_pos = vertex_objects[3][0].get_center()
            
            if (np.allclose(start, v2_pos) and np.allclose(end, v3_pos)) or \
               (np.allclose(start, v3_pos) and np.allclose(end, v2_pos)):
                self.play(edge.animate.set_color(YELLOW))
                break
        
        # Highlight matrix cells
        self.play(
            matrix_cells[1][2][0].animate.set_color(YELLOW),
            matrix_cells[2][1][0].animate.set_color(YELLOW)
        )
        
        self.wait(2)
        
        # Show degree calculation
        self.play(FadeOut(highlight_text))
        degree_text = Text("Vertex Degrees = Row Sums", font_size=24, color=YELLOW)
        degree_text.to_edge(DOWN)
        self.play(Write(degree_text))
        
        # Calculate and show degrees
        for i, vertex in enumerate(vertices):
            degree = sum(adj_matrix[i])
            degree_label = Text(f"deg({vertex}) = {degree}", font_size=20)
            degree_label.next_to(vertex_objects[vertex], DOWN, buff=0.5)
            self.play(Write(degree_label))
        
        self.wait(2)
        
        # Clean up
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Final message
        final = Text("Graph Theory & Matrices!", font_size=48, color=GOLD)
        self.play(Write(final))
        self.wait()