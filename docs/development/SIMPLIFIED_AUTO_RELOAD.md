# Simplified Auto-Reload Implementation

## What We Changed

### 1. Removed Complex Threading
- Removed queue-based file change handling
- Removed Pyglet clock scheduling
- Direct callback from file watcher to handler

### 2. Simplified File Change Handler
- Works just like checkpoint_paste
- Finds the changed line
- Restores to checkpoint before that line
- Runs all code after that checkpoint

### 3. Clean Implementation
```python
# When file changes:
1. Find what line changed
2. Find checkpoint before that line
3. Restore scene state to checkpoint
4. Extract code after checkpoint
5. Run it with exec()
```

## Testing

Run the test scene:
```bash
maniml test_simple_reload.py TestSimpleReload
```

Then edit line 15 while it's running:
- Change `Square` to `Circle`
- Change `RED` to `GREEN`
- Save the file

You should see:
```
File changed! Auto-reloading...
Change detected at line 15
Restoring to checkpoint 3 (line 13)
Running updated code...
Reload complete!
```

## How It Works

1. **Checkpoints**: Automatically saved at each `play()` and `wait()`
2. **File Watching**: Simple thread watches for file changes
3. **State Restoration**: Uses ManimGL's `restore_state()` 
4. **Code Execution**: Runs updated code in proper namespace

## Configuration

Window size is configured in `custom_config.yml`:
```yaml
window:
  size: (1536, 864)  # 80% of 1920x1080
  position_string: "OO"  # Center
```

## Differences from Previous Implementation

- No threading complexity
- No queue management
- No Pyglet event loop integration
- Direct, simple approach like ManimGL's checkpoint_paste

This simplified approach should be more reliable and easier to debug.