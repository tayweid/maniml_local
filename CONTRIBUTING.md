# Contributing to maniml

First off, thank you for considering contributing to maniml! It's people like you that make maniml such a great tool for creating mathematical animations.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style Guide](#documentation-style-guide)

## Code of Conduct

This project and everyone participating in it is governed by the [maniml Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/maniml.git
   cd maniml
   ```
3. Install in development mode:
   ```bash
   pip install -e .
   ```
4. Create a branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Great Bug Reports** include:
- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Explain why this enhancement would be useful to most maniml users
- List some other animation libraries where this enhancement exists (if applicable)

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- Issues labeled `good first issue` - should only require a few lines of code
- Issues labeled `help wanted` - more involved than beginner issues

### Pull Requests

1. Ensure your code follows the style guidelines
2. Include appropriate test cases (when we have a test framework)
3. Update documentation as necessary
4. Add a note to `CHANGELOG.md` about the changes

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add MotionPath animation class

- Implement path-following animation
- Add examples in examples/01_getting_started/
- Update documentation

Fixes #123
```

### Python Style Guide

We follow PEP 8 with these additions:

- Line length: 88 characters (Black default)
- Use type hints where possible
- Docstrings: Google style

Example:
```python
def animate_along_path(
    mobject: Mobject,
    path: Path,
    run_time: float = 1.0
) -> Animation:
    """Animate a mobject along a given path.
    
    Args:
        mobject: The mobject to animate.
        path: The path to follow.
        run_time: Duration of the animation in seconds.
        
    Returns:
        The resulting Animation object.
    """
    # Implementation here
```

### Documentation Style Guide

- Use Markdown for all documentation
- Include code examples wherever possible
- Keep explanations clear and concise
- Test all code examples before submitting

## Recognition

Contributors will be recognized in our README and release notes. Thank you for helping make maniml better!

## Questions?

Feel free to open an issue with your question or reach out on our discussions page.