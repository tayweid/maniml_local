# Changelog

All notable changes to maniml will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of maniml as a standalone Manim implementation
- Core animation system from ManimGL
- Interactive objects: MotionMobject, Button, Slider, Checkbox
- LaTeX rendering support
- 3D scene support
- Preview mode as default
- Comprehensive example library organized by difficulty
- Full documentation suite

### Changed
- Renamed project from internal name to maniml
- Restructured package to follow Python standards
- Organized examples into tutorial-style categories

### Fixed
- LaTeX rendering path issues
- Window display in preview mode
- Import system for standalone operation

## [0.1.0] - 2024-07-04

### Added
- Basic shape primitives (Circle, Square, Rectangle, etc.)
- Animation classes (Create, Write, Transform, FadeIn/Out)
- Text and MathTex support
- Value trackers and updaters
- Coordinate systems and graphing
- Window-based preview system

### Known Issues
- Some ManimCE API differences in method parameters
- ValueTracker doesn't support all operators (+=, -=, etc.)
- Limited test coverage

[Unreleased]: https://github.com/yourusername/maniml/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/maniml/releases/tag/v0.1.0