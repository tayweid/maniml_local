# Plan to Fix Checkpoint Storage with Deep Copies

## The Problem
- Checkpoints currently store references to objects
- When objects are modified (e.g., `circle.scale(2)`), the checkpoint's "original" is also modified
- This causes animations to replay with incorrect parameters

## The Solution
Store deep copies of variables in checkpoints and restore variables to these copies before replaying.

## Implementation Steps

### 1. Update imports
Add `import copy` to the file

### 2. Modify `play()` method (around line 1513)
Change from storing references to storing deep copies:
```python
# Store the local variables from the calling frame
caller_locals = {}
for name, obj in frame.f_locals.items():
    if not name.startswith('_') and name != 'self':
        try:
            # Try to create a deep copy of the object
            caller_locals[name] = copy.deepcopy(obj)
        except (TypeError, AttributeError, RecursionError):
            # Some objects can't be deepcopied (e.g., Scene, functions)
            # Fall back to storing reference
            caller_locals[name] = obj
```

### 3. Modify `wait()` method (around line 1571)
Same change - store deep copies instead of references

### 4. Verify `_play_through_next_animation()` is using stored locals correctly
- It should already be doing `namespace.update(stored_locals)`
- This will now restore variables to their checkpoint values

### 5. Test the fix
- Run `python test_simple.py` 
- Verify that after editing and hot reloading, animations execute with correct scaling

## Why This Works

1. When we store `circle_copy = deepcopy(circle)` at checkpoint time
2. Later when `circle` has been scaled, we can restore with `circle = circle_copy`
3. The exec() receives the restored circle, so `circle.animate.scale(2)` works correctly
4. Visual state is handled separately by `restore_state()`, variable state by our copies

## Key Insight
Instead of complex namespace mapping, we simply:
1. Store copies of ALL variables (both mobjects and regular values)
2. When restoring, set our namespace variables to these stored copies
3. Let the scene's visual state be handled independently by restore_state()

This is much cleaner than trying to map between stored mobjects and current scene mobjects.