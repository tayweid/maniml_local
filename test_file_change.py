#!/usr/bin/env python3
"""Test script to simulate file changes for testing hot reload."""

import time
import sys

# Read the original file
with open('test_simple.py', 'r') as f:
    original_content = f.read()

# Make a simple change - modify the scale factor in line 23
modified_content = original_content.replace(
    'circle.animate.scale(2)',
    'circle.animate.scale(3)'  # Change scale from 2 to 3
)

print("Modifying test_simple.py - changing scale from 2 to 3...")

# Write the modified content
with open('test_simple.py', 'w') as f:
    f.write(modified_content)

print("File modified. Waiting 3 seconds before restoring...")
time.sleep(3)

# Restore original
with open('test_simple.py', 'w') as f:
    f.write(original_content)

print("File restored to original.")