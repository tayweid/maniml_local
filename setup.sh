#!/bin/bash
# maniml installation script

echo "🎬 Installing maniml - Standalone Manim"
echo "======================================"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.7+ is required (found $python_version)"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install package
echo "📦 Installing maniml package..."
pip install -e .

# Test installation
echo "🧪 Testing installation..."
python -c "from maniml import *; print('✅ Import test passed')"

echo ""
echo "✨ Installation complete!"
echo ""
echo "🚀 Quick start:"
echo "   maniml examples/basic/01_hello_world.py HelloWorld"
echo ""
echo "📚 See examples/ directory for more demos"
echo "📖 See README.md for documentation"