"""
maniml Mobjects - CE-compatible mobjects using GL backend.
"""

# Base classes
from maniml.manimgl_core.mobject.mobject import Mobject
from maniml.manimgl_core.mobject.types.vectorized_mobject import VMobject, VGroup

# Import our wrapped versions
from .text import Text, MarkupText, Paragraph
from .tex import Tex, MathTex, SingleStringMathTex, TexTemplate
from .geometry import (
    Circle, Dot, Ellipse, 
    Rectangle, Square, RoundedRectangle,
    Triangle, RegularPolygon, Polygon,
    Line, DashedLine, Arrow, DoubleArrow, Vector,
    Arc, ArcBetweenPoints, CurvedArrow, CurvedDoubleArrow,
    Angle, RightAngle, Elbow
)
from .svg_mobject import SVGMobject, ImageMobject
from .number_line import NumberLine, UnitInterval
from .coordinate_systems import Axes, ThreeDAxes, NumberPlane, PolarPlane
from .three_d import (
    Sphere, Cube, Cylinder, Cone, Torus,
    Box3D, Prism, Surface, ParametricSurface,
    Line3D, Arrow3D, Dot3D, ThreeDVMobject,
    Tetrahedron, Octahedron, Icosahedron, Dodecahedron
)
from .value_tracker import ValueTracker, ComplexValueTracker
from .graph import Graph

# Direct imports from GL (these are already compatible)
from maniml.manimgl_core.mobject.geometry import (
    Annulus, AnnularSector, Sector,
    CubicBezier, Polyline
)
from maniml.manimgl_core.mobject.svg.brace import Brace, BraceLabel
from maniml.manimgl_core.mobject.numbers import DecimalNumber, Integer
from maniml.manimgl_core.mobject.matrix import Matrix, DecimalMatrix, IntegerMatrix
from maniml.manimgl_core.mobject.interactive import (
    MotionMobject, Button, Checkbox, LinearNumberSlider,
    ColorSliders, Textbox, ControlPanel
)
# Table not available in GL
# from maniml.manimgl_core.mobject.table import Table, MathTable

__all__ = [
    # Base classes
    "Mobject", "VMobject", "VGroup",
    
    # Text
    "Text", "MarkupText", "Paragraph",
    
    # TeX
    "Tex", "MathTex", "SingleStringMathTex", "TexTemplate",
    
    # 2D Geometry
    "Circle", "Dot", "Ellipse",
    "Rectangle", "Square", "RoundedRectangle",
    "Triangle", "RegularPolygon", "Polygon",
    "Line", "DashedLine", "Arrow", "DoubleArrow", "Vector",
    "Arc", "ArcBetweenPoints", "CurvedArrow", "CurvedDoubleArrow",
    "Angle", "RightAngle", "Elbow",
    "Annulus", "AnnularSector", "Sector",
    "CubicBezier", "Polyline",
    
    # SVG and Images
    "SVGMobject", "ImageMobject",
    
    # Coordinate systems
    "NumberLine", "UnitInterval", "DecimalNumber", "Integer",
    "Axes", "ThreeDAxes", "NumberPlane", "PolarPlane",
    
    # 3D Geometry
    "Sphere", "Cube", "Cylinder", "Cone", "Torus",
    "Box3D", "Prism", "Surface", "ParametricSurface",
    "Line3D", "Arrow3D", "Dot3D", "ThreeDVMobject",
    "Tetrahedron", "Octahedron", "Icosahedron", "Dodecahedron",
    
    # Utilities
    "ValueTracker", "ComplexValueTracker",
    "Brace", "BraceLabel", "BraceBetweenPoints",
    "Matrix", "DecimalMatrix", "IntegerMatrix",
    # "Table", "MathTable",  # Not available in GL
    
    # Interactive
    "MotionMobject", "Button", "Checkbox", "LinearNumberSlider",
    "ColorSliders", "Textbox", "ControlPanel",
    
    # Graph theory
    "Graph",
]


# CE compatibility functions
from maniml.manimgl_core.constants import DEGREES

def BraceBetweenPoints(point1, point2, direction=None, **kwargs):
    """CE-compatible BraceBetweenPoints."""
    from .geometry import Line
    line = Line(point1, point2)
    if direction is None:
        direction = line.copy().rotate(90 * DEGREES).get_unit_vector()
    return Brace(line, direction=direction, **kwargs)