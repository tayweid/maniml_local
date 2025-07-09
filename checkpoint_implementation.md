# Checkpoint System Implementation

## Overview
This document describes the implementation of the checkpoint system for maniml_local, which enables navigation through animations using arrow keys with proper state synchronization between animation mobjects and Python objects.

## Architecture

### Core Concepts

1. **Checkpoints**: Saved states at each animation, storing scene state and context
2. **Tight/Slack States**: 
   - Tight: Can execute new code directly (haven't navigated backward)
   - Slack: Must re-execute code up to current point (have navigated backward)
3. **State Management**: Uses ManimGL's SceneState for efficient mobject storage
4. **Code Execution**: Smart extraction and execution of construct method code

### Data Structures

```python
# Main checkpoint list
self.checkpoints = [
    (index, line_number, scene_state, locals_dict, animation_info),
    ...
]

# State tracking
self.current_checkpoint = -1  # Current position
self.tight = True            # Execution state
```

## Function Reference

### Initialization

#### `start()`
Initializes the checkpoint system with a blank screen as checkpoint 0.
- Creates initial checkpoint with empty scene
- Sets up file watching if enabled
- Runs first animation

### Code Execution

#### `run_next_code()`
Executes code after the current checkpoint to create the next animation.
- Extracts code with lines up to current checkpoint commented out
- Executes with stored local variables
- Creates new checkpoint when animation plays

#### `run_exec(code, namespace, animations=True)`
Core execution function that runs Python code.
- Parameters:
  - `code`: Python code string to execute
  - `namespace`: Dictionary of variables for execution context
  - `animations`: If False, suppresses animation execution
- Handles compilation and execution with proper error handling

#### `reexecute()`
Re-runs all code up to current checkpoint without animations.
- Used when in "slack" state to rebuild scene state
- Skips all animations to quickly reach current point
- Sets tight=True after completion

### Code Extraction

#### `comment_out_to_line(line)`
Extracts construct method code with executed lines commented out.
- Comments out all code up to and including the specified line
- Preserves line numbers for accurate debugging
- Handles multi-line statements correctly

#### `code_upto_line(line)`
Extracts construct method code up to a specific line.
- Returns executable code without comments
- Used by reexecute() to rebuild state

#### `get_namespace()`
Creates execution namespace with proper context.
- Includes 'self' reference
- Imports maniml modules
- Adds stored local variables from current checkpoint

### Navigation

#### `play_forward()`
Plays the animation at the next checkpoint.
- Restores to state before the animation
- Uses stored animation info to replay without re-execution
- Remaps mobject references to current scene objects
- Sets tight=False after navigation

#### `jump_to(checkpoint_index)`
Instantly jumps to a checkpoint's final state.
- No animation playback
- Direct state restoration
- Updates display immediately

#### `jump_back()`
Convenience method for jumping to previous checkpoint.
- Used by left and up arrow keys
- Calls jump_to() with previous index

### Arrow Key Handlers

#### `right_arrow()`
Plays next animation forward.
- If next checkpoint exists: calls play_forward()
- If at end: creates new animation
  - Calls reexecute() if slack
  - Calls run_next_code()

#### `down_arrow()`
Jumps to next checkpoint instantly.
- Similar to right_arrow but uses jump_to() instead of play_forward()

#### `left_arrow()` / `up_arrow()`
Jumps to previous checkpoint.
- Calls jump_back()
- Sets tight=False

### File Change Handling

#### `on_edit()`
Handles file changes during auto-reload.
- Finds changed line ranges
- Identifies last unaffected checkpoint
- Restores to safe checkpoint
- Re-executes affected code

### State Management

#### `create_checkpoint(line_no, animation_info=None)`
Creates a new checkpoint at current state.
- Uses SceneState for efficient mobject storage
- Captures local variables
- Stores animation info for replay

#### `restore_checkpoint(checkpoint)`
Restores scene to a checkpoint's state.
- Uses SceneState.restore_scene()
- Updates current_checkpoint index

### Animation Remapping

#### `remap_stored_animations(anim_info)`
Maps stored animation references to current scene mobjects.
- Groups mobjects by type
- Matches by order within type
- Creates fresh animation copies

## Usage Flow

### Initial Run
1. `start()` creates blank checkpoint 0
2. `run_next_code()` executes first animation
3. `play()` creates checkpoint 1
4. Continue until interactive_embed()

### Right Arrow Press
1. Check if next checkpoint exists
2. If yes: `play_forward()` replays animation
3. If no: 
   - Check tight/slack state
   - If slack: `reexecute()` to rebuild state
   - `run_next_code()` to create new animation

### Left Arrow Press
1. `jump_back()` to previous checkpoint
2. Set tight=False (now in slack state)
3. Update display

### File Edit
1. File watcher detects change
2. `on_edit()` finds affected lines
3. Restore to last safe checkpoint
4. Re-execute affected animations

## Integration with ManimGL

### SceneState Usage
- Leverages ManimGL's optimized state storage
- Reuses unchanged mobject copies between checkpoints
- Uses `become()` for state restoration

### Animation Replay
- Stores animation objects at checkpoint creation
- Remaps mobject references during replay
- Preserves animation parameters and timing

## Benefits

1. **Efficient Navigation**: Instant jumping, smart replay
2. **Memory Optimized**: Reuses unchanged mobjects
3. **Accurate Replay**: Preserves exact animation behavior
4. **Developer Friendly**: Clear state model, good debugging
5. **Robust**: Handles edits, errors, and edge cases

## Implementation Notes

- The system maintains compatibility with existing CE API
- File watching runs in a separate thread with flag-based communication
- Line number tracking handles multi-line statements
- Error handling preserves scene state for recovery