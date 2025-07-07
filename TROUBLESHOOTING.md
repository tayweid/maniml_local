# Troubleshooting Guide

This guide covers common issues and their solutions when using maniml.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Import Errors](#import-errors)
- [Rendering Issues](#rendering-issues)
- [LaTeX Problems](#latex-problems)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)

## Installation Issues

### "pip install -e ." fails

**Problem**: Installation fails with permission errors or dependency conflicts.

**Solutions**:
1. Use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

2. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install with user flag:
   ```bash
   pip install --user -e .
   ```

### "maniml: command not found"

**Problem**: The maniml command isn't recognized after installation.

**Solutions**:
1. Check if it's in PATH:
   ```bash
   echo $PATH
   ```

2. Use Python module syntax:
   ```bash
   python -m maniml your_file.py YourScene
   ```

3. Reinstall with pip:
   ```bash
   pip uninstall maniml
   pip install -e .
   ```

## Import Errors

### "ImportError: No module named 'maniml'"

**Problem**: Python can't find the maniml module.

**Solutions**:
1. Verify installation:
   ```bash
   pip list | grep maniml
   ```

2. Check Python path:
   ```python
   import sys
   print(sys.path)
   ```

3. Reinstall in development mode:
   ```bash
   cd /path/to/maniml
   pip install -e .
   ```

### "ImportError: cannot import name 'SomeClass'"

**Problem**: Trying to import a class that doesn't exist in maniml.

**Solutions**:
1. Check the [API differences](examples/04_advanced_techniques/manim_api_differences.py)
2. Some ManimCE classes may not be implemented
3. Use alternative classes or methods

## Rendering Issues

### No window appears

**Problem**: Running a scene but no preview window opens.

**Solutions**:
1. Check if running in SSH/headless environment
2. Verify graphics drivers are installed
3. Try forcing window creation:
   ```python
   class MyScene(Scene):
       def construct(self):
           # Your code here
           self.wait()  # Add explicit wait
   ```

### Black screen or frozen window

**Problem**: Window opens but shows black or doesn't animate.

**Solutions**:
1. Update graphics drivers
2. Check for infinite loops in your code
3. Add explicit waits between animations:
   ```python
   self.play(Create(circle))
   self.wait(0.5)  # Add small waits
   ```

### Animations play too fast/slow

**Problem**: Animation speed isn't what you expect.

**Solutions**:
1. Adjust run_time:
   ```python
   self.play(Create(circle), run_time=2)  # 2 seconds
   ```

2. Change frame rate in scene:
   ```python
   class MyScene(Scene):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           self.camera.frame_rate = 30  # Adjust as needed
   ```

## LaTeX Problems

### "LaTeX Error" or "Failed to compile"

**Problem**: LaTeX rendering fails for MathTex objects.

**Solutions**:
1. Verify LaTeX installation:
   ```bash
   which pdflatex  # Should show path
   pdflatex --version
   ```

2. Install required packages:
   ```bash
   # Ubuntu/Debian
   sudo apt install texlive-latex-extra texlive-fonts-extra
   
   # macOS
   brew install --cask mactex
   ```

3. Use Text instead of MathTex for non-math:
   ```python
   # Instead of MathTex("Hello")
   text = Text("Hello")
   ```

### Missing LaTeX packages

**Problem**: Specific LaTeX packages not found.

**Solutions**:
1. Install full LaTeX distribution:
   ```bash
   # Ubuntu/Debian
   sudo apt install texlive-full
   
   # macOS (already includes most packages)
   brew install --cask mactex
   ```

2. Check tex_templates.yml configuration

## Performance Issues

### Slow rendering

**Problem**: Animations render very slowly.

**Solutions**:
1. Reduce quality for testing:
   ```python
   from maniml import config
   config.pixel_height = 480
   config.pixel_width = 854
   ```

2. Simplify complex scenes:
   - Use fewer objects
   - Reduce subdivision levels
   - Avoid nested VGroups with many elements

3. Profile your code:
   ```python
   import cProfile
   cProfile.run('scene.run()')
   ```

### High memory usage

**Problem**: maniml uses too much RAM.

**Solutions**:
1. Clear unused objects:
   ```python
   self.remove(old_mobject)
   ```

2. Avoid creating objects in loops:
   ```python
   # Bad
   for i in range(1000):
       self.add(Circle())
   
   # Good
   circles = VGroup(*[Circle() for i in range(1000)])
   self.add(circles)
   ```

## Platform-Specific Issues

### macOS

**"No window appears on macOS"**
- Check Security & Privacy settings
- Allow Terminal/IDE to control computer
- Try running from Terminal instead of IDE

### Windows

**"DLL load failed"**
- Install Visual C++ Redistributable
- Update Windows
- Reinstall Python with "Add to PATH" checked

### Linux

**"Cannot connect to X server"**
- Install X11 libraries:
  ```bash
  sudo apt install xorg
  ```
- For WSL, install VcXsrv on Windows

## Getting Further Help

If your issue isn't covered here:

1. **Search existing issues**: https://github.com/yourusername/maniml/issues
2. **Ask on discussions**: https://github.com/yourusername/maniml/discussions
3. **Create a new issue** with:
   - Operating system and version
   - Python version
   - Complete error message
   - Minimal code example
   - Steps to reproduce

## Debug Mode

For more detailed error information:

```python
from maniml import config
config.verbosity = "DEBUG"

# Your scene code here
```

This will provide more detailed logging to help diagnose issues.