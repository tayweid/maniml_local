# Auto-Reload Features in maniml

## Overview
maniml now includes automatic file watching and checkpoint-based reloading, similar to ManimGL's checkpoint_paste but with automatic file monitoring.

## Key Features

### 1. Automatic File Watching
- The scene automatically watches for changes to your Python file
- When you save the file, it detects changes and reloads intelligently
- No need to manually trigger reloads - just save!

### 2. Smart Checkpoint System
- Every `play()` and `wait()` call creates an automatic checkpoint
- The system tracks which line each animation was called from
- When you change code, it finds the checkpoint before your change
- Only the changed code is executed, not the entire scene

### 3. Interactive Commands
Available in interactive mode:
- `list_checkpoints()` - Show all saved animation checkpoints
- `jump_to(n)` - Jump instantly to checkpoint n
- `checkpoint_paste()` - Run code from clipboard with checkpoint support
- `reload()` - Manually reload the scene if needed

### 4. State Preservation
- The window stays open during reloads
- IPython session continues running
- All mobjects maintain their state
- Named objects (with `.name` attribute) are accessible by name

## Usage Example

```python
from maniml import *

class AutoReloadExample(Scene):
    def construct(self):
        # Initial setup
        title = Text("Auto-Reload Demo")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Create a shape - edit this line and save!
        shape = Circle(radius=1, color=BLUE)  # Try: Square(), Triangle()
        shape.name = "shape"
        self.play(Create(shape))
        
        # Move it - change the direction!
        self.play(shape.animate.shift(RIGHT * 2))  # Try: LEFT, UP, DOWN
        
        # Enter interactive mode
        self.interactive_embed()
```

## How It Works

1. **File Monitoring**: Uses a simple file watcher that checks for changes every second
2. **Change Detection**: Compares the new file content with the original
3. **Smart Reloading**: 
   - Finds which line changed
   - Restores to the checkpoint before that line
   - Executes only the new/changed code
4. **Error Handling**: Syntax errors are caught and reported without crashing

## Testing Auto-Reload

1. Run one of the example files:
   ```bash
   maniml auto_reload_demo.py AutoReloadDemo
   ```

2. While it's in interactive mode, edit the file:
   - Change colors (BLUE → GREEN)
   - Change shapes (Circle → Square)
   - Modify parameters (radius=1 → radius=2)
   - Add new animations after existing ones

3. Save the file and watch it auto-reload!

## Differences from ManimGL/ManimCE

- **ManimGL**: Uses module reloading and recreates the scene
- **ManimCE GL**: Manual checkpoint_paste with clipboard
- **maniml**: Automatic file watching with smart partial execution

## Limitations

- Only tracks changes within the `construct()` method
- Maximum 50 checkpoints kept in memory
- File check interval is 1 second
- Changes before the first animation require manual reload()

## Configuration

Auto-reload is enabled by default. To disable:
```python
class MyScene(Scene):
    def __init__(self, **kwargs):
        kwargs['auto_reload'] = False
        super().__init__(**kwargs)
```