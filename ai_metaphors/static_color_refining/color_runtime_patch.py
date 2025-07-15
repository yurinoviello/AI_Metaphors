import numpy as np
from manim import Scene, Mobject, VMobject, ManimColor
from .palette import nearest_color


def _normalize_colors(mob: Mobject):
    if isinstance(mob, VMobject):
        if np.all(mob.get_fill_opacities() == 0):
            mob.set_stroke(nearest_color(mob.get_stroke_color()))
        else:
            mob.set_fill(nearest_color(mob.get_fill_color()))
    for sub in mob.submobjects:
        _normalize_colors(sub)


_original_add = Scene.add


def _patched_add(self: Scene, *mobs):
    for mob in mobs:
        _normalize_colors(mob)
    return _original_add(self, *mobs)


Scene.add = _patched_add

_original_play = Scene.play


def _patched_play(self: Scene, *anims, **kwargs):
    res = _original_play(self, *anims, **kwargs)
    for mob in self.mobjects:
        _normalize_colors(mob)
    return res


Scene.play = _patched_play

_original_construct = Scene.construct


def _patched_construct(self: Scene):
    _original_construct(self)
    for mob in self.mobjects:
        _normalize_colors(mob)


Scene.construct = _patched_construct


def _wrap_setters(method_name: str):
    original_method = getattr(VMobject, method_name)

    def wrapped_method(self: VMobject, *args, **kwargs):
        if args:
            args = (nearest_color(ManimColor(args[0])),) + args[1:]
        if "color" in kwargs and kwargs["color"] is not None:
            kwargs["color"] = nearest_color(ManimColor(kwargs["color"]))
        return original_method(self, *args, **kwargs)

    return wrapped_method


for name in ("set_fill", "set_stroke", "set_color"):
    setattr(VMobject, name, _wrap_setters(name))

print("✅  Color runtime patch is active.")
