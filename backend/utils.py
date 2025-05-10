import io

import cairosvg
import pygame


class FAIcon:
    def __init__(self,
                 name: str,
                 size: int,
                 version: str = "free-6.7.2-desktop"
                 ):
        """
        svg_path: Path to the .svg file.
        size: Size in pixels (width and height will be square).
        """
        svg_path = f"assets/icons/fontawesome-{version}/svgs/{name}.svg"
        self.surface = self._load_svg(svg_path, size)

    def _load_svg(self, svg_path: str, size: int) -> pygame.Surface:
        """
        Convert SVG to PNG bytes and load as Pygame Surface.
        """
        # Convert SVG to PNG in memory
        png_bytes = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
        image_stream = io.BytesIO(png_bytes)

        # Load into Pygame Surface
        return pygame.image.load(image_stream).convert_alpha()

    def render(self) -> pygame.Surface:
        return self.surface