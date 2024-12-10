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
        self.toggle.move_to(self.base.get_top() - UP * 0.3 if self.switch_state else self.base.get_bottom() + UP * 0.3)

        # Add the base and toggle to the switch
        self.add(self.base, self.toggle)

    def toggle_switch(self):
        """Toggle the switch state between ON and OFF."""
        self.switch_state = not self.switch_state
        new_position = self.base.get_top() - UP * 0.3 if self.switch_state else self.base.get_bottom() + UP * 0.3
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
        self.light_switch = LightSwitch()
        self.light = Light()

        # Position the light switch and light in the room
        self.light_switch.move_to(LEFT * 2)
        self.light.move_to(RIGHT * 2)

        # Add the light switch and light to the room
        self.add(self.light_switch, self.light)

    def toggle_light(self):
        """Toggle the light based on the switch's state."""
        animations = [self.light_switch.toggle_switch()]
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

        # Step 3: Introduce the metaphor
        room = Room()
        self.play(FadeIn(room))
        self.wait(1)

        # Step 4: Add narration text
        narration_text = Text("Imagine a light switch in your room.", color=WHITE, font_size=36).to_edge(UP)
        self.play(Write(narration_text))
        self.wait(2)

        # Step 5: Highlight the LightSwitch
        highlight = SurroundingRectangle(room.light_switch, color=BLUE, buff=0.2)
        switch_text = Text("This switch can only be ON or OFF.", color=WHITE, font_size=24).next_to(room.light_switch, DOWN)
        self.play(Create(highlight), Write(switch_text))
        self.wait(2)

        # Step 6: Demonstrate the OFF state
        off_text = Text("When the switch is OFF, the light is not shining (false).", color=WHITE, font_size=24).to_edge(DOWN)
        self.play(Write(off_text))
        self.wait(2)

        # Step 7: Switch to the ON state
        self.play(*room.toggle_light())
        on_text = Text("When the switch is ON, the light is shining (true).", color=WHITE, font_size=24).to_edge(DOWN)
        self.play(Transform(off_text, on_text))
        self.wait(2)

        # Step 8: Explain the metaphor
        self.play(FadeOut(off_text), FadeOut(highlight), FadeOut(switch_text))
        metaphor_text = Text("In programming, a Boolean is like this light switch.", color=WHITE, font_size=36).to_edge(UP)
        self.play(Transform(narration_text, metaphor_text))
        self.wait(2)

        # Step 9: Toggle back to OFF
        self.play(*room.toggle_light())
        toggle_text = Text("It can only be true (ON) or false (OFF).", color=WHITE, font_size=24).to_edge(DOWN)
        self.play(Write(toggle_text))
        self.wait(2)

        # Step 10: Summarize the concept
        self.play(FadeOut(toggle_text), FadeOut(narration_text))
        summary_text = Text("A Boolean controls whether a condition is true or false.", color=WHITE, font_size=36)
        self.play(Write(summary_text))
        self.wait(2)

        # Step 11: Fade out the scene
        self.play(FadeOut(room), FadeOut(summary_text))

        # Step 12: End with a thank you message
        thank_you = Text("Thanks for watching", color=WHITE, font_size=48)
        self.play(Write(thank_you))
        self.wait(2)

        # Step 13: Fade out the thank you message
        self.play(FadeOut(thank_you))