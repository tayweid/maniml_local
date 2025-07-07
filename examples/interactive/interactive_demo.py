from maniml import *

class InteractiveDemo(Scene):
    def construct(self):
        # Create initial text
        text = Text("maniml Interactive Demo", font_size=36)
        self.play(Write(text))
        self.wait()
        
        # Move it up
        self.play(text.animate.to_edge(UP))
        
        # Create a circle
        circle = Circle(radius=1.5, color=BLUE)
        circle.name = "circle"  # Name for easy access
        self.play(Create(circle))
        
        # Interactive checkpoint
        print("\n" + "="*50)
        print("INTERACTIVE MODE - Try these commands:")
        print("="*50)
        print("circle.set_color(RED)")
        print("circle.shift(LEFT * 2)")
        print("play(circle.animate.scale(1.5))")
        print("play(Rotate(circle, PI/2))")
        print("")
        print("# Create new objects:")
        print("square = Square(color=GREEN)")
        print("add(square)")
        print("play(square.animate.shift(RIGHT * 2))")
        print("")
        print("# Access the scene:")
        print("self.camera.frame.scale(1.2)")
        print("")
        print("Press Ctrl-D when done to continue")
        print("="*50 + "\n")
        
        # Pause for interaction
        self.interactive_embed()
        
        # After interactive mode
        final_text = Text("Changes applied!", font_size=24, color=GREEN)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)
        
        # Fade everything out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Final message
        end_text = Text("Interactive Demo Complete", font_size=42, color=GOLD)
        self.play(Write(end_text))
        self.wait()


class InteractivePlotting(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        )
        axes.add_coordinates()
        axes.name = "axes"
        
        labels = axes.get_axis_labels("x", "y")
        
        self.play(Create(axes), Write(labels))
        
        # Plot initial function
        func1 = lambda x: 0.5 * x**2 - 1
        graph = axes.plot(func1, color=GREEN)
        graph.name = "graph"
        
        graph_label = axes.get_graph_label(graph, "f(x) = 0.5x^2 - 1")
        
        self.play(Create(graph), Write(graph_label))
        self.wait()
        
        print("\n" + "="*50)
        print("INTERACTIVE PLOTTING")
        print("="*50)
        print("# Modify the graph:")
        print("play(graph.animate.set_color(RED))")
        print("")
        print("# Plot new functions:")
        print("sin_graph = axes.plot(lambda x: 2*np.sin(x), color=YELLOW)")
        print("play(Create(sin_graph))")
        print("")
        print("# Add areas:")
        print("area = axes.get_area(graph, x_range=[-2, 2], color=BLUE, opacity=0.3)")
        print("play(Create(area))")
        print("")
        print("# Transform graphs:")
        print("new_graph = axes.plot(lambda x: -x**2 + 2, color=PURPLE)")
        print("play(Transform(graph, new_graph))")
        print("="*50 + "\n")
        
        self.interactive_embed(
            # Make useful functions available
            sin=np.sin,
            cos=np.cos,
            exp=np.exp,
            Transform=Transform,
            ReplacementTransform=ReplacementTransform,
            area=None,  # Placeholder for area
            graph_label=graph_label,
        )
        
        # Continue after interactive mode
        self.wait(2)