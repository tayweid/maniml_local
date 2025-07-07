from __future__ import annotations

from colour import Color
from colour import hex2rgb
from colour import rgb2hex
import numpy as np
import random
from matplotlib import pyplot

from maniml.manimgl_core.constants import COLORMAP_3B1B
from maniml.manimgl_core.constants import WHITE
from maniml.manimgl_core.utils.bezier import interpolate
from maniml.manimgl_core.utils.iterables import resize_with_interpolation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Sequence, Callable
    from maniml.manimgl_core.typing import ManimColor, Vect3, Vect4, Vect3Array, Vect4Array, NDArray


def color_to_rgb(color: ManimColor) -> Vect3:
    if isinstance(color, str):
        return hex_to_rgb(color)
    elif isinstance(color, Color):
        return np.array(color.get_rgb())
    else:
        raise Exception("Invalid color type")


def color_to_rgba(color: ManimColor, alpha: float = 1.0) -> Vect4:
    return np.array([*color_to_rgb(color), alpha])


def rgb_to_color(rgb: Vect3 | Sequence[float]) -> Color:
    try:
        return Color(rgb=tuple(rgb))
    except ValueError:
        return Color(WHITE)


def rgba_to_color(rgba: Vect4) -> Color:
    return rgb_to_color(rgba[:3])


def rgb_to_hex(rgb: Vect3 | Sequence[float]) -> str:
    return rgb2hex(rgb, force_long=True).upper()


def hex_to_rgb(hex_code: str) -> Vect3:
    return np.array(hex2rgb(hex_code))


def invert_color(color: ManimColor) -> Color:
    return rgb_to_color(1.0 - color_to_rgb(color))


def color_to_int_rgb(color: ManimColor) -> np.ndarray[int, np.dtype[np.uint8]]:
    return (255 * color_to_rgb(color)).astype('uint8')


def color_to_int_rgba(color: ManimColor, opacity: float = 1.0) -> np.ndarray[int, np.dtype[np.uint8]]:
    alpha = int(255 * opacity)
    return np.array([*color_to_int_rgb(color), alpha], dtype=np.uint8)


def color_to_hex(color: ManimColor) -> str:
    return Color(color).get_hex_l().upper()


def hex_to_int(rgb_hex: str) -> int:
    return int(rgb_hex[1:], 16)


def int_to_hex(rgb_int: int) -> str:
    return f"#{rgb_int:06x}".upper()


def color_gradient(
    reference_colors: Iterable[ManimColor],
    length_of_output: int
) -> list[Color]:
    if length_of_output == 0:
        return []
    rgbs = list(map(color_to_rgb, reference_colors))
    alphas = np.linspace(0, (len(rgbs) - 1), length_of_output)
    floors = alphas.astype('int')
    alphas_mod1 = alphas % 1
    # End edge case
    alphas_mod1[-1] = 1
    floors[-1] = len(rgbs) - 2
    return [
        rgb_to_color(np.sqrt(interpolate(rgbs[i]**2, rgbs[i + 1]**2, alpha)))
        for i, alpha in zip(floors, alphas_mod1)
    ]


def interpolate_color(
    color1: ManimColor,
    color2: ManimColor,
    alpha: float
) -> Color:
    rgb = np.sqrt(interpolate(color_to_rgb(color1)**2, color_to_rgb(color2)**2, alpha))
    return rgb_to_color(rgb)


def interpolate_color_by_hsl(
    color1: ManimColor,
    color2: ManimColor,
    alpha: float
) -> Color:
    hsl1 = np.array(Color(color1).get_hsl())
    hsl2 = np.array(Color(color2).get_hsl())
    return Color(hsl=interpolate(hsl1, hsl2, alpha))


def average_color(*colors: ManimColor) -> Color:
    rgbs = np.array(list(map(color_to_rgb, colors)))
    return rgb_to_color(np.sqrt((rgbs**2).mean(0)))


def random_color() -> Color:
    return Color(rgb=tuple(np.random.random(3)))


def random_bright_color(
    hue_range: tuple[float, float] = (0.0, 1.0),
    saturation_range: tuple[float, float] = (0.5, 0.8),
    luminance_range: tuple[float, float] = (0.5, 1.0),
) -> Color:
    return Color(hsl=(
        interpolate(*hue_range, random.random()),
        interpolate(*saturation_range, random.random()),
        interpolate(*luminance_range, random.random()),
    ))


def get_colormap_from_colors(colors: Iterable[ManimColor]) -> Callable[[Sequence[float]], Vect4Array]:
    """
    Returns a funciton which takes in values between 0 and 1, and returns
    a corresponding list of rgba values
    """
    rgbas = np.array([color_to_rgba(color) for color in colors])

    def func(values):
        alphas = np.clip(values, 0, 1)
        scaled_alphas = alphas * (len(rgbas) - 1)
        indices = scaled_alphas.astype(int)
        next_indices = np.clip(indices + 1, 0, len(rgbas) - 1)
        inter_alphas = scaled_alphas % 1
        inter_alphas = inter_alphas.repeat(4).reshape((len(indices), 4))
        result = interpolate(rgbas[indices], rgbas[next_indices], inter_alphas)
        return result

    return func


def get_color_map(map_name: str) -> Callable[[Sequence[float]], Vect4Array]:
    if map_name == "3b1b_colormap":
        return get_colormap_from_colors(COLORMAP_3B1B)
    return pyplot.get_cmap(map_name)


# Delete this?
def get_colormap_list(
    map_name: str = "viridis",
    n_colors: int = 9
) -> Vect3Array:
    """
    Options for map_name:
    3b1b_colormap
    magma
    inferno
    plasma
    viridis
    cividis
    twilight
    twilight_shifted
    turbo
    """
    from matplotlib.cm import cmaps_listed

    if map_name == "3b1b_colormap":
        rgbs = np.array([color_to_rgb(color) for color in COLORMAP_3B1B])
    else:
        rgbs = cmaps_listed[map_name].colors  # Make more general?
    return resize_with_interpolation(np.array(rgbs), n_colors)
