from manim import ManimColor, Mobject, Scene, VMobject
import numpy as np

from ai_metaphors.static_color_refining.palette import nearest_color

KEYS_TO_CLAMP = (
    "color",
    "stroke_color",
    "fill_color",
)


def _normalize_colors(mob: Mobject):
    if isinstance(mob, VMobject) and mob.get_num_points() > 0:
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


def _wrap_setter(name: str):
    orig = getattr(VMobject, name)

    def wrapper(self: VMobject, *args, **kw):
        if args and args[0] is not None:
            try:
                first_clamped = nearest_color(ManimColor(args[0]))
                args = (first_clamped,) + args[1:]
            except (ValueError, TypeError):
                pass

        for key in KEYS_TO_CLAMP:
            if key in kw and kw[key] is not None:
                try:
                    kw[key] = nearest_color(ManimColor(kw[key]))
                except (ValueError, TypeError):
                    pass

        return orig(self, *args, **kw)

    return wrapper


for name in ("set_fill", "set_stroke", "set_color"):
    setattr(VMobject, name, _wrap_setter(name))

print("Color runtime patch is active!")
