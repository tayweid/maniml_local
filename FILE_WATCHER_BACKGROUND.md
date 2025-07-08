# File Watcher with Background Checkpoint Creation

## How It Works

When you edit and save a file while maniml is running:

1. **Change Detection**
   - File watcher detects which lines changed
   - Identifies which animations are affected

2. **State Restoration**
   - Restores to the checkpoint before the first affected animation
   - Clears all invalid checkpoints after that point

3. **Background Execution**
   - Sets `skip_animations = True` to suppress visual execution
   - Executes the entire construct method from the beginning
   - Animations run instantly without rendering
   - New checkpoints are created with proper animation info

4. **Ready for Navigation**
   - All checkpoints now have correct animation info
   - Arrow key navigation works seamlessly
   - No more "line 609" errors or missing animations

## Example Flow

```python
# Original file:
self.play(Create(square))  # Line 17

# Edit to:
self.play(FadeIn(square))  # Line 17
```

Console output:
```
File changed! Auto-reloading...
Changed lines: [(17, 17)]
Affected animations: [3]
[RESTORE] Restoring to checkpoint 1 (before first affected)
Cleared checkpoints from 2 to 5
Creating checkpoints in background...
Executing construct method (animations suppressed)...
Created 4 new checkpoints in background
Background checkpoint creation complete!
Reload complete!
```

Now when you navigate:
- LEFT/RIGHT arrows work with all animations
- Checkpoints have correct line numbers
- FadeIn animation plays instead of Create

## Benefits

1. **Fast** - No visual execution during reload
2. **Complete** - All checkpoints are created properly
3. **Seamless** - Navigation works immediately after reload
4. **Accurate** - Line numbers and animation info are correct

## Technical Details

The key insight is using the existing `skip_animations` flag:
- When `True`, animations execute instantly without rendering
- Checkpoints are still created with proper info
- The scene state is updated without visual delay

This approach elegantly solves the checkpoint invalidation problem while maintaining smooth user experience.