from manim import DARK_BROWN as BROWN
from manim import *

# Define the Carpenter class
class Carpenter(VGroup):
    def __init__(self, carpenter_height=1.0, start_position=ORIGIN, colour=BLUE_D, **kwargs):
        super().__init__(**kwargs)
        self.carpenter_height = carpenter_height
        # Create the head
        self.head = Circle(radius=self.carpenter_height * 0.3)
        self.head.set_color(colour)
        self.head.set_fill(colour, opacity=1)
        # Create the body
        self.body = Rectangle(width=self.carpenter_height * 0.7, height=self.carpenter_height)
        self.body.set_color(colour)
        self.body.set_fill(colour, opacity=1)
        # Position the head above the body
        self.head.next_to(self.body, UP, buff=0.1)
        # Move the carpenter to the starting position
        self.move_to(start_position)
        # Add the carpenter parts to the VGroup
        self.add(self.head, self.body)

    def use_tool(self, tool):
        return FadeIn(tool)

# Define the MagicalToolbox class
class MagicalToolbox(VGroup):
    def __init__(self, toolbox_size=1.0, position=ORIGIN, colour=GOLD, **kwargs):
        super().__init__(**kwargs)
        self.toolbox_size = toolbox_size
        # Create the toolbox
        self.box = Rectangle(
            width=self.toolbox_size * 2,
            height=self.toolbox_size,
            color=colour,
            fill_color=colour,
            fill_opacity=1
        )
        # Add a label to the toolbox
        self.label = Text("Magical Toolbox", font_size=24).next_to(self.box, UP)
        # Move the toolbox to the specified position
        self.move_to(position)
        # Add the box and label to the VGroup
        self.add(self.box, self.label)

    def open_toolbox(self):
        return self.animate.set_fill(opacity=0.5)

# Define the Tool class
class Tool(VGroup):
    def __init__(self, tool_name="Tool", tool_size=0.5, position=ORIGIN, colour=GRAY, **kwargs):
        super().__init__(**kwargs)
        self.tool_size = tool_size
        # Create the tool representation
        self.tool = Rectangle(
            width=self.tool_size,
            height=self.tool_size * 0.5,
            color=colour,
            fill_color=colour,
            fill_opacity=1
        )
        # Add a label to the tool
        self.label = Text(tool_name, font_size=18).next_to(self.tool, UP, buff=0.1)
        # Move the tool to the specified position
        self.move_to(position)
        # Add the tool and label to the VGroup
        self.add(self.tool, self.label)

    def use(self):
        return self.animate.set_color(YELLOW)

# Define the Workshop class
class Workshop(VGroup):
    def __init__(self, workshop_size=5.0, position=ORIGIN, colour=LIGHT_BROWN, **kwargs):
        super().__init__(**kwargs)
        self.workshop_size = workshop_size
        # Create the workshop representation
        self.workshop = Rectangle(
            width=self.workshop_size * 2,
            height=self.workshop_size,
            color=colour,
            fill_color=colour,
            fill_opacity=1
        )
        # Add a label to the workshop
        self.label = Text("Workshop", font_size=32).next_to(self.workshop, UP)
        # Move the workshop to the specified position
        self.move_to(position)
        # Add the workshop and label to the VGroup
        self.add(self.workshop, self.label)

# Define the animation scene
class CompanionObjectScene(Scene):
    def construct(self):
        # Display the title
        title = Text("Companion Object", font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Create the workshop
        workshop = Workshop(position=ORIGIN)
        self.play(Create(workshop))
        self.wait(1)

        # Create the carpenter
        carpenter = Carpenter(start_position=LEFT * 3)
        self.play(FadeIn(carpenter))
        self.wait(1)

        # Create the magical toolbox
        toolbox = MagicalToolbox(position=RIGHT * 3)
        self.play(FadeIn(toolbox))
        self.wait(1)

        # Show the carpenter using a tool
        hammer = Tool(tool_name="Hammer", position=RIGHT * 3 + DOWN)
        self.play(FadeIn(hammer))
        self.play(carpenter.use_tool(hammer))
        self.wait(1)

        # Show the toolbox being used without the carpenter
        self.play(FadeOut(carpenter))
        self.play(toolbox.open_toolbox())
        self.play(hammer.use())
        self.wait(1)

        # Clear the scene and display the thank you message
        self.play(FadeOut(workshop), FadeOut(toolbox), FadeOut(hammer))
        thank_you = Text("Thanks for watching", font_size=48, color=WHITE)
        self.play(Write(thank_you))
        self.wait(2)
        self.play(FadeOut(thank_you))