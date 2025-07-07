# Auto-Reload Implementation Using IPython's run_cell()

## Overview

We've successfully implemented auto-reload functionality that combines:
1. **ManimGL's checkpoint_paste approach**: Uses `shell.run_cell()` to execute code in IPython's namespace
2. **Our file watching system**: Automatically detects file changes and triggers reload

## Key Implementation Details

### 1. Storing the IPython Shell

When `interactive_embed()` is called, we create ManimGL's `InteractiveSceneEmbed` object and store its shell:

```python
# In interactive_embed()
from manimlib.scene.scene_embed import InteractiveSceneEmbed

# Create the embed object
embed_obj = InteractiveSceneEmbed(self)

# Store the shell for our auto-reload
self._ipython_shell = embed_obj.shell

# Launch the interactive session
embed_obj.launch()
```

### 2. Using run_cell() for Code Execution

When a file change is detected, we use the stored IPython shell to run the updated code:

```python
# In _handle_file_change()
if hasattr(self, '_ipython_shell') and self._ipython_shell:
    try:
        # Run the code using IPython's run_cell - just like checkpoint_paste!
        self._ipython_shell.run_cell(code_to_run)
        print("Code executed successfully!")
    except Exception as e:
        print(f"Error executing updated code: {e}")
```

### 3. Benefits of Using run_cell()

- **Full namespace access**: All imports and variables from the IPython session are available
- **IPython magic commands**: Works with IPython-specific features
- **Same as checkpoint_paste**: Identical execution environment to ManimGL's checkpoint_paste
- **No namespace building needed**: IPython maintains the full context

## How It Works

1. **File Watching**: Background thread detects when the Python file is saved
2. **Change Detection**: Finds which line was modified
3. **Checkpoint Restoration**: Restores scene state to the checkpoint before the change
4. **Code Execution**: Uses `shell.run_cell()` to run only the code after the checkpoint
5. **Scene Update**: The animation updates with the new changes

## Testing

1. Run: `maniml ipython_test.py IPythonTest`
2. When the interactive embed opens, edit the file:
   - Change line 20 from `Square(side_length=2, color=RED` to `Circle(radius=1.5, color=GREEN`
3. Save the file
4. The animation automatically updates!

## Comparison with ManimGL

**ManimGL's checkpoint_paste**:
```python
# Manual process
1. Copy code
2. Run checkpoint_paste()
3. Code executes via shell.run_cell()
```

**Our auto-reload**:
```python
# Automatic process
1. Save file
2. File watcher detects change
3. Code executes via shell.run_cell()
```

Same execution method, but triggered automatically on file save!

## Window Size Configuration

The custom_config.yml ensures proper window sizing:
```yaml
window:
  size: (1536, 864)  # 80% of 1920x1080
  position_string: "OO"  # Center of screen
```

This implementation provides a seamless development experience with proper IPython integration.