"""Main entry point for maniml command."""

import sys
import os
import importlib.util

def main():
    """Main entry point for maniml command."""
    
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print("""
maniml - Standalone Manim without external dependencies

Usage: maniml [file] [Scene] [options]

Options:
  --help           Show this help message
  -p, --preview    Preview animation after rendering

Examples:
  maniml example.py MyScene
  maniml example.py MyScene -p
""")
        sys.exit(0)
    
    # Get the file and scene name
    script_file = sys.argv[1]
    
    if not os.path.exists(script_file):
        print(f"Error: File '{script_file}' not found")
        sys.exit(1)
    
    # Import and run
    spec = importlib.util.spec_from_file_location("__main__", script_file)
    module = importlib.util.module_from_spec(spec)
    module.__name__ = "__main__"
    
    try:
        spec.loader.exec_module(module)
        
        # If scene name provided, try to render it
        if len(sys.argv) > 2:
            scene_name = sys.argv[2]
            if hasattr(module, scene_name):
                scene_class = getattr(module, scene_name)
                if callable(scene_class):
                    # Always create window for preview mode (default)
                    from maniml.manimgl_core.window import Window
                    window = Window()
                    scene = scene_class(window=window)
                    scene.run()
            else:
                print(f"Error: Scene '{scene_name}' not found in {script_file}")
                sys.exit(1)
    except Exception as e:
        print(f"Error running scene: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()