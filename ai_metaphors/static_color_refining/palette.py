from manim import ManimColor

PALETTE_HEX = ["#28b8a0", "#fc801d", "#ff318c", "#6b57ff", "#ffffff"]
PALETTE = [ManimColor(hex_color) for hex_color in PALETTE_HEX]


def nearest_color(color: ManimColor) -> ManimColor:
    src_r, src_g, src_b = color.to_int_rgb()

    def norm(c: ManimColor) -> float:
        r, g, b = c.to_int_rgb()
        return (src_r - r) ** 2 + (src_g - g) ** 2 + (src_b - b) ** 2

    return min(PALETTE, key=norm)
