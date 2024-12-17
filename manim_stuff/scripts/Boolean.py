import manimpango
manimpango.register_font('ai_metaphors/resources/JetBrainsSans-Regular.ttf')
from manim import DARK_BROWN as BROWN
from manim import *

# LightSwitch class implementation
class LightSwitch(VGroup):
    def __init__(self, switch_height=2.0, start_state='OFF', **kwargs):
        super().__init__(**kwargs)
        self.switch_height = switch_height
        self.state = start_state.upper()

        # Create the base of the switch
        self.base = Rectangle(
            width=self.switch_height * 0.5,
            height=self.switch_height,
            color=GRAY,
            fill_color=GRAY,
            fill_opacity=1
        )

        # Create the toggle (the part that moves)
        self.toggle = Rectangle(
            width=self.switch_height * 0.4,
            height=self.switch_height * 0.2,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=1
        )

        # Position the toggle based on the initial state
        if self.state == 'ON':
            self.toggle.move_to(self.base.get_top() - DOWN * self.switch_height * 0.1)
        else:  # OFF state
            self.toggle.move_to(self.base.get_bottom() + UP * self.switch_height * 0.1)

        # Add the base and toggle to the switch
        self.add(self.base, self.toggle)

    def switch_on(self):
        """Switch the state to ON."""
        if self.state != 'ON':
            self.state = 'ON'
            return self.toggle.animate.move_to(self.base.get_top() - DOWN * self.switch_height * 0.1)

    def switch_off(self):
        """Switch the state to OFF."""
        if self.state != 'OFF':
            self.state = 'OFF'
            return self.toggle.animate.move_to(self.base.get_bottom() + UP * self.switch_height * 0.1)

    def toggle_switch(self):
        """Toggle the state between ON and OFF."""
        if self.state == 'ON':
            return self.switch_off()
        else:
            return self.switch_on()

# LightBulb class implementation
class LightBulb(VGroup):
    def __init__(self, bulb_radius=0.5, start_state='OFF', **kwargs):
        super().__init__(**kwargs)
        self.bulb_radius = bulb_radius
        self.state = start_state.upper()

        # Create the bulb
        self.bulb = Circle(
            radius=self.bulb_radius,
            color=YELLOW if self.state == 'ON' else GRAY,
            fill_color=YELLOW if self.state == 'ON' else GRAY,
            fill_opacity=1
        )

        # Add the bulb to the group
        self.add(self.bulb)

    def turn_on(self):
        """Turn the light bulb ON."""
        if self.state != 'ON':
            self.state = 'ON'
            return self.bulb.animate.set_fill(YELLOW, opacity=1).set_color(YELLOW)

    def turn_off(self):
        """Turn the light bulb OFF."""
        if self.state != 'OFF':
            self.state = 'OFF'
            return self.bulb.animate.set_fill(GRAY, opacity=1).set_color(GRAY)

    def toggle_light(self):
        """Toggle the light bulb between ON and OFF."""
        if self.state == 'ON':
            return self.turn_off()
        else:
            return self.turn_on()

# Main animation scene
class BooleanAnimation(Scene):
    def construct(self):
        # Step 1: Display the title
        title = Text("Boolean", color=WHITE).scale(1.5)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Step 2: Introduce the metaphor
        metaphor_text = Text("A Boolean is like a light switch.", color=WHITE).scale(0.7)
        metaphor_text.to_edge(UP)
        self.play(FadeIn(metaphor_text))

        # Step 3: Introduce the LightSwitch
        light_switch = LightSwitch(start_state="OFF")
        light_switch_label = Text("Light Switch (OFF)", color=WHITE).scale(0.5)
        light_switch_label.next_to(light_switch, DOWN)
        self.play(Create(light_switch), Write(light_switch_label))

        # Step 4: Introduce the LightBulb
        light_bulb = LightBulb(start_state="OFF")
        light_bulb.next_to(light_switch, RIGHT, buff=2)
        light_bulb_label = Text("Light Bulb (OFF)", color=WHITE).scale(0.5)
        light_bulb_label.next_to(light_bulb, DOWN)
        self.play(Create(light_bulb), Write(light_bulb_label))

        # Step 5: Explain the OFF state
        off_text = Text("When the switch is OFF, the light is OFF (false).", color=WHITE).scale(0.5)
        off_text.to_edge(DOWN)
        self.play(Write(off_text))
        self.wait(3)
        self.play(FadeOut(off_text))

        # Step 6: Switch to the ON state
        self.play(light_switch.switch_on(), light_bulb.turn_on())
        self.play(Transform(light_switch_label, Text("Light Switch (ON)", color=WHITE).scale(0.5).next_to(light_switch, DOWN)))
        self.play(Transform(light_bulb_label, Text("Light Bulb (ON)", color=WHITE).scale(0.5).next_to(light_bulb, DOWN)))

        # Step 7: Explain the ON state
        on_text = Text("When the switch is ON, the light is ON (true).", color=WHITE).scale(0.5)
        on_text.to_edge(DOWN)
        self.play(Write(on_text))
        self.wait(3)
        self.play(FadeOut(on_text))

        # Step 8: Toggle the switch multiple times
        for _ in range(3):
            self.play(light_switch.toggle_switch(), light_bulb.toggle_light())
            if light_switch.state == "ON":
                self.play(Transform(light_switch_label, Text("Light Switch (ON)", color=WHITE).scale(0.5).next_to(light_switch, DOWN)))
                self.play(Transform(light_bulb_label, Text("Light Bulb (ON)", color=WHITE).scale(0.5).next_to(light_bulb, DOWN)))
            else:
                self.play(Transform(light_switch_label, Text("Light Switch (OFF)", color=WHITE).scale(0.5).next_to(light_switch, DOWN)))
                self.play(Transform(light_bulb_label, Text("Light Bulb (OFF)", color=WHITE).scale(0.5).next_to(light_bulb, DOWN)))

        # Step 9: Summarize the metaphor
        self.play(FadeOut(light_switch, light_switch_label, light_bulb, light_bulb_label, metaphor_text))
        summary_text = Text("A Boolean is like a light switch: ON (true) or OFF (false).", color=WHITE).scale(0.7)
        self.play(Write(summary_text))
        self.wait(3)
        self.play(FadeOut(summary_text))

        # Step 10: End the animation
        thanks_text = Text("Thanks for watching", color=WHITE).scale(1.2)
        self.play(Write(thanks_text))
        self.wait(2)
        self.play(FadeOut(thanks_text))