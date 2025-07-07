# Installation Guide

This guide will help you install maniml on your system.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Linux](#linux)
- [Verifying Installation](#verifying-installation)
- [Optional: LaTeX Setup](#optional-latex-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **LaTeX** (optional, for mathematical expressions)

## Quick Install

If you already have Python and Git installed:

```bash
# Clone the repository
git clone https://github.com/yourusername/maniml.git
cd maniml

# Install maniml
pip install -e .

# Test the installation
maniml examples/01_getting_started/01_hello_world.py HelloWorld
```

## Detailed Installation

### macOS

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew
   brew install python3
   
   # Or download from python.org
   ```

2. **Install Git** (if not already installed):
   ```bash
   brew install git
   ```

3. **Clone and install maniml**:
   ```bash
   git clone https://github.com/yourusername/maniml.git
   cd maniml
   pip3 install -e .
   ```

4. **Install LaTeX** (optional):
   ```bash
   brew install --cask mactex
   # Or download MacTeX from https://tug.org/mactex/
   ```

### Windows

1. **Install Python**:
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install Git**:
   - Download Git from [git-scm.com](https://git-scm.com/download/win)

3. **Clone and install maniml**:
   ```cmd
   git clone https://github.com/yourusername/maniml.git
   cd maniml
   pip install -e .
   ```

4. **Install LaTeX** (optional):
   - Download and install [MiKTeX](https://miktex.org/download)

### Linux

#### Ubuntu/Debian

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip git

# Clone and install maniml
git clone https://github.com/yourusername/maniml.git
cd maniml
pip3 install -e .

# Install LaTeX (optional)
sudo apt install texlive-full
```

#### Fedora

```bash
# Install Python and pip
sudo dnf install python3 python3-pip git

# Clone and install maniml
git clone https://github.com/yourusername/maniml.git
cd maniml
pip3 install -e .

# Install LaTeX (optional)
sudo dnf install texlive-scheme-full
```

#### Arch Linux

```bash
# Install Python and pip
sudo pacman -S python python-pip git

# Clone and install maniml
git clone https://github.com/yourusername/maniml.git
cd maniml
pip install -e .

# Install LaTeX (optional)
sudo pacman -S texlive-most
```

## Verifying Installation

1. **Check maniml command**:
   ```bash
   maniml --version
   ```

2. **Run a test animation**:
   ```bash
   maniml examples/01_getting_started/01_hello_world.py HelloWorld
   ```

3. **Test imports in Python**:
   ```python
   python3 -c "from maniml import *; print('Import successful!')"
   ```

## Optional: LaTeX Setup

LaTeX is required for rendering mathematical expressions with `MathTex`.

### Testing LaTeX

Create a file `test_latex.py`:

```python
from maniml import *

class TestLaTeX(Scene):
    def construct(self):
        equation = MathTex(r"e^{i\pi} + 1 = 0")
        self.play(Write(equation))
        self.wait()
```

Run it:
```bash
maniml test_latex.py TestLaTeX
```

If you see an error about LaTeX, make sure:
1. LaTeX is installed (see platform-specific instructions above)
2. `pdflatex` is in your PATH:
   ```bash
   which pdflatex  # macOS/Linux
   where pdflatex  # Windows
   ```

## Troubleshooting

### Common Issues

#### "maniml: command not found"

The installation directory might not be in your PATH. Try:
```bash
python3 -m maniml examples/01_getting_started/01_hello_world.py HelloWorld
```

#### ImportError: No module named 'maniml'

Make sure you installed with `-e` flag:
```bash
pip install -e .
```

#### LaTeX errors

If you get LaTeX-related errors but don't need math rendering:
- Use `Text` instead of `MathTex`
- Install LaTeX following the platform-specific instructions

#### Window doesn't appear

On some systems, you might need to install additional graphics libraries:

**Linux**:
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/yourusername/maniml/issues)
3. Open a new issue with:
   - Your operating system
   - Python version (`python3 --version`)
   - Complete error message
   - Steps to reproduce

## Next Steps

After installation:
- Follow the [Getting Started Tutorial](examples/01_getting_started/README.md)
- Explore the [Example Gallery](examples/README.md)
- Read the [API Documentation](docs/api/README.md)