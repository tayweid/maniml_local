# ManimL Checkpoint System Documentation

## Overview

The checkpoint system in maniml allows users to navigate through animations using arrow keys, creating an interactive debugging and presentation experience. This system captures the state of the scene after each animation and allows replaying animations forward or jumping between states.

## Key Components

### Files Involved

1. **`/maniml/scene/scene.py`** - Main implementation
   - Contains the Scene class that extends GLScene
   - Implements checkpoint creation, storage, and navigation
   - Handles arrow key events

2. **`/maniml/__main__.py`** - Entry point
   - Passes the scene file path to the Scene instance
   - Enables the checkpoint system to access source code

3. **User's scene files** (e.g., `test_simple.py`)
   - Standard Manim scenes that automatically get checkpoint support

## Data Structures

### Checkpoint Storage

Each checkpoint is stored as a tuple with 5 elements:

```python
checkpoint = (
    index,           # int: Sequential animation index (0, 1, 2, ...)
    line_no,         # int: Line number where play/wait was called
    state,           # dict: Complete scene state (mobjects, camera, etc.)
    caller_locals,   # dict: Local variables from the calling context
    animation_info   # dict: Information needed to replay the animation
)
```

### Animation Info Dictionary

For `play()` calls:
```python
animation_info = {
    'type': 'play',
    'animations': animations,  # tuple of Animation objects
    'kwargs': kwargs,          # dict of keyword arguments
    'line_no': line_no        # int: source line number
}
```

For `wait()` calls:
```python
animation_info = {
    'type': 'wait',
    'duration': duration,              # float
    'stop_condition': stop_condition,  # callable or None
    'frozen_frame': frozen_frame,      # bool or None
    'line_no': line_no                # int
}
```

### Scene State

The state dictionary (from `get_state()`) contains:
- All mobjects and their properties
- Camera position and settings
- Any other scene-specific state

## Flow of Execution

### 1. Initial Animation Execution

When a scene runs normally:

```python
# User's code
self.play(Create(circle))  # Line 10
```

1. `play()` method is called
2. Before playing: Captures animation info and locals
3. Executes the animation via `super().play()`
4. After playing: Creates checkpoint with:
   - Current state (after animation)
   - Animation info (for replay)
   - Local variables

### 2. Checkpoint Creation

```python
# In scene.py play() method
if not is_navigating:
    # Capture info BEFORE playing
    animation_info = {
        'type': 'play',
        'animations': animations,
        'kwargs': kwargs,
        'line_no': line_no
    }
    
    # Play animation
    result = super().play(*animations, **kwargs)
    
    # Save checkpoint AFTER animation completes
    self.current_animation_index += 1
    state = self.get_state()
    self.animation_checkpoints.append((
        self.current_animation_index,
        line_no,
        state,
        caller_locals,
        animation_info
    ))
```

### 3. Arrow Key Navigation

#### UP Arrow - Jump Forward
- Increments `current_animation_index`
- Restores state from that checkpoint
- No animation replay, just state restoration

#### DOWN Arrow - Jump Backward
- Decrements `current_animation_index`
- Restores state from that checkpoint
- No animation replay, just state restoration

#### LEFT Arrow - Reverse
- Decrements `current_animation_index`
- Restores state from previous checkpoint
- Sets `_navigating_animations = True` to prevent new checkpoints
- Currently just jumps (reverse animation not implemented)

#### RIGHT Arrow - Play Forward
- Finds the next checkpoint to play
- **Key insight**: To replay animation N, restore to checkpoint N-1
- Sets `_navigating_animations = True`
- Replays the stored animation using the captured info
- Updates `current_animation_index` after successful replay

## Navigation Logic

### Checkpoint Indexing

Consider this sequence:
```python
1. self.play(Create(circle))      # Creates checkpoint 0 (after Create)
2. self.play(circle.animate.shift(RIGHT))  # Creates checkpoint 1 (after shift)
3. self.play(circle.animate.scale(0.5))    # Creates checkpoint 2 (after scale)
```

**Important**: Checkpoints store state AFTER animations complete.

To replay the scale animation:
1. Restore to checkpoint 1 (circle shifted but not scaled)
2. Execute the scale animation
3. Result: checkpoint 2 state

### The `_navigating_animations` Flag

This flag prevents checkpoint creation during navigation:
- Set to `True` when replaying animations
- Prevents duplicate checkpoints
- Ensures checkpoint list remains consistent

## Example Walkthrough

```python
class ExampleScene(Scene):
    def construct(self):
        # Creates checkpoint 0
        circle = Circle()
        self.play(Create(circle))
        
        # Creates checkpoint 1
        self.play(circle.animate.shift(RIGHT * 2))
        
        # Creates checkpoint 2
        self.play(circle.animate.scale(0.5))
        
        self.wait(10)  # Time for navigation
```

Navigation sequence:
1. Press LEFT twice → at checkpoint 0
2. Press RIGHT → restores to checkpoint 0, plays shift animation
3. Press RIGHT → restores to checkpoint 1, plays scale animation

## Implementation Details

### State Restoration

The `restore_state()` method (inherited from GLScene):
- Clears current mobjects
- Recreates mobjects from saved state
- Restores camera settings
- Updates the display

### Animation Replay

Instead of parsing source code, the system now:
1. Stores actual Animation objects
2. Stores method parameters
3. Replays by calling `self.play()` with stored objects

This approach is:
- More reliable (no parsing errors)
- Faster (no file I/O during navigation)
- More accurate (exact same animations)

### Memory Management

- Only keeps last 50 checkpoints
- Older checkpoints are removed automatically
- Prevents memory issues in long scenes

## Usage Tips

1. **Navigation works best with discrete animations**
   - Each `play()` or `wait()` creates a checkpoint
   - Continuous animations work but may skip states

2. **Complex animations are preserved**
   - Multi-object animations stored correctly
   - Animation parameters maintained

3. **Local variables available**
   - Checkpoint stores local namespace
   - Useful for debugging variable states

4. **Performance considerations**
   - State saving has overhead
   - Navigation is disabled during file watching/auto-reload

## Future Enhancements

1. **Reverse animation playback**
   - Currently LEFT arrow just jumps
   - Could implement true reverse playback

2. **Checkpoint labels**
   - Add descriptive names to checkpoints
   - Easier navigation in complex scenes

3. **Checkpoint persistence**
   - Save/load checkpoint sequences
   - Share specific animation states

4. **Visual checkpoint indicator**
   - Show current position in timeline
   - Display checkpoint information on screen