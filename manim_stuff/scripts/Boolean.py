import manimpango
manimpango.register_font('/home/ynoviello/Downloads/JetBrainsSans-Regular.ttf')
from manim import DARK_BROWN as BROWN
from manim import *

# LightSwitch class
class LightSwitch(VGroup):
    def __init__(self, switch_state=False, **kwargs):
        super().__init__(**kwargs)
        self.switch_state = switch_state  # False = OFF, True = ON

        # Create the switch base
        self.base = Rectangle(width=1, height=2, color=GRAY, fill_color=GRAY, fill_opacity=1)

        # Create the switch toggle
        self.toggle = Rectangle(width=0.8, height=0.6, color=WHITE, fill_color=WHITE, fill_opacity=1)
        self.toggle.move_to(self.base.get_top() - DOWN * 0.3 if self.switch_state else self.base.get_bottom() + UP * 0.3)

        # Add the base and toggle to the switch
        self.add(self.base, self.toggle)

    def toggle_switch(self):
        """Toggle the switch state between ON and OFF."""
        self.switch_state = not self.switch_state
        new_position = self.base.get_top() - DOWN * 0.3 if self.switch_state else self.base.get_bottom() + UP * 0.3
        return self.toggle.animate.move_to(new_position)

# Light class
class Light(Circle):
    def __init__(self, is_on=False, **kwargs):
        super().__init__(radius=0.5, **kwargs)
        self.is_on = is_on
        self.set_color(YELLOW if self.is_on else GRAY)
        self.set_fill(YELLOW if self.is_on else GRAY, opacity=1 if self.is_on else 0.3)

    def turn_on(self):
        """Turn the light ON."""
        self.is_on = True
        return self.animate.set_color(YELLOW).set_fill(YELLOW, opacity=1)

    def turn_off(self):
        """Turn the light OFF."""
        self.is_on = False
        return self.animate.set_color(GRAY).set_fill(GRAY, opacity=0.3)

# Room class
class Room(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the light switch and light
        self.light_switch = LightSwitch(switch_state=False)
        self.light_switch.move_to(LEFT * 2)

        self.light = Light(is_on=False)
        self.light.move_to(RIGHT * 2)

        # Add the light switch and light to the room
        self.add(self.light_switch, self.light)

    def toggle_light(self):
        """Toggle the light based on the switch state."""
        animations = []
        animations.append(self.light_switch.toggle_switch())
        if self.light_switch.switch_state:
            animations.append(self.light.turn_on())
        else:
            animations.append(self.light.turn_off())
        return animations

# Main animation scene
class BooleanAnimation(Scene):
    def construct(self):
        # Step 1: Display the title
        title = Text("Boolean", color=WHITE, font_size=72)
        self.play(Write(title))
        self.wait(2)

        # Step 2: Remove the title
        self.play(FadeOut(title))

        # Step 3: Introduce the Room
        room = Room()
        self.play(FadeIn(room))
        self.wait(1)

        # Step 4: Explain the metaphor
        metaphor_text = Text("A Boolean is like a light switch.", font_size=36).to_edge(UP)
        self.play(Write(metaphor_text))
        self.wait(3)

        # Step 5: Focus on the LightSwitch
        self.play(FadeOut(metaphor_text))
        switch_text = Text("This is the light switch. It can be ON or OFF.", font_size=30).to_edge(DOWN)
        self.play(Write(switch_text))
        self.play(Indicate(room.light_switch))
        self.wait(3)

        # Step 6: Demonstrate the OFF state
        self.play(FadeOut(switch_text))
        off_text = Text("The switch is OFF. The light is OFF.", font_size=30).to_edge(DOWN)
        self.play(Write(off_text))
        self.wait(3)

        # Step 7: Toggle the switch to ON
        self.play(FadeOut(off_text))
        on_text = Text("Now, let's turn the switch ON.", font_size=30).to_edge(DOWN)
        self.play(Write(on_text))
        self.play(*room.toggle_light())
        self.wait(3)

        # Step 8: Explain the ON state
        self.play(FadeOut(on_text))
        on_state_text = Text("The switch is ON. The light is ON.", font_size=30).to_edge(DOWN)
        self.play(Write(on_state_text))
        self.wait(3)

        # Step 9: Toggle the switch back to OFF
        self.play(FadeOut(on_state_text))
        off_again_text = Text("Now, let's turn the switch OFF again.", font_size=30).to_edge(DOWN)
        self.play(Write(off_again_text))
        self.play(*room.toggle_light())
        self.wait(3)

        # Step 10: Summarize the metaphor
        self.play(FadeOut(off_again_text))
        summary_text_top = Text("A Boolean is like this switch.", font_size=36).to_edge(UP)
        summary_text_bottom = Text("It can only be true (ON) or false (OFF).", font_size=30).to_edge(DOWN)
        self.play(Write(summary_text_top), Write(summary_text_bottom))
        self.wait(3)

        # Step 11: Clear the scene
        self.play(FadeOut(room), FadeOut(summary_text_top), FadeOut(summary_text_bottom))

        # Step 12: End with a Thank You message
        thank_you = Text("Thanks for watching", color=WHITE, font_size=48)
        self.play(Write(thank_you))
        self.wait(2)

        # Step 13: End the animation
        self.play(FadeOut(thank_you))