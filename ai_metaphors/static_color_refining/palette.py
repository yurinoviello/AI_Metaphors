from manim import ManimColor

# JetBrains dark theme color palette plus white and black
PALETTE_HEX = ["#28b8a0", "#fc801d", "#ff318c", "#6b57ff", "#ffffff", "#000000"]
PALETTE = [ManimColor(hex_color) for hex_color in PALETTE_HEX]


def nearest_color(color: ManimColor, threshold: float = 0.075) -> ManimColor:
    src_r, src_g, src_b = color.to_int_rgb()

    def norm(c: ManimColor) -> float:
        r, g, b = c.to_int_rgb()
        return ((src_r - r) ** 2 + (src_g - g) ** 2 + (src_b - b) ** 2) / (3 * 255 ** 2)

    closest = min(PALETTE, key=norm)

    if norm(closest) < threshold:
        return color
    else:
        return closest
