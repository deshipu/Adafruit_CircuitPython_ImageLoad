# SPDX-FileCopyrightText: 2018 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Matt Land
# SPDX-FileCopyrightText: Brooke Storm
# SPDX-FileCopyrightText: Sam McGahan
#
# SPDX-License-Identifier: MIT

"""
`adafruit_imageload.pnm.pgm.ascii`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Matt Land, Brooke Storm, Sam McGahan

"""
try:
    from typing import Tuple, Set, Optional
    from io import BufferedReader
    from displayio import Palette, Bitmap
    from ...displayio_types import PaletteConstructor, BitmapConstructor
except ImportError:
    pass


def load(
    file: BufferedReader,
    width: int,
    height: int,
    bitmap: BitmapConstructor = None,
    palette: PaletteConstructor = None,
) -> Tuple[Optional[Bitmap], Optional[Palette]]:
    """
    Load a PGM ascii file (P2)
    """
    data_start = file.tell()  # keep this so we can rewind
    _palette_colors = set()
    pixel = bytearray()
    # build a set of all colors present in the file, so palette and bitmap can be constructed
    while True:
        byte = file.read(1)
        if byte == b"":
            break
        if not byte.isdigit():
            int_pixel = int("".join(["%c" % char for char in pixel]))
            _palette_colors.add(int_pixel)
            pixel = bytearray()
        pixel += byte
    if palette:
        palette = build_palette(palette, _palette_colors)  # type: Palette
    if bitmap:
        bitmap = bitmap(width, height, len(_palette_colors))  # type: Bitmap
        _palette_colors = list(_palette_colors)
        file.seek(data_start)
        for y in range(height):
            for x in range(width):
                pixel = bytearray()
                while True:
                    byte = file.read(1)
                    if not byte.isdigit():
                        break
                    pixel += byte
                int_pixel = int("".join(["%c" % char for char in pixel]))
                bitmap[x, y] = _palette_colors.index(int_pixel)
    return bitmap, palette


def build_palette(
    palette_class: PaletteConstructor, palette_colors: Set[int]
) -> Palette:  # pylint: disable=duplicate-code
    """
    construct the Palette, and populate it with the set of palette_colors
    """
    palette = palette_class(len(palette_colors))
    for counter, color in enumerate(palette_colors):
        palette[counter] = bytes([color, color, color])
    return palette
