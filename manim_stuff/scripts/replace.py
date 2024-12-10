import manimpango
manimpango.register_font('/home/ynoviello/Downloads/JetBrainsSans-Regular.ttf')
from manim import DARK_BROWN as BROWN
from manim import *

# Define the Editor class
class Editor(VGroup):
    def __init__(self, editor_height=1.0, start_position=ORIGIN, colour=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.editor_height = editor_height
        # Create the head
        self.head = Circle(radius=self.editor_height * 0.3)
        self.head.set_color(colour)
        self.head.set_fill(colour, opacity=1)
        # Create the body
        self.body = Rectangle(width=self.editor_height * 0.7, height=self.editor_height)
        self.body.set_color(colour)
        self.body.set_fill(colour, opacity=1)
        # Position the head above the body
        self.head.next_to(self.body, UP, buff=0.1)
        # Move the editor to the starting position
        self.move_to(start_position)
        # Add the editor parts to the VGroup
        self.add(self.head, self.body)

    def replace_text(self, line, old_text, new_text):
        """Simulates the editor replacing text in a line."""
        new_line = line.replace_text(old_text, new_text)
        return TransformMatchingTex(line, new_line)

# Define the Book class
class Book(VGroup):
    def __init__(self, num_pages=5, lines_per_page=4, **kwargs):
        super().__init__(**kwargs)
        self.pages = []
        for i in range(num_pages):
            page = Page(lines_per_page=lines_per_page)
            page.move_to(RIGHT * i * 2)
            self.pages.append(page)
            self.add(page)

# Define the Page class
class Page(VGroup):
    def __init__(self, lines_per_page=4, **kwargs):
        super().__init__(**kwargs)
        self.lines = []
        for i in range(lines_per_page):
            line = LineOfText(text=f"Line {i+1}: John is here.")
            line.move_to(UP * (lines_per_page / 2 - i))
            self.lines.append(line)
            self.add(line)

# Define the LineOfText class
class LineOfText(Text):
    def __init__(self, text="", **kwargs):
        super().__init__(text, **kwargs)

    def replace_text(self, old_text, new_text):
        """Replaces occurrences of old_text with new_text in the line."""
        new_content = self.text.replace(old_text, new_text)
        return LineOfText(text=new_content)

# Main animation class
class ReplaceFunctionAnimation(Scene):
    def construct(self):
        # Title Scene
        title = Text("replace", color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Metaphor Animation
        # Scene Setup
        book = Book(num_pages=3, lines_per_page=3)
        book.move_to(LEFT * 2)
        self.play(FadeIn(book))

        # Introducing the Editor
        editor = Editor(start_position=LEFT * 6)
        self.play(editor.animate.move_to(LEFT * 4), run_time=2)
        self.play(editor.animate.move_to(LEFT * 3))

        # Explaining the Task
        task_text = Text("The editor's task is to replace 'John' with 'Jack'.", font_size=24).to_edge(UP)
        self.play(Write(task_text))
        self.play(editor.animate.shift(RIGHT * 0.5), editor.animate.shift(LEFT * 0.5))

        # Editor in Action
        for page in book.pages:
            # Zoom into the page
            self.play(FocusOn(page))
            self.play(page.animate.scale(1.2).move_to(ORIGIN))
            for line in page.lines:
                # Highlight the line
                self.play(Indicate(line, color=YELLOW))
                # Replace 'John' with 'Jack'
                replacement_animation = editor.replace_text(line, "John", "Jack")
                self.play(replacement_animation)
                # Return line to original color
                self.play(line.animate.set_color(WHITE))
            # Zoom out to the full book
            self.play(page.animate.scale(1 / 1.2).move_to(book))

        # Completion
        updated_text = Text("The story now reads with the new name throughout.", font_size=24).to_edge(UP)
        self.play(Transform(task_text, updated_text))
        self.wait(2)

        # Ending Scene
        self.play(FadeOut(editor), FadeOut(book), FadeOut(task_text))
        thank_you = Text("Thanks for watching", color=WHITE)
        self.play(Write(thank_you))
        self.wait(2)
        self.play(FadeOut(thank_you))