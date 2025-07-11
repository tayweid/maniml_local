"""
Scene with CE compatibility using GL backend.
"""

import maniml.manimgl_core
from maniml.manimgl_core.scene.scene import Scene as GLScene
from maniml.manimgl_core.scene.scene import ThreeDScene as GLThreeDScene
from maniml.manimgl_core.scene.scene import SceneState as GLSceneState, EndScene
import warnings
import time
import sys
import inspect
import pyperclip
from pyglet.window import key as PygletWindowKeys
import difflib
import itertools as it
import numpy as np
import copy
from contextlib import contextmanager

# Import IPython for persistent namespace execution
from IPython.terminal.embed import InteractiveShellEmbed

# Import event system - use ManimGL's since that's what the mobjects use
from maniml.manimgl_core.event_handler import EVENT_DISPATCHER
from maniml.manimgl_core.event_handler.event_listner import EventListener
from maniml.manimgl_core.event_handler.event_type import EventType

# Import mobject types for selection
from maniml.manimgl_core.mobject.mobject import Group
from maniml.manimgl_core.mobject.mobject import Mobject
from maniml.manimgl_core.mobject.mobject import Point
from maniml.manimgl_core.mobject.types.vectorized_mobject import VGroup
from maniml.manimgl_core.mobject.types.vectorized_mobject import VMobject
from maniml.manimgl_core.mobject.types.vectorized_mobject import VHighlight
from maniml.manimgl_core.mobject.types.dot_cloud import DotCloud
from maniml.manimgl_core.mobject.geometry import Rectangle
from maniml.manimgl_core.mobject.geometry import Square
from maniml.manimgl_core.mobject.numbers import DecimalNumber
from maniml.manimgl_core.mobject.svg.tex_mobject import Tex
from maniml.manimgl_core.mobject.svg.text_mobject import Text

# Import animation for pasting
from maniml.manimgl_core.animation.fading import FadeIn

# Import constants
from maniml.manimgl_core.constants import DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR
from maniml.manimgl_core.constants import FRAME_WIDTH, FRAME_HEIGHT, SMALL_BUFF
from maniml.manimgl_core.constants import PI, DEG
from maniml.manimgl_core.constants import MANIM_COLORS, WHITE, GREY_A, GREY_C

# Import utilities
from maniml.manimgl_core.utils.family_ops import extract_mobject_family_members
from maniml.manimgl_core.utils.space_ops import get_norm
from maniml.manimgl_core.utils.tex_file_writing import LatexError

try:
    from maniml.scene.file_watcher import SimpleFileWatcher, AnimationTracker
except ImportError:
    SimpleFileWatcher = None
    AnimationTracker = None

# Dummy AutoReloadMixin since we're not using the complex version
class AutoReloadMixin:
    def setup_auto_reload(self):
        pass

# Fix spinning cursor issue - disable debug GL in pyglet
try:
    import pyglet
    pyglet.options['debug_gl'] = False
except ImportError:
    pass

# Key bindings for interactive mode (from ManimGL)
# These would normally come from manim_config but we'll use defaults
SELECT_KEY = 's'
UNSELECT_KEY = 'u'
GRAB_KEY = 'g'
X_GRAB_KEY = 'h'
Y_GRAB_KEY = 'v'
GRAB_KEYS = [GRAB_KEY, X_GRAB_KEY, Y_GRAB_KEY]
RESIZE_KEY = 't'
COLOR_KEY = 'c'
INFORMATION_KEY = 'i'
CURSOR_KEY = ';'

# For keyboard interactions
ARROW_SYMBOLS = [
    PygletWindowKeys.LEFT,
    PygletWindowKeys.UP,
    PygletWindowKeys.RIGHT,
    PygletWindowKeys.DOWN,
]

ALL_MODIFIERS = PygletWindowKeys.MOD_CTRL | PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_SHIFT


class Scene(GLScene):
    """
    CE-compatible Scene using GL backend with InteractiveScene functionality.
    
    Provides CE's API while using GL's fast rendering.
    Includes ManimGL's mouse interaction features.
    
    Checkpoint Navigation Implementation:
    - Uses IPython's InteractiveShellEmbed for persistent namespace execution
    - Stores complete scene state at each checkpoint (before and after animation)
    - Navigation works by:
      - Backward: Restore scene state from checkpoint
      - Forward: If checkpoint exists, restore it; otherwise execute next code
    - IPython's run_cell() maintains proper variable scope and object references
    - temp_skip() context manager controls animation execution during re-runs
    """
    
    # Interaction settings
    scroll_sensitivity = 20  # From ManimGL's default
    drag_to_pan = False  # Disable by default, use Cmd/Ctrl + drag instead
    
    # InteractiveScene configuration
    corner_dot_config = dict(
        color=WHITE,
        radius=0.05,
        glow_factor=2.0,
    )
    selection_rectangle_stroke_color = WHITE
    selection_rectangle_stroke_width = 1.0
    palette_colors = MANIM_COLORS
    selection_nudge_size = 0.05
    cursor_location_config = dict(
        font_size=24,
        fill_color=GREY_C,
        num_decimal_places=3,
    )
    time_label_config = dict(
        font_size=24,
        fill_color=GREY_C,
        num_decimal_places=1,
    )
    crosshair_width = 0.2
    crosshair_style = dict(
        stroke_color=GREY_A,
        stroke_width=[3, 0, 3],
    )
    
    def __init__(self, **kwargs):
        # CE compatibility attributes
        self.renderer = self  # CE code often references scene.renderer
        self.animations = []  # Track animations for CE compatibility
        
        # Checkpoint management
        # Structure: (index, line_number, start_state, end_state, locals, animation_info)
        self.checkpoints = []
        self.current_checkpoint = -1
        self.tight = True  # True if we can execute directly, False if we need to reexecute
        
        # Legacy checkpoint support (will be phased out)
        self.checkpoint_states = {}  # key -> SceneState
        self.animation_count = 0
        self.animation_checkpoints = []  # For backward compatibility
        self.current_animation_index = -1
        
        # Initialize persistent namespace for code execution
        # Will be fully initialized after super().__init__
        self.code_namespace = None
        
        # Auto-reload setup
        self.file_watcher = None
        self.auto_reload_enabled = kwargs.pop('auto_reload', True)  # Enable by default
        self._scene_filepath = None
        self._original_content = None
        self._file_changed_flag = False  # Thread-safe flag
        
        # Track mobject variable names for animation replay
        self._mobject_to_name = {}  # Maps mobject id to variable name
        
        # Animation control for checkpoint navigation
        self._animations_to_play = 1  # How many animations to play
        self._animations_played = 0   # How many have been played so far
        
        # InteractiveScene attributes
        self.selection = Group()
        self.selection_highlight = None  # Will be initialized in setup()
        self.selection_rectangle = None  # Will be initialized in setup()
        self.crosshair = None  # Will be initialized in setup()
        self.information_label = None  # Will be initialized in setup()
        self.color_palette = None  # Will be initialized in setup()
        self.unselectables = []  # Will be populated in setup()
        self.select_top_level_mobs = True
        self.selection_search_set = []
        
        self.is_selecting = False
        self.is_grabbing = False
        
        # Mouse interaction state
        self.mouse_to_selection = None
        self.scale_about_point = None
        self.scale_ref_vect = None
        self.scale_ref_width = None
        self.scale_ref_height = None
        
        super().__init__(**kwargs)
        
        # Initialize persistent namespace after super().__init__ so self is fully initialized
        self.code_namespace = {'self': self}
        exec("from maniml import *", self.code_namespace)
        
        # Initialize IPython shell for code execution
        self.shell = None
        self._initialize_ipython_shell()
        
        # Enable auto-reload if requested
        if self.auto_reload_enabled:
            self.setup_auto_reload()
            
        # Setup interactive elements
        self.setup_interactive_elements()
    
    def _initialize_ipython_shell(self):
        """Initialize IPython shell for persistent namespace execution."""
        try:
            # Create a dummy module to hold the namespace
            import types
            module = types.ModuleType('__main__')
            module.__dict__.update(self.code_namespace)
            
            # Create the shell without displaying banner
            self.shell = InteractiveShellEmbed(
                user_module=module,
                display_banner=False,
                # Don't use IPython's exception handling - we'll handle our own
                xmode='Plain'
            )
            
            # Disable IPython's GUI event loop since we manage our own
            self.shell.enable_gui = lambda gui=None: None
            
        except Exception as e:
            print(f"Warning: Failed to initialize IPython shell: {e}")
            print("Falling back to exec-based execution")
            self.shell = None
    
    def setup_interactive_elements(self):
        """Initialize interactive elements like selection highlight, crosshair, etc."""
        self.selection_highlight = self.get_selection_highlight()
        self.selection_rectangle = self.get_selection_rectangle()
        self.crosshair = self.get_crosshair()
        self.information_label = self.get_information_label()
        self.color_palette = self.get_color_palette()
        self.unselectables = [
            self.selection,
            self.selection_highlight,
            self.selection_rectangle,
            self.crosshair,
            self.information_label,
            self.camera.frame
        ]
        self.regenerate_selection_search_set()
        self.add(self.selection_highlight)
    
    def update_frame(self, dt=0, force_draw=False):
        """Override update_frame to check for file changes."""
        # Check file change flag
        if hasattr(self, '_file_changed_flag') and self._file_changed_flag:
            self._file_changed_flag = False  # Reset flag
            self._handle_file_change()
        
        # Call parent update_frame
        return super().update_frame(dt, force_draw)
    
    def add(self, *mobjects):
        """CE-style add method that returns self for chaining."""
        super().add(*mobjects)
        return self
    
    def remove(self, *mobjects):
        """CE-style remove method that returns self for chaining."""
        super().remove(*mobjects)
        return self
    
    @contextmanager
    def temp_skip(self):
        """Temporarily skip animations in this context."""
        prev_skip = self.skip_animations
        self.skip_animations = True
        try:
            yield
        finally:
            self.skip_animations = prev_skip
    
    def play(self, *animations, **kwargs):
        """
        CE-style play with multiple animations and lag_ratio support.
        """
        # Extract CE-specific kwargs
        run_time = kwargs.pop('run_time', None)
        lag_ratio = kwargs.pop('lag_ratio', 0)
        rate_func = kwargs.pop('rate_func', None)
        
        # Handle run_time
        if run_time is not None:
            for anim in animations:
                if hasattr(anim, 'run_time'):
                    anim.run_time = run_time
        
        # Handle rate_func
        if rate_func is not None:
            for anim in animations:
                if hasattr(anim, 'rate_func'):
                    anim.rate_func = rate_func
        
        # Handle multiple animations
        if len(animations) == 1:
            super().play(animations[0], **kwargs)
        else:
            # Multiple animations
            if lag_ratio > 0:
                from maniml.manimgl_core.animation.composition import LaggedStart
                super().play(LaggedStart(*animations, lag_ratio=lag_ratio), **kwargs)
            else:
                from maniml.manimgl_core.animation.composition import AnimationGroup
                super().play(AnimationGroup(*animations), **kwargs)
        
        return self
    
    def wait(self, duration=1.0, stop_condition=None, frozen_frame=None):
        """CE-style wait with proper event handling."""
        super().wait(duration=duration, stop_condition=stop_condition)
        return self
    
    
    def next_section(self, name="", type="default", skip_animations=False):
        """CE compatibility - sections not supported in GL."""
        warnings.warn(
            "maniml: Sections not supported. Use comments for organization.",
            UserWarning
        )
        return self
    
    def add_subcaption(self, text, duration=None, offset=0):
        """CE compatibility - subcaptions not supported in GL."""
        warnings.warn(
            "maniml: Subcaptions not supported. Use Text objects instead.",
            UserWarning
        )
        return self
    
    def bring_to_front(self, *mobjects):
        """CE compatibility method."""
        for mob in mobjects:
            self.remove(mob)
            self.add(mob)
        return self
    
    def bring_to_back(self, *mobjects):
        """CE compatibility method."""
        for mob in mobjects:
            self.remove(mob)
            # Add at the beginning
            self.mobjects.insert(0, mob)
        return self
    
    def clear(self):
        """CE compatibility - clear the scene."""
        self.remove(*self.mobjects)
        return self
    
    def get_top(self):
        """CE compatibility - get top of frame."""
        return self.camera.frame_shape[1] / 2
    
    def get_bottom(self):
        """CE compatibility - get bottom of frame."""
        return -self.camera.frame_shape[1] / 2
    
    def get_left(self):
        """CE compatibility - get left edge of frame."""
        return -self.camera.frame_shape[0] / 2
    
    def get_right(self):
        """CE compatibility - get right edge of frame."""
        return self.camera.frame_shape[0] / 2
    
    def interactive_embed(self, terminal=True, **kwargs):
        """
        CE compatibility - optionally open an interactive IPython terminal.
        
        Similar to checkpoint_paste in ManimGL and interactive mode in ManimCE.
        Provides access to self and all scene objects in the terminal.
        
        Args:
            terminal: If True (default), launch IPython terminal. If False, just show window.
        """
        # Setup file watching if available
        if SimpleFileWatcher and self.auto_reload_enabled:
            # Get the scene file path
            frame = inspect.currentframe()
            while frame:
                filepath = frame.f_globals.get('__file__')
                if filepath and not filepath.endswith('scene.py'):
                    # Store the filepath for later use
                    self._scene_filepath = filepath
                    
                    # Store the original file content
                    with open(filepath, 'r') as f:
                        self._original_content = f.readlines()
                    
                    # Store the construct method's namespace for later use
                    self._construct_namespace = frame.f_locals.copy()
                    
                    # Create file watcher that sets a flag
                    self._file_watcher = SimpleFileWatcher(
                        filepath,
                        lambda: setattr(self, '_file_changed_flag', True)
                    )
                    self._file_watcher.start()
                    print(f"Auto-reload enabled for: {filepath}")
                    break
                frame = frame.f_back
        
        # If terminal=False, just print instructions and return
        if not terminal:
            print("\nWindow controls:")
            print("  ↑/↓     : Jump between animations")
            print("  ←/→     : Navigate animations (→ plays forward)")
            print("  ESC     : Quit")
            print("\nAuto-reload is enabled - file changes will reload automatically.")
            return
        
        # Skip IPython completely - just print instructions
        print("\nWindow controls:")
        print("  ↑/↓     : Jump between animations")
        print("  ←/→     : Navigate animations (→ plays forward)")
        print("  ESC     : Quit")
        if self._file_watcher:
            print("\nAuto-reload is enabled - file changes will reload automatically.")
    
    # Let ManimGL handle resize naturally - it prevents squishing automatically
    # by using OpenGL viewport management
    
    def setup(self):
        """Setup the scene, including file watcher if enabled."""
        # Call parent setup
        super().setup()
        
        # Initialize checkpoint system
        self.start()
        
        # Setup file watching if enabled
        if SimpleFileWatcher and self.auto_reload_enabled:
            # Use the filepath that was passed from __main__.py
            if hasattr(self, '_scene_filepath') and self._scene_filepath:
                filepath = self._scene_filepath
            else:
                # Fallback: try to find the scene file
                import inspect
                frame = inspect.currentframe()
                filepath = None
                while frame:
                    frame_filepath = frame.f_globals.get('__file__')
                    if frame_filepath and not frame_filepath.endswith('scene.py'):
                        filepath = frame_filepath
                        break
                    frame = frame.f_back
            
            if filepath:
                try:
                    # Store the original file content
                    with open(filepath, 'r') as f:
                        self._original_content = f.readlines()
                    
                    # Create file watcher
                    # The file watcher runs in a separate thread, so we use a flag
                    # that gets checked in the main animation loop
                    self._file_changed_flag = False
                    self._file_watcher = SimpleFileWatcher(
                        filepath,
                        lambda: setattr(self, '_file_changed_flag', True)
                    )
                    self._file_watcher.start()
                    print(f"[AUTO-RELOAD] Watching for changes in: {filepath}")
                except Exception as e:
                    print(f"[AUTO-RELOAD] Failed to setup file watcher: {e}")
    
    # Checkpoint System Core Functions
    
    def start(self):
        """Initialize checkpoint system with blank screen as checkpoint 0."""
        # Create initial blank checkpoint
        # For checkpoint 0, start and end state are the same (blank scene)
        # Use line 0 to indicate no lines should be executed before checkpoint 0
        blank_state = self.get_state()
        self.checkpoints = [(0, 0, blank_state, blank_state, {}, None)]
        self.current_checkpoint = 0
        self.tight = True
        
        # Also update legacy system for compatibility
        self.animation_checkpoints = [(0, 0, blank_state, {}, None)]
        self.current_animation_index = 0
    
    def run_next_code(self):
        """Execute code to play the next animation."""
        if not hasattr(self, '_scene_filepath') or not self._scene_filepath:
            return False
        
        # After reexecute(), the scene is at the current checkpoint state
        # We just need to play ONE more animation
        # Set counters to skip animations we've already seen
        self._animations_to_play = self.current_checkpoint + 2  # Skip first N, play the (N+1)th
        self._animations_played = self.current_checkpoint + 1  # Start counting from where we are
        
        # Get the full construct method code
        code = self._extract_construct_code()
        
        # Execute the code - it will skip to the right place and play one animation
        if self.shell is not None:
            result = self.run_exec_in_namespace(code, self.shell.user_module.__dict__, animations=True)
        else:
            result = self.run_exec_in_namespace(code, self.code_namespace, animations=True)
        
        # Check if we actually played a new animation
        played_new = self._animations_played > self.current_checkpoint + 1
        
        # Reset animation counter
        self._animations_played = 0
        
        return played_new
    
    def run_exec(self, code, animations=True):
        """Execute code with optional animation suppression."""
        # Use persistent namespace
        return self.run_exec_in_namespace(code, self.code_namespace, animations)
    
    def run_exec_in_namespace(self, code, namespace, animations=True):
        """Execute code in a specific namespace with optional animation suppression."""
        try:
            # Check if we have executable code
            has_executable = False
            for line in code.split('\n'):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    has_executable = True
                    break
            
            if not has_executable:
                return False
            
            # Execute with or without animations
            if not animations:
                # Use temp_skip context to skip animations
                with self.temp_skip():
                    self._execute_code(code, namespace)
            else:
                self._execute_code(code, namespace)
            
            # Return whether we played any animations
            return self._animations_played > 0
            
        except Exception as e:
            print(f"Error in run_exec: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _execute_code(self, code, namespace):
        """Helper to execute code using IPython or exec."""
        # Inject line tracking before execution
        tracked_code = self._inject_line_tracking(code)
        
        # Use IPython shell if available, otherwise fall back to exec
        if self.shell is not None:
            # Update the shell's namespace with the provided namespace
            self.shell.user_module.__dict__.update(namespace)
            
            # Execute using IPython's run_cell with tracked code
            result = self.shell.run_cell(tracked_code, silent=True, store_history=False)
            
            # Check for errors
            if result.error_in_exec:
                print(f"Error in run_cell: {result.error_in_exec}")
                raise result.error_in_exec
        else:
            # Fallback to exec if IPython is not available
            compiled = compile(tracked_code, self._scene_filepath, 'exec')
            exec(compiled, namespace)
    
    def reexecute(self):
        """Re-run all code up to current checkpoint by playing N animations."""
        if not hasattr(self, '_scene_filepath') or not self._scene_filepath:
            return None
        
        # Clear the scene to ensure clean slate
        self.clear()
        
        # Clear the namespace completely
        if self.shell is not None:
            # Clear IPython namespace except for 'self'
            self.shell.user_module.__dict__.clear()
            self.shell.user_module.__dict__['self'] = self
            # Re-import maniml
            self.shell.run_cell("from maniml import *", silent=True, store_history=False)
        else:
            # Clear and recreate namespace for exec
            self.code_namespace = {'self': self}
            exec("from maniml import *", self.code_namespace)
        
        # If at checkpoint 0 or before, don't execute any animations
        if self.current_checkpoint <= 0:
            self.tight = True
            return
        
        # Set up to play animations up to current checkpoint
        self._animations_to_play = self.current_checkpoint
        self._animations_played = 0
        
        # Get the full construct method code
        code = self._extract_construct_code()
        
        # Execute the code - animation counting will handle skipping
        if self.shell is not None:
            # Use _execute_code which injects line tracking
            self._execute_code(code, self.shell.user_module.__dict__)
        else:
            self._execute_code(code, self.code_namespace)
        
        # Reset animation counter for next operation
        self._animations_played = 0
        
        # Mark as tight since we're caught up
        self.tight = True
    
    
    
    def _inject_line_tracking(self, code):
        """Inject line tracking statements before each code line."""
        # If code is empty, return as is
        if not code.strip():
            return code
        
        try:
            # Find the starting line number from the original file
            if hasattr(self, '_construct_start_line'):
                base_line = self._construct_start_line
            else:
                # Try to find construct method start line
                base_line = self._find_construct_start_line()
            
            # Simple line-by-line injection approach
            lines = code.split('\n')
            tracked_lines = []
            
            for i, line in enumerate(lines):
                # Skip empty lines and comments
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    tracked_lines.append(line)
                    continue
                
                # Calculate actual line number in the original file
                actual_line = base_line + i
                
                # Get indentation of current line
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                
                # Check if this line might contain a play() call
                # We inject tracking before lines that could have play()
                # Avoid false positives on print statements
                if any(keyword in line for keyword in ['self.play(', 'self.wait(']):
                    # Add line tracking before this line
                    tracked_lines.append(f"{indent_str}self._current_line_in_file = {actual_line}")
                    tracked_lines.append(line)
                    # Check if this is a multi-line statement
                    if line.rstrip().endswith('('):
                        # This starts a multi-line statement
                        # We'll track the end when we see the closing parenthesis
                        pass
                    else:
                        # Single line statement - track the line after
                        tracked_lines.append(f"{indent_str}self._current_line_in_file = {actual_line + 1}")
                elif i > 0 and ')' in line:
                    # This might be the end of a multi-line play() call
                    # Check if we're in a multi-line play context
                    # Look back to find if there's an open play() call
                    in_play_call = False
                    open_parens = 0
                    for j in range(i-1, max(0, i-10), -1):
                        if 'self.play(' in lines[j]:
                            in_play_call = True
                            break
                        # Count parentheses to ensure we're still in the same call
                        open_parens += lines[j].count('(') - lines[j].count(')')
                        if open_parens < 0:
                            break
                    
                    if in_play_call and line.strip() == ')':
                        # This is the closing parenthesis of a play() call
                        tracked_lines.append(line)
                        # Add tracking after the closing parenthesis with the correct line number
                        # The actual line in the file is base_line + i (current line in extracted code)
                        tracked_lines.append(f"{indent_str}self._current_line_in_file = {actual_line + 1}")
                    else:
                        tracked_lines.append(line)
                else:
                    tracked_lines.append(line)
            
            tracked_code = '\n'.join(tracked_lines)
            
            return tracked_code
            
        except Exception as e:
            print(f"[DEBUG] Failed to inject line tracking: {e}")
            import traceback
            traceback.print_exc()
            # If injection fails, return original code
            return code
    
    def _find_construct_start_line(self):
        """Find the line number where construct method starts."""
        if not hasattr(self, '_scene_filepath'):
            return 1
            
        try:
            with open(self._scene_filepath, 'r') as f:
                for i, line in enumerate(f, 1):
                    if 'def construct(self):' in line:
                        # Return line after def construct
                        return i + 1
        except:
            pass
        
        return 1

    def _extract_construct_code(self):
        """Extract just the construct method body."""
        if not hasattr(self, '_scene_filepath'):
            return ""
            
        # Use updated content if available, otherwise current file
        if hasattr(self, '_updated_content') and self._updated_content:
            content = self._updated_content
        else:
            try:
                with open(self._scene_filepath, 'r') as f:
                    content = f.readlines()
            except:
                return ""
        
        in_construct = False
        code_lines = []
        base_indent = None
        construct_line = 0
        
        for i, line in enumerate(content):
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                construct_line = i + 1  # Store construct start line (1-indexed)
                # Store it for line tracking
                self._construct_start_line = construct_line + 1  # Line after def
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Include all lines except interactive_embed
                if 'interactive_embed' not in line:
                    # Remove the base indentation
                    if len(line) > base_indent + 4:
                        dedented = line[base_indent + 4:]  # +4 for method body indent
                    else:
                        dedented = line[base_indent:] if len(line) > base_indent else line
                    
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_nth_animation_code(self, n):
        """Extract code for animation n by commenting out everything before."""
        if n <= 1:
            # First animation, return full code
            return self._extract_construct_code()
        
        if not hasattr(self, '_scene_filepath'):
            return ""
        
        # Get line number where animation n-1 ENDS (after the play() call)
        if n - 2 >= len(self.checkpoints):
            return ""
            
        prev_checkpoint = self.checkpoints[n - 2]
        comment_up_to_line = prev_checkpoint[1]  # Line number after previous animation
        
        # Use updated content if available, otherwise current file
        if hasattr(self, '_updated_content') and self._updated_content:
            content = self._updated_content
        else:
            try:
                with open(self._scene_filepath, 'r') as f:
                    content = f.readlines()
            except:
                return ""
        
        in_construct = False
        code_lines = []
        base_indent = None
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Skip interactive_embed lines
                if 'interactive_embed' in line:
                    continue
                
                # Remove the base indentation
                if len(line) > base_indent + 4:
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                else:
                    dedented = line[base_indent:] if len(line) > base_indent else line
                
                # Comment out lines up to the checkpoint
                if line_no <= comment_up_to_line:
                    if dedented.strip():  # Only comment non-empty lines
                        code_lines.append('# ' + dedented)
                    else:
                        code_lines.append(dedented)
                else:
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    
    def jump_to_n(self, n):
        """Jump to checkpoint n by restoring visual state only."""
        if n <= 0:
            # Restore to blank state
            self.clear()
            self.current_checkpoint = 0
            return
        
        if n > len(self.checkpoints):
            print(f"Checkpoint {n} doesn't exist yet")
            return
            
        # Get the checkpoint
        checkpoint = self.checkpoints[n - 1]
        end_state = checkpoint[3]  # State after animation
        
        # Restore only the visual state (mobjects)
        self.restore_state(end_state)
        
        # Update checkpoint index
        self.current_checkpoint = n - 1
        
        # Force redraw
        self.update_frame(dt=0, force_draw=True)
    
    def play_n(self, n):
        """Play only animation n from restored state."""
        if n <= 0:
            return False
        
        # First restore to state before animation n
        if n > 1:
            if n - 2 >= len(self.checkpoints):
                print(f"Cannot play animation {n} - not enough checkpoints")
                return False
            # Restore to end state of animation n-1
            prev_checkpoint = self.checkpoints[n - 2]
            self.restore_state(prev_checkpoint[3])  # end_state
            
            # Also restore the namespace from that checkpoint
            stored_locals = prev_checkpoint[4]  # caller_locals
            if stored_locals and self.shell is not None:
                # Update namespace with stored variables
                self.shell.user_module.__dict__.update(stored_locals)
        else:
            # Clear for first animation
            self.clear()
            # Clear namespace too
            if self.shell is not None:
                # Keep only essential imports
                keys_to_keep = {'self', 'maniml', 'manim', 'Circle', 'Square', 'Create', 
                                'BLUE', 'RED', 'GREEN', 'YELLOW', 'UP', 'DOWN', 'RIGHT', 'LEFT'}
                keys_to_remove = [k for k in self.shell.user_module.__dict__ 
                                 if k not in keys_to_keep and not k.startswith('_')]
                for key in keys_to_remove:
                    del self.shell.user_module.__dict__[key]
        
        # Extract code with previous animations commented out
        code = self._extract_nth_animation_code(n)
        
        if not code.strip():
            print("No code to execute")
            return False
        
        # Execute the code - only animation n should run
        # Set up to stop after one animation
        self._animations_to_play = 1
        self._animations_played = 0
        
        try:
            # Ensure self is available in namespace
            if self.shell is not None:
                namespace = self.shell.user_module.__dict__
                namespace['self'] = self
                # Use our _execute_code method which injects line tracking
                self._execute_code(code, namespace)
            else:
                # Use exec with our namespace
                namespace = self.code_namespace if hasattr(self, 'code_namespace') else {'self': self}
                self._execute_code(code, namespace)
                
        except Exception as e:
            print(f"Error in play_n: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Check if we played the animation
        played = self._animations_played > 0
        
        # Update checkpoint
        if played:
            self.current_checkpoint = n - 1
        
        # Reset counter
        self._animations_played = 0
        
        return played
    
    
    def get_namespace(self):
        """Get execution namespace with current checkpoint's locals."""
        namespace = {'self': self}
        exec("from maniml import *", namespace)
        
        # Add stored locals from current checkpoint
        if 0 <= self.current_checkpoint < len(self.checkpoints):
            stored_locals = self.checkpoints[self.current_checkpoint][4]  # locals are now at index 4
            if stored_locals:
                namespace.update(stored_locals)
        
        return namespace
    
    def jump_to(self, checkpoint_index):
        """Jump instantly to a checkpoint's final state."""
        if checkpoint_index < 0 or checkpoint_index >= len(self.checkpoints):
            print(f"Invalid checkpoint index: {checkpoint_index}")
            return
            
        checkpoint = self.checkpoints[checkpoint_index]
        # Restore to END state of this checkpoint
        end_state = checkpoint[3]  # end_state is at index 3
        self.restore_state(end_state)
        self.current_checkpoint = checkpoint_index
        self.current_animation_index = checkpoint_index  # Legacy support
        self.tight = False
        
        # Reset namespace when jumping to checkpoint 0 for a fresh start
        if checkpoint_index == 0:
            if self.shell is not None:
                # Clear IPython namespace and re-add imports
                self.shell.user_module.__dict__.clear()
                self.shell.user_module.__dict__['self'] = self
                self.shell.run_cell("from maniml import *", silent=True, store_history=False)
            else:
                self.code_namespace = {'self': self}
                exec("from maniml import *", self.code_namespace)
        
        self.update_frame(dt=0, force_draw=True)
        
        print(f"Jumped to checkpoint {checkpoint_index + 1}/{len(self.checkpoints)}")
    
    def jump_back(self):
        """Jump to previous checkpoint (called by up arrow)."""
        if self.current_checkpoint > 0:
            self.jump_to_n(self.current_checkpoint)
        else:
            print("Already at first checkpoint")
    
    
    def update_frame(self, dt=0, force_draw=False):
        """Override to check for file changes."""
        # Check if file changed
        if hasattr(self, '_file_changed_flag') and self._file_changed_flag:
            self._file_changed_flag = False
            self._handle_file_change()
        
        # Call parent update
        super().update_frame(dt, force_draw)
    
    def interact(self):
        """Override to suppress the tips message."""
        if self.window is None:
            return
        # Don't print the ManimGL tips message - we have our own navigation message
        self.skip_animations = False
        while not self.is_window_closing():
            self.update_frame(1 / self.camera.fps)
    
    def on_key_press(self, symbol, modifiers):
        """Handle key press events for navigation and control."""
        # Call parent implementation first
        super().on_key_press(symbol, modifiers)
        
        # Handle ESC key to quit (always process, regardless of other flags)
        if symbol == PygletWindowKeys.ESCAPE:
            self.quit_interaction = True
            
            # Clear any processing flags
            if hasattr(self, '_processing_key'):
                self._processing_key = False
            
            # Stop file watcher
            if hasattr(self, '_file_watcher') and self._file_watcher:
                self._file_watcher.stop()
            
            # Close the window gracefully
            if hasattr(self, 'window') and self.window:
                self.window.close()
            
            # Set a flag to exit the main loop
            self.done = True
        
        # Handle UP arrow - jump to previous animation
        elif symbol == PygletWindowKeys.UP:
            # Prevent if we're processing another key
            if hasattr(self, '_processing_key') and self._processing_key:
                return
            
            # If animation is playing, skip to end first
            if hasattr(self, 'playing') and self.playing:
                self.skip_animations = True
                return  # Let animation finish, then user can press UP again
                
            if len(self.checkpoints) == 0:
                print("No animations recorded yet")
                return
            
            self.jump_back()
        
        # Handle DOWN arrow - jump to next animation or run new code
        elif symbol == PygletWindowKeys.DOWN:
            # Prevent if we're processing another key
            if hasattr(self, '_processing_key') and self._processing_key:
                return
            
            # If animation is playing, skip to end first
            if hasattr(self, 'playing') and self.playing:
                self.skip_animations = True
                return  # Let animation finish, then user can press DOWN again
            
            # Check if there's a next checkpoint
            if self.current_checkpoint + 1 < len(self.checkpoints):
                # Jump to next checkpoint
                self._processing_key = True
                try:
                    self.jump_to_n(self.current_checkpoint + 2)
                finally:
                    self._processing_key = False
            else:
                # No next checkpoint, play next animation same as RIGHT arrow
                self._processing_key = True
                try:
                    # Use play_n to play the next animation
                    played = self.play_n(self.current_checkpoint + 2)
                    if not played:
                        print("No more animations to run")
                finally:
                    self._processing_key = False
        
        # Handle LEFT arrow - jump to previous animation
        elif symbol == PygletWindowKeys.LEFT:
            # Prevent handling if we're already processing a key
            if hasattr(self, '_processing_key') and self._processing_key:
                return
                
            if len(self.checkpoints) == 0:
                print("No animations recorded yet")
                return
            
            self._processing_key = True
            try:
                if self.current_checkpoint > 0:
                    # Jump to previous checkpoint
                    self.jump_to_n(self.current_checkpoint)
                else:
                    # Already at beginning
                    self.jump_to_n(0)
                    print("Already at the beginning")
            finally:
                self._processing_key = False
        
        # Handle RIGHT arrow - play next animation forward
        elif symbol == PygletWindowKeys.RIGHT:
            # Prevent handling if we're already processing a key
            if hasattr(self, '_processing_key') and self._processing_key:
                return
            
            self._processing_key = True
            try:
                # Use play_n to play the next animation
                played = self.play_n(self.current_checkpoint + 2)
                if not played:
                    print("No more animations to run")
            finally:
                self._processing_key = False
        
        # InteractiveScene key handlers
        char = chr(symbol) if symbol < 256 else ''
        
        # Handle event dispatcher first
        event_data = {"symbol": symbol, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.KeyPressEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
        
        # Selection controls
        if char == SELECT_KEY and (modifiers & ALL_MODIFIERS) == 0:
            self.enable_selection()
        elif char == UNSELECT_KEY:
            self.clear_selection()
        elif char in GRAB_KEYS and (modifiers & ALL_MODIFIERS) == 0:
            self.prepare_grab()
        elif char == RESIZE_KEY and (modifiers & PygletWindowKeys.MOD_SHIFT):
            self.prepare_resizing(about_corner=((modifiers & PygletWindowKeys.MOD_SHIFT) > 0))
        elif symbol == PygletWindowKeys.LSHIFT:
            if self.window.is_key_pressed(ord("t")):
                self.prepare_resizing(about_corner=True)
        elif char == COLOR_KEY and (modifiers & ALL_MODIFIERS) == 0:
            self.toggle_color_palette()
        elif char == INFORMATION_KEY and (modifiers & ALL_MODIFIERS) == 0:
            self.display_information()
        elif char == "c" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.copy_selection()
        elif char == "v" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.paste_selection()
        elif char == "x" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.copy_selection()
            self.delete_selection()
        elif symbol == PygletWindowKeys.BACKSPACE:
            self.delete_selection()
        elif char == "a" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.clear_selection()
            self.add_to_selection(*self.mobjects)
        elif char == "g" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.group_selection()
        elif char == "g" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL | PygletWindowKeys.MOD_SHIFT)):
            self.ungroup_selection()
        elif char == "t" and (modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL)):
            self.toggle_selection_mode()
        elif char == "d" and (modifiers & PygletWindowKeys.MOD_SHIFT):
            self.copy_frame_positioning()
        elif char == "c" and (modifiers & PygletWindowKeys.MOD_SHIFT):
            self.copy_cursor_position()
        elif symbol in ARROW_SYMBOLS and self.selection:
            # Only nudge if we have a selection and not using arrows for navigation
            self.nudge_selection(
                vect=[LEFT, UP, RIGHT, DOWN][ARROW_SYMBOLS.index(symbol)],
                large=(modifiers & PygletWindowKeys.MOD_SHIFT),
            )
        
        # Adding crosshair
        if char == CURSOR_KEY:
            if self.crosshair in self.mobjects:
                self.remove(self.crosshair)
            else:
                self.add(self.crosshair)
        if char == SELECT_KEY:
            self.add(self.crosshair)

        # Conditions for saving state
        if char in [GRAB_KEY, X_GRAB_KEY, Y_GRAB_KEY, RESIZE_KEY]:
            self.save_state()
    
    def on_key_release(self, symbol, modifiers):
        """Handle key release events."""
        super().on_key_release(symbol, modifiers)
        
        # Handle event dispatcher
        event_data = {"symbol": symbol, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.KeyReleaseEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
            
        char = chr(symbol) if symbol < 256 else ''
        if char == SELECT_KEY:
            self.gather_new_selection()
        if char in GRAB_KEYS:
            self.is_grabbing = False
        elif char == INFORMATION_KEY:
            self.display_information(False)
        elif symbol == PygletWindowKeys.LSHIFT and self.window.is_key_pressed(ord(RESIZE_KEY)):
            self.prepare_resizing(about_corner=False)
    
    def on_mouse_motion(self, point, d_point):
        """Handle mouse motion events."""
        super().on_mouse_motion(point, d_point)
        
        # Only move crosshair if it exists and is in the scene
        if hasattr(self, 'crosshair') and self.crosshair and self.crosshair in self.mobjects:
            self.crosshair.move_to(self.frame.to_fixed_frame_point(point))
        
        event_data = {"point": point, "d_point": d_point}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseMotionEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
            
        if self.is_grabbing:
            self.handle_grabbing(point)
        elif self.window.is_key_pressed(ord(RESIZE_KEY)):
            self.handle_resizing(point)
        elif self.window.is_key_pressed(ord(SELECT_KEY)) and self.window.is_key_pressed(PygletWindowKeys.LSHIFT):
            self.handle_sweeping_selection(point)
    
    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        """Handle mouse drag events with proper event order."""
        # IMPORTANT: Update mouse position first
        self.mouse_drag_point.move_to(point)
        
        # Then dispatch to event handlers BEFORE any panning
        event_data = {"point": point, "d_point": d_point, "buttons": buttons, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseDragEvent, **event_data)
        
        # If an object handled the drag, don't pan
        if propagate_event is False:
            return
        
        # Only pan if Cmd/Ctrl is held (and no object handled the event)
        if modifiers & (PygletWindowKeys.MOD_COMMAND | PygletWindowKeys.MOD_CTRL):
            # Pan the scene
            self.frame.shift(-d_point)
        
        # Update crosshair position if it exists
        if hasattr(self, 'crosshair') and self.crosshair and self.crosshair in self.mobjects:
            self.crosshair.move_to(self.frame.to_fixed_frame_point(point))
    
    def on_mouse_press(self, point, button, mods):
        """Handle mouse press events."""
        self.mouse_drag_point.move_to(point)
        event_data = {"point": point, "button": button, "mods": mods}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MousePressEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
    
    def on_mouse_release(self, point, button, mods):
        """Handle mouse release events."""
        event_data = {"point": point, "button": button, "mods": mods}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseReleaseEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
            
        if self.color_palette in self.mobjects:
            self.choose_color(point)
        else:
            self.clear_selection()
    
    def on_mouse_scroll(self, point, offset, x_pixel_offset, y_pixel_offset):
        """Handle mouse scroll events - only zoom with Cmd/Ctrl held."""
        event_data = {"point": point, "offset": offset}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseScrollEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
        
        # Only zoom if Cmd/Ctrl is held
        if self.window.is_key_pressed(PygletWindowKeys.LCOMMAND) or \
           self.window.is_key_pressed(PygletWindowKeys.RCOMMAND) or \
           self.window.is_key_pressed(PygletWindowKeys.LCTRL) or \
           self.window.is_key_pressed(PygletWindowKeys.RCTRL):
            # Use parent's zoom behavior
            rel_offset = y_pixel_offset / self.camera.get_pixel_height()
            self.frame.scale(
                1 - self.scroll_sensitivity * rel_offset,
                about_point=point
            )
    
    def setup_auto_reload(self):
        """Setup automatic file watching and reloading."""
        # Get the scene file path
        frame = inspect.currentframe()
        while frame:
            filepath = frame.f_globals.get('__file__')
            if filepath and not filepath.endswith('scene.py'):
                # Store the filepath for later use
                self._scene_filepath = filepath
                print(f"[AUTO-RELOAD] Scene file path set to: {filepath}")
                break
            frame = frame.f_back
    
    def checkpoint_paste(self, skip=False, record=False, progress_bar=True):
        """
        Run code from clipboard, with automatic checkpointing.
        
        If the code starts with a comment, it will be used as a checkpoint key.
        Running the same checkpoint again will restore to that state first.
        """
        code_string = pyperclip.paste()
        lines = code_string.strip().split('\n')
        
        # Check for checkpoint comment
        checkpoint_key = None
        if lines and lines[0].strip().startswith('#'):
            checkpoint_key = lines[0].strip()
        
        # Handle checkpoint
        if checkpoint_key:
            if checkpoint_key in self.checkpoint_states:
                # Restore to checkpoint
                print(f"Restoring to checkpoint: {checkpoint_key}")
                self.restore_state(self.checkpoint_states[checkpoint_key])
                # Clear later checkpoints
                keys_to_remove = []
                found = False
                for key in self.checkpoint_states:
                    if found:
                        keys_to_remove.append(key)
                    if key == checkpoint_key:
                        found = True
                for key in keys_to_remove:
                    del self.checkpoint_states[key]
            else:
                # Save new checkpoint
                print(f"Creating checkpoint: {checkpoint_key}")
                self.checkpoint_states[checkpoint_key] = self.get_state()
        
        # Execute the code
        with self.temp_config_change(skip=skip, record=record, progress_bar=progress_bar):
            # Get the calling frame's namespace
            frame = inspect.currentframe().f_back
            namespace = frame.f_locals.copy()
            namespace.update(frame.f_globals)
            namespace['self'] = self
            
            try:
                exec(code_string, namespace)
            except Exception as e:
                print(f"Error executing code: {e}")
                import traceback
                traceback.print_exc()
    
    def clear_checkpoints(self):
        """Clear all saved checkpoints."""
        self.checkpoint_states.clear()
        print("All checkpoints cleared")
    
    def reload_scene(self):
        """Reload the scene file and re-run from the beginning."""
        print("Reloading scene...")
        # This will exit the embed and trigger a reload in ManimGL
        if hasattr(self, '_shell'):
            self._shell.run_line_magic("exit_raise", "")
        else:
            raise EndScene()
    
    def edit_checkpoint(self, smallest_line_edit, largest_line_edit):
        """
        Handle file edits by finding affected checkpoints and re-executing.
        
        Args:
            smallest_line_edit: First line that was edited
            largest_line_edit: Last line that was edited
        """
        print(f"\n[EDIT] File changed at lines {smallest_line_edit}-{largest_line_edit}")
        
        # Find the checkpoint to restore to
        # Start from the last checkpoint and work backwards
        restore_checkpoint_index = -1
        
        for i in range(len(self.animation_checkpoints) - 1, -1, -1):
            checkpoint = self.animation_checkpoints[i]
            checkpoint_line = checkpoint[1]
            
            if checkpoint_line < smallest_line_edit:
                # This checkpoint is before the edit, safe to restore to
                restore_checkpoint_index = i
                break
        
        print(f"[EDIT] Restoring to checkpoint {restore_checkpoint_index}")
        
        # Set current checkpoint
        self.current_animation_index = restore_checkpoint_index
        
        # Delete all checkpoints after this index
        if restore_checkpoint_index >= 0:
            self.animation_checkpoints = self.animation_checkpoints[:restore_checkpoint_index + 1]
            # Restore to this checkpoint's state
            checkpoint = self.animation_checkpoints[restore_checkpoint_index]
            self.restore_state(checkpoint[2])
        else:
            # No safe checkpoint, clear everything
            self.animation_checkpoints = []
            self.clear()
        
        print(f"[EDIT] Deleted checkpoints after index {restore_checkpoint_index}")
        
        # According to the spec, we should run animations until the checkpoint line
        # is greater than largest_line_edit
        # Since we just restored to a checkpoint before the edit, we need to run
        # animations until we create a checkpoint past the edit region
        
        # Set a flag to indicate we're in edit mode
        # This will prevent using stale locals during re-execution
        self._in_edit_mode = True
        
        # Special case: if we're already at a checkpoint that ends within the edit region,
        # we need to re-run just that animation
        if restore_checkpoint_index >= 0 and restore_checkpoint_index < len(self.animation_checkpoints):
            current_checkpoint = self.animation_checkpoints[restore_checkpoint_index]
            if smallest_line_edit <= current_checkpoint[1] <= largest_line_edit:
                # The current checkpoint itself is in the edit region
                # Just run this one animation
                print(f"[EDIT] Current checkpoint at line {current_checkpoint[1]} is within edit region")
                print(f"[EDIT] Running just this animation...")
                success = self.run_next_animation(self.current_animation_index)
                print("[EDIT] Edit checkpoint complete")
                return
        
        # Run ONE animation at a time and check
        while True:
            # Check if we should continue
            if self.current_animation_index >= 0 and self.current_animation_index < len(self.animation_checkpoints):
                current_checkpoint = self.animation_checkpoints[self.current_animation_index]
                current_line = current_checkpoint[1]
                
                # If current checkpoint is already past the edit, we're done
                if current_line > largest_line_edit:
                    print(f"[EDIT] Current checkpoint at line {current_line} is past edit region")
                    break
            
            # Run next animation
            print(f"[EDIT] Running next animation...")
            success = self.run_next_animation(self.current_animation_index)
            
            if not success:
                # No more animations
                print("[EDIT] No more animations to run")
                break
            
            # Check the newly created checkpoint
            if self.current_animation_index >= 0 and self.current_animation_index < len(self.animation_checkpoints):
                new_checkpoint = self.animation_checkpoints[self.current_animation_index]
                new_line = new_checkpoint[1]
                print(f"[EDIT] Created checkpoint at line {new_line}")
                
                # If this checkpoint is past the edit region, we're done
                if new_line > largest_line_edit:
                    print(f"[EDIT] Checkpoint at line {new_line} is past edit region, done")
                    break
        
        print("[EDIT] Edit checkpoint complete")
        
        # Clear edit mode flag
        self._in_edit_mode = False
        
        # Force redraw
        self.update_frame(dt=0, force_draw=True)
    
    def on_edit(self):
        """Handle file edits by finding affected checkpoints and re-executing."""
        # Read new content
        with open(self._scene_filepath, 'r') as f:
            new_content = f.readlines()
        
        # Find changed line ranges
        changes = self._find_changed_line_ranges(self._original_content, new_content)
        if not changes:
            print("No changes detected")
            return
        
        smallest_edit = min(start for start, end in changes)
        
        # Find last unedited checkpoint
        last_safe_checkpoint = -1
        for i in range(len(self.checkpoints) - 1, -1, -1):
            if self.checkpoints[i][1] < smallest_edit:  # line_number is still at index 1
                last_safe_checkpoint = i
                break
        
        print(f"[EDIT] Restoring to checkpoint {last_safe_checkpoint}")
        
        # Update checkpoint lists
        self.current_checkpoint = last_safe_checkpoint
        self.current_animation_index = last_safe_checkpoint  # Legacy support
        
        # Truncate checkpoints after the safe point
        if last_safe_checkpoint >= 0:
            self.checkpoints = self.checkpoints[:last_safe_checkpoint + 1]
            self.animation_checkpoints = self.animation_checkpoints[:last_safe_checkpoint + 1]
            # Restore to safe checkpoint
            self.jump_to(last_safe_checkpoint)
        else:
            # No safe checkpoint, clear everything
            self.checkpoints = []
            self.animation_checkpoints = []
            self.clear()
            self.start()  # Reinitialize with blank checkpoint
        
        # Store updated content
        self._updated_content = new_content
        
        # Re-execute if needed
        if last_safe_checkpoint >= 0:
            self.reexecute()
        
        # Run animations until past the edited region
        largest_edit = max(end for start, end in changes)
        while True:
            # Check current position
            if self.current_checkpoint >= 0 and self.current_checkpoint < len(self.checkpoints):
                current_line = self.checkpoints[self.current_checkpoint][1]
                if current_line > largest_edit:
                    break
            
            # Run next animation
            success = self.run_next_code()
            if not success:
                break
        
        print("[EDIT] Edit handling complete")
    
    def _handle_file_change(self):
        """Handle file change by using on_edit."""
        print("\nFile changed! Auto-reloading...")
        
        try:
            # Read new content
            with open(self._scene_filepath, 'r') as f:
                new_content = f.readlines()
            
            # Check syntax
            try:
                compile(''.join(new_content), self._scene_filepath, 'exec')
            except SyntaxError as e:
                print(f"Syntax error at line {e.lineno}: {e.msg}")
                return
            
            # Use on_edit to handle the changes
            self.on_edit()
            
            # Update stored content
            self._original_content = new_content
            
            print("Reload complete!")
            
        except Exception as e:
            print(f"Error during reload: {e}")
            import traceback
            traceback.print_exc()
    
    def _find_first_changed_line(self, new_content):
        """Find the first line that changed."""
        for i, (old_line, new_line) in enumerate(zip(self._original_content, new_content)):
            if old_line != new_line:
                return i + 1  # Line numbers are 1-based
        
        # Check for added lines at the end
        if len(new_content) > len(self._original_content):
            return len(self._original_content) + 1
        
        return None
    
    def _find_changed_line_ranges(self, old_content, new_content):
        """Find all line ranges that changed using proper diff algorithm."""
        import difflib
        
        # Use difflib to get a proper diff
        differ = difflib.SequenceMatcher(None, old_content, new_content)
        changed_ranges = []
        
        # Get the opcodes which tell us what changed
        for tag, i1, i2, j1, j2 in differ.get_opcodes():
            if tag == 'equal':
                # Lines are the same, skip
                continue
            elif tag == 'replace':
                # Lines were replaced - these are actual content changes
                # Use the line numbers from the NEW content
                start = j1 + 1  # Convert to 1-based
                end = j2  # j2 is exclusive, so it's already correct
                changed_ranges.append((start, end))
            elif tag == 'insert':
                # Lines were inserted
                # The inserted lines themselves are "changed"
                start = j1 + 1
                end = j2
                changed_ranges.append((start, end))
            elif tag == 'delete':
                # Lines were deleted
                # We need to handle this carefully - the deletion point matters
                # Use the line number where deletion occurred in the new content
                deletion_point = j1 + 1
                # For deletions, we often want to re-run the animation at that line
                # if it exists (e.g., if we deleted a wait() between animations)
                if deletion_point <= len(new_content):
                    changed_ranges.append((deletion_point, deletion_point))
        
        # Merge overlapping or adjacent ranges
        if changed_ranges:
            merged = []
            current_start, current_end = changed_ranges[0]
            
            for start, end in changed_ranges[1:]:
                if start <= current_end + 1:  # Adjacent or overlapping
                    current_end = max(current_end, end)
                else:
                    merged.append((current_start, current_end))
                    current_start, current_end = start, end
            
            merged.append((current_start, current_end))
            changed_ranges = merged
        
        return changed_ranges
    
    
    def _extract_construct_body(self, content):
        """Extract the body of the construct method as executable code."""
        in_construct = False
        code_lines = []
        base_indent = None
        animations_seen = 0
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Skip interactive_embed calls
                if line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    
                    # Check if this is an animation we should skip
                    if dedented.lstrip().startswith(('self.play(', 'self.wait(')):
                        # Count animations and skip those already executed
                        if animations_seen <= self.current_animation_index:
                            # This animation was already executed, comment it out
                            dedented = f"# Already executed: {dedented.strip()}\n"
                        animations_seen += 1
                    
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_up_to_line(self, end_line, content):
        """Extract code from the construct method up to the given line."""
        in_construct = False
        code_lines = []
        base_indent = None
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Include all lines up to end_line
                if line_no <= end_line and line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_between_lines(self, start_line, end_line, content):
        """Extract code from the construct method between the given lines."""
        in_construct = False
        code_lines = []
        base_indent = None
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Only include lines between start_line and end_line
                if start_line < line_no <= end_line and line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_between_lines(self, start_line, end_line, content):
        """Extract code between two line numbers from the construct method."""
        in_construct = False
        code_lines = []
        base_indent = None
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Only include lines between start and end
                if start_line < line_no <= end_line and line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_after_line(self, start_line, content):
        """Extract code from the construct method after the given line."""
        in_construct = False
        code_lines = []
        base_indent = None
        found_start = False
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Start including lines after start_line
                if line_no > start_line:
                    if line.strip() and 'interactive_embed' not in line:
                        dedented = line[base_indent + 4:]  # +4 for method body indent
                        
                        # Check if this line is a continuation or looks incomplete
                        stripped = dedented.strip()
                        is_continuation = (
                            dedented.startswith(' ') or  # Indented line
                            stripped.startswith(')') or   # Closing parenthesis
                            stripped.startswith(']') or   # Closing bracket  
                            stripped.startswith('}') or   # Closing brace
                            stripped == ',' or            # Just a comma
                            (stripped.endswith(',') and len(stripped) < 10)  # Short line ending with comma
                        )
                        
                        # If this is our first line and it's a continuation,
                        # we need to look back to find the start of the statement
                        if not found_start and not code_lines and is_continuation:
                            # Look back to find the start of the statement
                            for j in range(i - 1, -1, -1):
                                prev_line = content[j]
                                prev_line_no = j + 1
                                if prev_line_no <= start_line:
                                    break
                                if prev_line.strip():
                                    prev_dedented = prev_line[base_indent + 4:] if base_indent is not None else prev_line
                                    # Check if this looks like the start of a statement
                                    if not prev_dedented.startswith(' '):
                                        # Found the start, add all lines from here
                                        for k in range(j, i + 1):
                                            if k + 1 > start_line:
                                                add_line = content[k]
                                                if add_line.strip():
                                                    add_dedented = add_line[base_indent + 4:]
                                                    code_lines.append(add_dedented)
                                        found_start = True
                                        break
                        elif not is_continuation or found_start:
                            # This is a complete statement or we've already started
                            code_lines.append(dedented)
                            found_start = True
        
        return ''.join(code_lines)
    
    def _extract_construct_body_until_line(self, content, end_line):
        """Extract the construct method body from beginning up to the given line."""
        in_construct = False
        code_lines = []
        base_indent = None
        skip_animations_before_checkpoint = []
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Stop at end_line
                if line_no > end_line:
                    break
                
                # Include all lines up to end_line
                if line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    
                    # Skip animations before our restore point
                    # by converting them to comments
                    if self.current_animation_index >= 0 and any(
                        dedented.lstrip().startswith(cmd) for cmd in ['self.play(', 'self.wait(']
                    ):
                        # Check if this is before our restore point
                        for j, checkpoint in enumerate(self.animation_checkpoints):
                            if checkpoint[1] == line_no and j <= self.current_animation_index:
                                # This animation already happened, skip it
                                dedented = f"# Skipped (already executed): {dedented.strip()}\n"
                                break
                    
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _play_through_next_animation(self):
        """
        Execute code from the updated file until one animation completes.
        Returns True if an animation was played, False if no more animations.
        """
        if not hasattr(self, '_updated_content') or not self._updated_content:
            return False
        
        # Get the line number after which to start executing
        if self.animation_checkpoints:
            start_after_line = self.animation_checkpoints[-1][1]
            stored_locals = self.animation_checkpoints[-1][3]
            current_checkpoint_index = len(self.animation_checkpoints) - 1
        else:
            start_after_line = 0
            stored_locals = {}
            current_checkpoint_index = -1
        
        print(f"[PLAY_NEXT DEBUG] Last checkpoint line: {start_after_line}")
        
        # Always extract and execute code from the updated file
        # We should NOT replay existing checkpoints - we need fresh execution
        # Extract code after the last checkpoint
        code_to_execute = self._extract_code_after_line(start_after_line, self._updated_content)
        
        if not code_to_execute.strip():
            print("[PLAY_NEXT DEBUG] No code to execute")
            self._updated_content = None  # Clear since we're done
            return False
        
        # Find the actual first line number in the extracted code
        # by looking at what line the extracted code starts from in the original file
        first_line_in_extract = None
        for i, line in enumerate(self._updated_content):
            if i + 1 > start_after_line and line.strip():
                # Found first non-empty line after checkpoint
                first_line_in_extract = i + 1
                break
        
        print(f"[PLAY_NEXT DEBUG] First line in extracted code should be: {first_line_in_extract}")
        print(f"[PLAY_NEXT DEBUG] Extracted code preview: {code_to_execute.strip()[:100]}...")
        
        # Add blank lines to preserve original line numbers
        # We need to pad so the first line of code matches its original line number
        if first_line_in_extract:
            padding = '\n' * (first_line_in_extract - 1)
            code_to_execute = padding + code_to_execute
            print(f"[PLAY_NEXT DEBUG] Added {first_line_in_extract - 1} blank lines for padding")
        
        # Set flags to execute only one animation
        self._stop_after_one_animation = True
        self._one_animation_executed = False
        
        try:
            # Create namespace with stored locals
            namespace = {'self': self}
            exec("from maniml import *", namespace)
            
            # Add all stored locals to namespace
            if stored_locals:
                namespace.update(stored_locals)
            
            # Execute the code
            exec(code_to_execute, namespace)
            
            # Return whether we executed an animation
            return self._one_animation_executed
            
        except Exception as e:
            print(f"Error executing next animation: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Clean up flags
            if hasattr(self, '_stop_after_one_animation'):
                delattr(self, '_stop_after_one_animation')
            if hasattr(self, '_one_animation_executed'):
                delattr(self, '_one_animation_executed')
    
    
    
    
    def jump_to_animation(self, index):
        """Jump instantly to a specific animation checkpoint."""
        if index < 0 or index >= len(self.animation_checkpoints):
            print(f"Invalid index. Available checkpoints: 0-{len(self.animation_checkpoints)-1}")
            return
            
        checkpoint = self.animation_checkpoints[index]
        print(f"Jumping to animation #{index + 1}")
        
        # Restore the state
        self.restore_state(checkpoint[2])
        self.current_animation_index = index
        
        # Update frame
        self.update_frame(force_draw=True)
    
    def list_checkpoints(self):
        """List all available animation checkpoints."""
        print(f"\nAvailable checkpoints ({len(self.animation_checkpoints)} total):")
        for i, checkpoint in enumerate(self.animation_checkpoints):
            idx, line_no = checkpoint[0], checkpoint[1]
            anim_info = ""
            if len(checkpoint) > 4 and checkpoint[4]:
                # Show animation info
                anim_info_data = checkpoint[4]
                if isinstance(anim_info_data, dict) and anim_info_data.get('type') == 'play':
                    anims = anim_info_data.get('animations', [])
                    anim_info = f" ({len(anims)} animation{'s' if len(anims) > 1 else ''})"
            print(f"  {i}: Animation at line {line_no}{anim_info}")
        print(f"\nUse jump_to(index) to jump to any checkpoint.")
    
    def play(self, *animations, **kwargs):
        """Play animations with checkpoint support.
        
        Checkpoint structure: (index, line_no, state, caller_locals, animation_info)
        - index: Animation index
        - line_no: Line number where play() was called
        - state: SceneState object with mobject copies
        - caller_locals: Dict of local variables (deepcopied when possible)
        - animation_info: Dict with animation details for replay
        """
        # Skip animations if we're in skip mode OR if we're doing animation counting
        should_skip = False
        
        # Check if we're in skip mode
        if hasattr(self, '_skip_animations') and self._skip_animations:
            should_skip = True
        
        # Check if we're doing animation counting and have played enough
        elif hasattr(self, '_animations_to_play') and hasattr(self, '_animations_played'):
            if self._animations_played >= self._animations_to_play:
                should_skip = True
            else:
                # Count this animation
                self._animations_played += 1
        
        if should_skip:
            # Still need to add mobjects to the scene
            from maniml.manimgl_core.animation.animation import prepare_animation
            animations_list = []
            for proto in animations:
                anim = prepare_animation(proto)
                animations_list.append(anim)
            
            # Add mobjects to scene (mimicking begin_animations behavior)
            all_mobjects = set(self.get_mobject_family_members())
            for animation in animations_list:
                animation.begin()
                if animation.mobject not in all_mobjects:
                    self.add(animation.mobject)
                    all_mobjects = all_mobjects.union(animation.mobject.get_family())
            
            return animations[0] if animations else None
        
        is_navigating = hasattr(self, '_navigating_animations') and self._navigating_animations
        
        # If this is the very first animation, print navigation tip
        if self.current_animation_index == -1 and not is_navigating:
            print("\n[Navigation] Use arrow keys to control animations:")
            print("  → Play next animation")
            print("  ↓ Jump to next animation")
            print("  ← Jump to previous animation")
            print("  ↑ Jump to previous animation")
        
        # Capture the animation info BEFORE playing
        if not is_navigating:
            # Store the local variables from the calling frame
            # DON'T copy mobjects here - we want to maintain references to the originals
            # The scene state will handle copying for restoration
            frame = inspect.currentframe().f_back
            caller_locals = {}
            for name, obj in frame.f_locals.items():
                if not name.startswith('_') and name != 'self':
                    caller_locals[name] = obj
            
            # Convert any _AnimationBuilder objects to actual animations
            from maniml.manimgl_core.mobject.mobject import _AnimationBuilder
            built_animations = []
            
            for anim in animations:
                if isinstance(anim, _AnimationBuilder):
                    # Build the actual animation from the builder
                    anim = anim.build()
                built_animations.append(anim)
            
            # Replace animations with built ones for actual playback
            animations = built_animations
            
            # Store basic animation info for debugging
            animation_info = {
                'type': 'play',
                'num_animations': len(animations),
            }
        
        # Capture start state BEFORE playing animation
        if not is_navigating:
            start_state = self.get_state()
            
            # Get the actual line number from the calling frame
            frame = inspect.currentframe().f_back
            line_no = frame.f_lineno
            
            # Try to get the real line number from IPython's context
            # IPython stores the original line number mapping
            if hasattr(self, '_current_line_in_file'):
                line_no = self._current_line_in_file
            
            # For multi-line play() calls, we need to find where the statement ends
            # We'll store the start line and use a heuristic to find the end
            play_start_line = line_no
        
        # Always play the animation normally
        result = super().play(*animations, **kwargs)
        
        # Only save checkpoints if we're NOT navigating with arrow keys
        if not is_navigating:
            # Get the line number AFTER play completes
            # We need to look at the calling frame to get the actual line in the user's code
            frame = inspect.currentframe()
            user_frame = None
            
            # Walk up the stack to find the frame in the user's file
            while frame:
                filename = frame.f_code.co_filename
                if self._scene_filepath and filename == self._scene_filepath:
                    user_frame = frame
                    break
                frame = frame.f_back
            
            if user_frame:
                line_no_after = user_frame.f_lineno
            else:
                # Fallback
                line_no_after = line_no
            
            # Debug: Show which line we're recording for this checkpoint
            if hasattr(self, '_current_line_in_file'):
                print(f"[Checkpoint {self.current_checkpoint + 1}] Animation at line {self._current_line_in_file}")
            
            # Always create a new checkpoint when playing forward
            # Never replay existing checkpoints
            self.current_animation_index += 1
            self.current_checkpoint += 1
            end_state = self.get_state()
            
            # Store in new system with both start and end states
            self.checkpoints.append((
                self.current_checkpoint,
                line_no_after,  # Store line number after play completes
                start_state,    # State before animation
                end_state,      # State after animation
                caller_locals,
                animation_info
            ))
            
            # Also store in legacy system for compatibility
            self.animation_checkpoints.append((
                self.current_animation_index, 
                line_no_after,  # Store line number after play completes
                end_state,      # Legacy system only stores end state
                caller_locals,
                animation_info if animation_info else None
            ))
            
            # Keep only last 50 checkpoints to avoid memory issues
            if len(self.checkpoints) > 50:
                self.checkpoints.pop(0)
                self.animation_checkpoints.pop(0)
                # Adjust indices
                self.current_checkpoint = min(self.current_checkpoint, len(self.checkpoints) - 1)
                self.current_animation_index = min(self.current_animation_index, len(self.animation_checkpoints) - 1)
        
        return result
    
    def wait(self, duration=1.0, stop_condition=None, frozen_frame=None):
        """Wait without creating checkpoints."""
        # Check if we should stop after one animation (hot reload)
        if hasattr(self, '_stop_after_one_animation') and self._stop_after_one_animation:
            if hasattr(self, '_one_animation_executed') and self._one_animation_executed:
                # Already executed one animation, skip the rest
                return
        
        # Just execute the wait normally - no checkpoint creation
        result = super().wait(duration, stop_condition, frozen_frame)
        
        return result
    
    
    def _extract_animation_code(self, lines, start_line, end_line):
        """Extract code between two line numbers from the construct method."""
        code_lines = []
        in_construct = False
        base_indent = None
        
        # First pass: collect the basic lines
        for i, line in enumerate(lines):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct and start_line < line_no <= end_line:
                if line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    if base_indent is not None:
                        dedented = line[base_indent + 4:]  # +4 for method body indent
                        
                        # Check if this line starts a new statement that would create a checkpoint
                        # If so, don't include it - we only want one checkpoint's worth of code
                        if code_lines and dedented.lstrip().startswith(('self.play(', 'self.wait(')):
                            break
                            
                        code_lines.append(dedented)
                    
                    # If this is the first line and it starts with indentation or is a continuation,
                    # we need to look back for the start of the statement
                    if len(code_lines) == 1 and (dedented.startswith('    ') or not dedented.lstrip().startswith(('self.', 'print', '#', 'if', 'for', 'while', 'def', 'class'))):
                        # Look back for the actual start of the statement
                        for j in range(start_line - 1, max(0, start_line - 10), -1):
                            prev_line = lines[j]
                            if prev_line.strip() and not prev_line.strip().startswith('#'):
                                prev_dedented = prev_line[base_indent + 4:] if base_indent is not None else prev_line
                                if prev_dedented.lstrip().startswith(('self.play(', 'self.wait(', 'self.add(', 'print(')):
                                    # Found the start, prepend it
                                    code_lines.insert(0, prev_dedented)
                                    break
        
        # Check if we have incomplete code (unclosed parentheses, brackets, etc.)
        code_str = ''.join(code_lines)
        if code_str.strip():
            # Count opening and closing parentheses/brackets
            open_parens = code_str.count('(') - code_str.count(')')
            open_brackets = code_str.count('[') - code_str.count(']')
            open_braces = code_str.count('{') - code_str.count('}')
            
            # If we have unclosed delimiters, continue reading until they're closed
            if open_parens > 0 or open_brackets > 0 or open_braces > 0:
                for i in range(end_line, min(end_line + 20, len(lines))):  # Look ahead up to 20 lines
                    if i < len(lines):
                        line = lines[i]
                        if line.strip() and 'interactive_embed' not in line:
                            if base_indent is not None:
                                dedented = line[base_indent + 4:]
                                code_lines.append(dedented)
                                code_str = ''.join(code_lines)
                                
                                # Check if we've closed all delimiters
                                open_parens = code_str.count('(') - code_str.count(')')
                                open_brackets = code_str.count('[') - code_str.count(']')
                                open_braces = code_str.count('{') - code_str.count('}')
                                
                                if open_parens <= 0 and open_brackets <= 0 and open_braces <= 0:
                                    break
        
        return ''.join(code_lines)
    
    
    
    
    def run_next_animation(self, current_checkpoint):
        """
        Execute code from file starting after current checkpoint.
        Blocks key interaction during execution.
        Comments out all code up to and including checkpoint line.
        Exits after playing one animation and updates checkpoint.
        """
        # Block key interaction
        self._processing_key = True
        
        try:
            # Get the file content
            if not hasattr(self, '_scene_filepath') or not self._scene_filepath:
                print("No scene file path available")
                return False
                
            # Use updated content if available (from file change), otherwise current file
            if hasattr(self, '_updated_content') and self._updated_content:
                content = self._updated_content
            else:
                with open(self._scene_filepath, 'r') as f:
                    content = f.readlines()
            
            # Determine the line to start after
            if current_checkpoint >= 0 and current_checkpoint < len(self.animation_checkpoints):
                checkpoint = self.animation_checkpoints[current_checkpoint]
                start_after_line = checkpoint[1]  # line_number from checkpoint
            else:
                start_after_line = 0
            
            
            # Extract code with commenting
            code_to_execute = self._extract_code_with_comments(content, start_after_line)
            
            
            # Check if we have any executable code after the comments
            # Split by lines and check if any non-comment line exists
            has_executable_code = False
            for line in code_to_execute.split('\n'):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    has_executable_code = True
                    break
            
            if not has_executable_code:
                print("Already at last animation")
                return False
            
            # Set flags to execute only one animation
            # Don't reset _one_animation_executed here - it should be managed by navigation
            
            # Create namespace
            namespace = {'self': self}
            exec("from maniml import *", namespace)
            
            # Add stored locals from current checkpoint if available
            # BUT skip this if we're in edit mode to avoid stale mobject references
            if not hasattr(self, '_in_edit_mode') or not self._in_edit_mode:
                if current_checkpoint >= 0 and current_checkpoint < len(self.animation_checkpoints):
                    checkpoint = self.animation_checkpoints[current_checkpoint]
                    if len(checkpoint) > 3:
                        stored_locals = checkpoint[3]
                        for name, obj in stored_locals.items():
                            namespace[name] = obj
            else:
                # In edit mode, we need to execute code up to the checkpoint to define variables
                # but WITHOUT playing animations
                if current_checkpoint >= 0 and current_checkpoint < len(self.animation_checkpoints):
                    checkpoint = self.animation_checkpoints[current_checkpoint]
                    checkpoint_line = checkpoint[1]
                    
                    # Extract and execute code up to the checkpoint line without animations
                    setup_code = self._extract_code_up_to_line(content, checkpoint_line)
                    if setup_code:
                        # Temporarily disable animations
                        self._skip_animations = True
                        try:
                            exec(compile(setup_code, self._scene_filepath, 'exec'), namespace)
                        finally:
                            self._skip_animations = False
            
            # Execute the code
            # We need to compile with the correct filename and starting line
            # to get accurate line numbers in stack traces
            compiled = compile(code_to_execute, self._scene_filepath, 'exec')
            
            # Add a line offset to the namespace so checkpoints know the real line numbers
            namespace['__line_offset__'] = start_after_line
            
            exec(compiled, namespace)
            
            # Check if we executed an animation
            if self._one_animation_executed:
                # Animation was executed and checkpoint created
                return True
            else:
                print("No animation found in remaining code")
                return False
                
        except Exception as e:
            print(f"Error in run_next_animation: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Clean up flags
            self._processing_key = False
            # Don't delete _stop_after_one_animation - we want this behavior permanently
            # Reset _one_animation_executed for next navigation
            if hasattr(self, '_one_animation_executed'):
                self._one_animation_executed = False
    
    
    def jump_to_next_animation(self, current_checkpoint):
        """
        Jump to the next animation checkpoint without playing.
        Updates current_checkpoint and restores state.
        """
        next_index = current_checkpoint + 1
        
        if next_index >= len(self.animation_checkpoints):
            print("Already at last animation")
            return current_checkpoint
        
        checkpoint = self.animation_checkpoints[next_index]
        print(f"Jump to animation {next_index + 1}/{len(self.animation_checkpoints)}")
        self.restore_state(checkpoint[2])
        self.current_animation_index = next_index
        self.update_frame(dt=0, force_draw=True)
        
        return next_index
    
    def jump_to_previous_animation(self, current_checkpoint):
        """
        Jump to the previous animation checkpoint without playing.
        Updates current_checkpoint and restores state.
        """
        prev_index = current_checkpoint - 1
        
        if prev_index < 0:
            print("Already at first animation")
            return current_checkpoint
        
        checkpoint = self.animation_checkpoints[prev_index]
        print(f"Jump to animation {prev_index + 1}/{len(self.animation_checkpoints)}")
        
        # Set flag if we're jumping to checkpoint 0
        if prev_index == 0:
            self._restoring_to_zero = True
        
        self.restore_state(checkpoint[2])
        self.current_animation_index = prev_index
        
        # Clear the flag
        if hasattr(self, '_restoring_to_zero'):
            delattr(self, '_restoring_to_zero')
        
        self.update_frame(dt=0, force_draw=True)
        
        return prev_index
    
    def _extract_code_up_to_line(self, content, up_to_line):
        """
        Extract code from construct method up to the specified line.
        Used in edit mode to define variables without playing animations.
        """
        in_construct = False
        code_lines = []
        base_indent = None
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Stop at the specified line
                if line_no > up_to_line:
                    break
                
                # Include this line
                if line.strip() and 'interactive_embed' not in line:
                    # Remove the base indentation
                    dedented = line[base_indent + 4:]  # +4 for method body indent
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_with_animation_count(self, content, animations_to_comment):
        """
        Extract code from construct method, commenting out the first N animations.
        This avoids the line number tracking issues with exec/IPython.
        """
        in_construct = False
        code_lines = []
        base_indent = None
        animations_seen = 0
        
        for i, line in enumerate(content):
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Include all lines, even empty ones, to preserve structure
                if 'interactive_embed' not in line:
                    # Remove the base indentation
                    if len(line) > base_indent + 4:
                        dedented = line[base_indent + 4:]  # +4 for method body indent
                    else:
                        dedented = line[base_indent:] if len(line) > base_indent else line
                    
                    # Check if this line contains self.play(
                    if 'self.play(' in dedented and not dedented.strip().startswith('#'):
                        if animations_seen < animations_to_comment:
                            # Comment out this animation
                            leading_spaces = len(dedented) - len(dedented.lstrip())
                            comment_prefix = ' ' * leading_spaces + '# Already executed: '
                            dedented = comment_prefix + dedented.strip() + '\n'
                            animations_seen += 1
                    
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def _extract_code_with_comments(self, content, comment_up_to_line):
        """
        Extract code from construct method, commenting out lines up to comment_up_to_line.
        This prevents re-execution of animations that have already been played.
        """
        in_construct = False
        code_lines = []
        base_indent = None
        actual_line_count = 0  # Track line numbers in extracted code
        
        for i, line in enumerate(content):
            line_no = i + 1
            
            if 'def construct(self):' in line:
                in_construct = True
                base_indent = len(line) - len(line.lstrip())
                continue
            
            if in_construct:
                # Check if we've exited construct
                if line.strip() and not line[base_indent:].startswith(' '):
                    break
                
                # Include all lines, even empty ones, to preserve structure
                if 'interactive_embed' not in line:
                    actual_line_count += 1
                    
                    # Remove the base indentation
                    if len(line) > base_indent + 4:
                        dedented = line[base_indent + 4:]  # +4 for method body indent
                    else:
                        dedented = line[base_indent:] if len(line) > base_indent else line
                    
                    # Comment out lines up to and including comment_up_to_line
                    # Special case: if comment_up_to_line is -1, don't comment anything
                    if comment_up_to_line >= 0 and line_no <= comment_up_to_line and line.strip():
                        # Keep original indentation when commenting
                        # Find the amount of leading whitespace after dedenting
                        leading_spaces = len(dedented) - len(dedented.lstrip())
                        comment_prefix = ' ' * leading_spaces + '# Already executed: '
                        dedented = comment_prefix + dedented.strip() + '\n'
                    
                    # Add a special marker for the line we start from
                    if line_no == comment_up_to_line + 1:
                        code_lines.append(f"__line_offset__ = {line_no - actual_line_count}  # Line offset for checkpoints\n")
                    
                    code_lines.append(dedented)
        
        return ''.join(code_lines)
    
    def tear_down(self):
        """Clean up file watcher on scene end."""
        if hasattr(self, '_file_watcher') and self._file_watcher:
            self._file_watcher.stop()
        super().tear_down()
    
    # InteractiveScene methods (ported from ManimGL)
    
    def get_selection_rectangle(self):
        rect = Rectangle(
            stroke_color=self.selection_rectangle_stroke_color,
            stroke_width=self.selection_rectangle_stroke_width,
        )
        rect.fix_in_frame()
        rect.fixed_corner = ORIGIN
        rect.add_updater(self.update_selection_rectangle)
        return rect

    def update_selection_rectangle(self, rect):
        p1 = rect.fixed_corner
        p2 = self.frame.to_fixed_frame_point(self.mouse_point.get_center())
        rect.set_points_as_corners([
            p1, np.array([p2[0], p1[1], 0]),
            p2, np.array([p1[0], p2[1], 0]),
            p1,
        ])
        return rect

    def get_selection_highlight(self):
        result = Group()
        result.tracked_mobjects = []
        result.add_updater(self.update_selection_highlight)
        return result

    def update_selection_highlight(self, highlight):
        if set(highlight.tracked_mobjects) == set(self.selection):
            return

        # Otherwise, refresh contents of highlight
        highlight.tracked_mobjects = list(self.selection)
        highlight.set_submobjects([
            self.get_highlight(mob)
            for mob in self.selection
        ])
        try:
            index = min((
                i for i, mob in enumerate(self.mobjects)
                for sm in self.selection
                if sm in mob.get_family()
            ))
            self.mobjects.remove(highlight)
            self.mobjects.insert(index - 1, highlight)
        except ValueError:
            pass

    def get_crosshair(self):
        lines = VMobject().replicate(2)
        lines[0].set_points([LEFT, ORIGIN, RIGHT])
        lines[1].set_points([UP, ORIGIN, DOWN])
        crosshair = VGroup(*lines)

        crosshair.set_width(self.crosshair_width)
        crosshair.set_style(**self.crosshair_style)
        crosshair.set_animating_status(True)
        crosshair.fix_in_frame()
        return crosshair

    def get_color_palette(self):
        palette = VGroup(*(
            Square(fill_color=color, fill_opacity=1, side_length=1)
            for color in self.palette_colors
        ))
        palette.set_stroke(width=0)
        palette.arrange(RIGHT, buff=0.5)
        palette.set_width(FRAME_WIDTH - 0.5)
        palette.to_edge(DOWN, buff=SMALL_BUFF)
        palette.fix_in_frame()
        return palette

    def get_information_label(self):
        loc_label = VGroup(*(
            DecimalNumber(**self.cursor_location_config)
            for n in range(3)
        ))

        def update_coords(loc_label):
            for mob, coord in zip(loc_label, self.mouse_point.get_location()):
                mob.set_value(coord)
            loc_label.arrange(RIGHT, buff=loc_label.get_height())
            loc_label.to_corner(DR, buff=SMALL_BUFF)
            loc_label.fix_in_frame()
            return loc_label

        loc_label.add_updater(update_coords)

        time_label = DecimalNumber(0, **self.time_label_config)
        time_label.to_corner(DL, buff=SMALL_BUFF)
        time_label.fix_in_frame()
        time_label.add_updater(lambda m, dt: m.increment_value(dt))

        return VGroup(loc_label, time_label)

    # Selection management

    def toggle_selection_mode(self):
        self.select_top_level_mobs = not self.select_top_level_mobs
        self.refresh_selection_scope()
        self.regenerate_selection_search_set()

    def get_selection_search_set(self):
        return self.selection_search_set

    def regenerate_selection_search_set(self):
        selectable = list(filter(
            lambda m: m not in self.unselectables,
            self.mobjects
        ))
        if self.select_top_level_mobs:
            self.selection_search_set = selectable
        else:
            self.selection_search_set = [
                submob
                for mob in selectable
                for submob in mob.family_members_with_points()
            ]

    def refresh_selection_scope(self):
        curr = list(self.selection)
        if self.select_top_level_mobs:
            self.selection.set_submobjects([
                mob
                for mob in self.mobjects
                if any(sm in mob.get_family() for sm in curr)
            ])
            self.selection.refresh_bounding_box(recurse_down=True)
        else:
            self.selection.set_submobjects(
                extract_mobject_family_members(
                    curr, exclude_pointless=True,
                )
            )

    def get_corner_dots(self, mobject):
        dots = DotCloud(**self.corner_dot_config)
        radius = float(self.corner_dot_config["radius"])
        if mobject.get_depth() < 1e-2:
            vects = [DL, UL, UR, DR]
        else:
            vects = np.array(list(it.product(*3 * [[-1, 1]])))
        dots.add_updater(lambda d: d.set_points([
            mobject.get_corner(v) + v * radius
            for v in vects
        ]))
        return dots

    def get_highlight(self, mobject):
        if isinstance(mobject, VMobject) and mobject.has_points() and not self.select_top_level_mobs:
            length = max([mobject.get_height(), mobject.get_width()])
            result = VHighlight(
                mobject,
                max_stroke_addition=min([50 * length, 10]),
            )
            result.add_updater(lambda m: m.replace(mobject, stretch=True))
            return result
        elif isinstance(mobject, DotCloud):
            return Mobject()
        else:
            return self.get_corner_dots(mobject)

    def add_to_selection(self, *mobjects):
        mobs = list(filter(
            lambda m: m not in self.unselectables and m not in self.selection,
            mobjects
        ))
        if len(mobs) == 0:
            return
        self.selection.add(*mobs)
        for mob in mobs:
            mob.set_animating_status(True)

    def toggle_from_selection(self, *mobjects):
        for mob in mobjects:
            if mob in self.selection:
                self.selection.remove(mob)
                mob.set_animating_status(False)
                mob.refresh_bounding_box()
            else:
                self.add_to_selection(mob)

    def clear_selection(self):
        for mob in self.selection:
            mob.set_animating_status(False)
            mob.refresh_bounding_box()
        self.selection.set_submobjects([])

    def disable_interaction(self, *mobjects):
        for mob in mobjects:
            for sm in mob.get_family():
                self.unselectables.append(sm)
        self.regenerate_selection_search_set()

    def enable_interaction(self, *mobjects):
        for mob in mobjects:
            for sm in mob.get_family():
                if sm in self.unselectables:
                    self.unselectables.remove(sm)

    # Keyboard action methods

    def copy_selection(self):
        # Simplified version without IPython
        names = [str(id(mob)) for mob in self.selection]
        pyperclip.copy(", ".join(names))

    def paste_selection(self):
        clipboard_str = pyperclip.paste()
        # Try pasting a mobject
        try:
            ids = map(int, clipboard_str.split(","))
            mobs = map(self.id_to_mobject, ids)
            mob_copies = [m.copy() for m in mobs if m is not None]
            self.clear_selection()
            self.play(*(
                FadeIn(mc, run_time=0.5, scale=1.5)
                for mc in mob_copies
            ))
            self.add_to_selection(*mob_copies)
            return
        except ValueError:
            pass
        # Otherwise, treat as tex or text
        if set("\\^=+").intersection(clipboard_str):  # Proxy to text for LaTeX
            try:
                new_mob = Tex(clipboard_str)
            except LatexError:
                return
        else:
            new_mob = Text(clipboard_str)
        self.clear_selection()
        self.add(new_mob)
        self.add_to_selection(new_mob)

    def delete_selection(self):
        self.remove(*self.selection)
        self.clear_selection()

    def enable_selection(self):
        self.is_selecting = True
        self.add(self.selection_rectangle)
        self.selection_rectangle.fixed_corner = self.frame.to_fixed_frame_point(
            self.mouse_point.get_center()
        )

    def gather_new_selection(self):
        self.is_selecting = False
        if self.selection_rectangle in self.mobjects:
            self.remove(self.selection_rectangle)
            additions = []
            for mob in reversed(self.get_selection_search_set()):
                if self.selection_rectangle.is_touching(mob):
                    additions.append(mob)
                    if self.selection_rectangle.get_arc_length() < 1e-2:
                        break
            self.toggle_from_selection(*additions)

    def prepare_grab(self):
        mp = self.mouse_point.get_center()
        self.mouse_to_selection = mp - self.selection.get_center()
        self.is_grabbing = True

    def prepare_resizing(self, about_corner=False):
        center = self.selection.get_center()
        mp = self.mouse_point.get_center()
        if about_corner:
            self.scale_about_point = self.selection.get_corner(center - mp)
        else:
            self.scale_about_point = center
        self.scale_ref_vect = mp - self.scale_about_point
        self.scale_ref_width = self.selection.get_width()
        self.scale_ref_height = self.selection.get_height()

    def toggle_color_palette(self):
        if len(self.selection) == 0:
            return
        if self.color_palette not in self.mobjects:
            self.save_state()
            self.add(self.color_palette)
        else:
            self.remove(self.color_palette)

    def display_information(self, show=True):
        if show:
            self.add(self.information_label)
        else:
            self.remove(self.information_label)

    def group_selection(self):
        group = self.get_group(*self.selection)
        self.add(group)
        self.clear_selection()
        self.add_to_selection(group)

    def ungroup_selection(self):
        pieces = []
        for mob in list(self.selection):
            self.remove(mob)
            pieces.extend(list(mob))
        self.clear_selection()
        self.add(*pieces)
        self.add_to_selection(*pieces)

    def nudge_selection(self, vect, large=False):
        nudge = self.selection_nudge_size
        if large:
            nudge *= 10
        self.selection.shift(nudge * vect)

    # Mouse event handlers

    def handle_grabbing(self, point):
        diff = point - self.mouse_to_selection
        if self.window.is_key_pressed(ord(GRAB_KEY)):
            self.selection.move_to(diff)
        elif self.window.is_key_pressed(ord(X_GRAB_KEY)):
            self.selection.set_x(diff[0])
        elif self.window.is_key_pressed(ord(Y_GRAB_KEY)):
            self.selection.set_y(diff[1])

    def handle_resizing(self, point):
        if not hasattr(self, "scale_about_point") or self.scale_about_point is None:
            return
        vect = point - self.scale_about_point
        if self.window.is_key_pressed(PygletWindowKeys.LCTRL):
            for i in (0, 1):
                scalar = vect[i] / self.scale_ref_vect[i]
                self.selection.rescale_to_fit(
                    scalar * [self.scale_ref_width, self.scale_ref_height][i],
                    dim=i,
                    about_point=self.scale_about_point,
                    stretch=True,
                )
        else:
            scalar = get_norm(vect) / get_norm(self.scale_ref_vect)
            self.selection.set_width(
                scalar * self.scale_ref_width,
                about_point=self.scale_about_point
            )

    def handle_sweeping_selection(self, point):
        mob = self.point_to_mobject(
            point,
            search_set=self.get_selection_search_set(),
            buff=SMALL_BUFF
        )
        if mob is not None:
            self.add_to_selection(mob)

    def choose_color(self, point):
        # Search through all mobject on the screen, not just the palette
        to_search = [
            sm
            for mobject in self.mobjects
            for sm in mobject.family_members_with_points()
            if mobject not in self.unselectables
        ]
        mob = self.point_to_mobject(point, to_search)
        if mob is not None:
            self.selection.set_color(mob.get_color())
        self.remove(self.color_palette)

    # Override add/remove to maintain selection search set
    
    def add(self, *mobjects):
        super().add(*mobjects)
        self.regenerate_selection_search_set()
        return self

    def remove(self, *mobjects):
        super().remove(*mobjects)
        self.regenerate_selection_search_set()
        return self

    def remove_all_except(self, *mobjects_to_keep):
        super().remove_all_except(*mobjects_to_keep)
        self.regenerate_selection_search_set()

    # Override get_state to ignore interactive elements
    
    def get_state(self):
        return GLSceneState(self, ignore=[
            self.selection_highlight,
            self.selection_rectangle,
            self.crosshair,
        ])

    def restore_state(self, scene_state):
        # Special handling for checkpoint 0 (blank state)
        # When restoring to the initial blank checkpoint, ensure we clear all mobjects
        if self.current_animation_index == 0 or (hasattr(self, '_restoring_to_zero') and self._restoring_to_zero):
            # Clear all mobjects except unselectables
            mobjects_to_remove = [m for m in self.mobjects if m not in self.unselectables]
            for mob in mobjects_to_remove:
                self.remove(mob)
        
        super().restore_state(scene_state)
        if hasattr(self, 'selection_highlight') and self.selection_highlight:
            self.mobjects.insert(0, self.selection_highlight)

    # Copy positioning helpers
    
    def copy_frame_positioning(self):
        frame = self.frame
        center = frame.get_center()
        height = frame.get_height()
        angles = frame.get_euler_angles()

        call = f"reorient("
        theta, phi, gamma = (angles / DEG).astype(int)
        call += f"{theta}, {phi}, {gamma}"
        if any(center != 0):
            call += f", {tuple(np.round(center, 2))}"
        if height != FRAME_HEIGHT:
            call += ", {:.2f}".format(height)
        call += ")"
        pyperclip.copy(call)

    def copy_cursor_position(self):
        pyperclip.copy(str(tuple(self.mouse_point.get_center().round(2))))


class ThreeDScene(GLThreeDScene):
    """CE-compatible ThreeDScene using GL backend."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add CE compatibility methods
        self.renderer = self
        # Disable drag-to-pan by default since we use Cmd/Ctrl + drag
        self.drag_to_pan = False
    
    # Override methods to add CE compatibility
    def add(self, *mobjects):
        """CE-style add method that returns self for chaining."""
        GLThreeDScene.add(self, *mobjects)
        return self
    
    def remove(self, *mobjects):
        """CE-style remove method that returns self for chaining."""
        GLThreeDScene.remove(self, *mobjects)
        return self
    
    def play(self, *animations, **kwargs):
        """CE-style play with multiple animations and lag_ratio support."""
        # Extract CE-specific kwargs
        run_time = kwargs.pop('run_time', None)
        lag_ratio = kwargs.pop('lag_ratio', 0)
        rate_func = kwargs.pop('rate_func', None)
        
        # Handle run_time
        if run_time is not None:
            for anim in animations:
                if hasattr(anim, 'run_time'):
                    anim.run_time = run_time
        
        # Handle rate_func
        if rate_func is not None:
            for anim in animations:
                if hasattr(anim, 'rate_func'):
                    anim.rate_func = rate_func
        
        # Handle multiple animations
        if len(animations) == 1:
            GLThreeDScene.play(self, animations[0], **kwargs)
        else:
            # Multiple animations
            if lag_ratio > 0:
                from maniml.manimgl_core.animation.composition import LaggedStart
                GLThreeDScene.play(self, LaggedStart(*animations, lag_ratio=lag_ratio), **kwargs)
            else:
                from maniml.manimgl_core.animation.composition import AnimationGroup
                GLThreeDScene.play(self, AnimationGroup(*animations), **kwargs)
    
    def wait(self, duration=None, stop_condition=None, note=None, ignore_presenter_mode=False):
        """CE-style wait method."""
        # Call parent's wait directly
        if duration is None:
            duration = 1.0  # Default wait time
        GLThreeDScene.wait(self, duration, stop_condition, note, ignore_presenter_mode)
    
    def bring_to_front(self, *mobjects):
        """CE-style bring_to_front."""
        GLThreeDScene.bring_to_front(self, *mobjects)
        return self
    
    def bring_to_back(self, *mobjects):
        """CE-style bring_to_back."""
        GLThreeDScene.bring_to_back(self, *mobjects)
        return self
    
    def clear(self):
        """CE-style clear."""
        GLThreeDScene.clear(self)
        return self
    
    # Interactive methods from Scene
    def on_key_press(self, symbol, modifiers):
        """Handle key press with Scene's interactive features."""
        # First call parent's on_key_press
        GLThreeDScene.on_key_press(self, symbol, modifiers)
        # Then add our interactive features if Scene has them
        if hasattr(Scene, 'on_key_press') and hasattr(Scene, 'gather_new_selection'):
            # Call specific interactive methods we need
            pass
    
    def checkpoint_paste(self):
        """Interactive checkpoint paste."""
        if hasattr(Scene, 'checkpoint_paste'):
            return Scene.checkpoint_paste(self)
    
    def clear_checkpoints(self):
        """Clear checkpoints."""
        if hasattr(Scene, 'clear_checkpoints'):
            return Scene.clear_checkpoints(self)
    
    def set_camera_orientation(self, phi=None, theta=None, gamma=None, **kwargs):
        """CE compatibility wrapper for camera orientation."""
        # Convert CE-style angles (in radians) to degrees for reorient
        if phi is not None or theta is not None or gamma is not None:
            # Get current angles if not specified
            current_theta = self.frame.get_theta() if theta is None else theta
            current_phi = self.frame.get_phi() if phi is None else phi
            current_gamma = self.frame.get_gamma() if gamma is None else gamma
            
            # Convert radians to degrees
            theta_deg = current_theta * 180 / PI
            phi_deg = current_phi * 180 / PI
            gamma_deg = current_gamma * 180 / PI
            
            # Use reorient which expects degrees
            self.frame.reorient(theta_deg, phi_deg, gamma_deg)
        
        return self
    
    def move_camera(self, phi=None, theta=None, gamma=None, **kwargs):
        """CE compatibility wrapper for animating camera movement."""
        # For animated camera movements
        animations = []
        
        if theta is not None:
            animations.append(self.frame.animate.set_theta(theta))
        if phi is not None:
            animations.append(self.frame.animate.set_phi(phi))
        if gamma is not None:
            animations.append(self.frame.animate.set_gamma(gamma))
        
        if animations:
            self.play(*animations, **kwargs)
        
        return self


# Alias for CE compatibility
SpecialThreeDScene = ThreeDScene