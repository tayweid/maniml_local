# maniml Animation Reference

## Quick Reference for Available Animations

### Creation Animations
- `Create(mobject)` - Draw the mobject gradually
- `Write(text)` - Write text as if by hand
- `DrawBorderThenFill(mobject)` - Draw border first, then fill
- `ShowCreation(mobject)` - Alias for Create
- `Uncreate(mobject)` - Reverse of Create
- `Unwrite(text)` - Reverse of Write
- `AddTextLetterByLetter(text)` - Add text one letter at a time
- `AddTextWordByWord(text)` - Add text one word at a time

### Transform Animations
- `Transform(mob1, mob2)` - Morph mob1 into mob2
- `ReplacementTransform(mob1, mob2)` - Replace mob1 with mob2
- `TransformFromCopy(mob1, mob2)` - Create mob2 as a copy of mob1
- `MoveToTarget(mobject)` - Move to mobject.target
- `ApplyMethod(method, *args)` - Apply any method with animation
- `ClockwiseTransform(mob1, mob2)` - Transform with clockwise path
- `CounterclockwiseTransform(mob1, mob2)` - Transform with counterclockwise path

### Fading Animations
- `FadeIn(mobject, shift=None)` - Fade in, optionally from a direction
- `FadeOut(mobject, shift=None)` - Fade out, optionally to a direction
- `FadeInFrom(mobject, direction)` - Fade in from specified direction
- `FadeOutAndShift(mobject, direction)` - Fade out while shifting
- `FadeInFromPoint(mobject, point)` - Fade in from a specific point
- `FadeOutToPoint(mobject, point)` - Fade out to a specific point
- `FadeInFromLarge(mobject, scale_factor=2)` - Fade in while shrinking
- `FadeTransform(mob1, mob2)` - Fade out mob1 while fading in mob2

### Growing Animations
- `GrowFromCenter(mobject)` - Grow from center point
- `GrowFromPoint(mobject, point)` - Grow from specified point
- `GrowFromEdge(mobject, edge)` - Grow from specified edge
- `GrowArrow(arrow)` - Grow arrow from base to tip
- `SpinInFromNothing(mobject)` - Spin and grow from nothing
- `ShrinkToCenter(mobject)` - Shrink to center point

### Movement Animations
- `Shift(mobject, direction)` - Shift by vector amount
- `MoveTo(mobject, point_or_mobject)` - Move to position
- `Scale(mobject, scale_factor)` - Scale in place
- `Rotate(mobject, angle)` - Rotate by angle
- `Rotating(mobject, radians=2*PI)` - Continuous rotation
- `MoveAlongPath(mobject, path)` - Move along a path

### Indication Animations
- `FocusOn(mobject)` - Focus attention on mobject
- `Indicate(mobject)` - Briefly highlight mobject
- `Flash(mobject)` - Create a flash at mobject
- `CircleIndicate(mobject)` - Circle around mobject
- `ShowPassingFlashAround(mobject)` - Passing flash around border
- `Wiggle(mobject)` - Wiggle mobject
- `ShowCreationThenDestruction(mobject)` - Create then destroy
- `ShowCreationThenFadeOut(mobject)` - Create then fade out
- `Circumscribe(mobject, shape=Rectangle)` - Draw shape around mobject

### Composition Animations
- `AnimationGroup(*animations)` - Play animations together
- `Succession(*animations)` - Play animations in sequence
- `LaggedStart(*animations, lag_ratio=0.5)` - Start with delays
- `LaggedStartMap(AnimClass, mobjects)` - Apply animation with delays
- `Wait(duration=1)` - Pause for duration

### Update Animations
- `UpdateFromFunc(mobject, update_func)` - Update using function
- `UpdateFromAlphaFunc(mobject, func)` - Update based on alpha value

### Rate Functions
Available rate functions to control animation pacing:
- `linear` - Constant speed
- `smooth` - Smooth ease in/out
- `rush_into` - Start fast, slow down
- `rush_from` - Start slow, speed up
- `slow_into` - Gradual acceleration
- `double_smooth` - Extra smooth
- `there_and_back` - Go and return
- `wiggle` - Wiggle motion
- `lingering` - Pause at end
- `exponential_decay` - Exponential slowdown

## Usage Examples

```python
# Basic creation
self.play(Create(circle))

# Transform with custom rate function
self.play(Transform(circle, square, rate_func=there_and_back))

# Multiple animations with timing
self.play(
    FadeIn(text1, shift=UP),
    Create(circle),
    run_time=2,
    lag_ratio=0.5
)

# Using mobject.animate syntax
self.play(
    circle.animate.shift(RIGHT * 2).scale(1.5).set_color(RED)
)

# Succession of animations
self.play(Succession(
    Create(circle),
    Transform(circle, square),
    FadeOut(square)
))
```

## Tips
1. Most animations accept `run_time` and `rate_func` parameters
2. Use `lag_ratio` with multiple animations for staggered starts
3. The `animate` syntax works for property changes
4. Combine animations with `AnimationGroup` or play multiple at once
5. All CE animations are available with GL's performance benefits!