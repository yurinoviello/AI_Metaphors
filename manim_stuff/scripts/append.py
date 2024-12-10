import manimpango
manimpango.register_font('/home/ynoviello/Downloads/JetBrainsSans-Regular.ttf')
from manim import DARK_BROWN as BROWN
from manim import *

# Define the Scrapbook class
class Scrapbook(VGroup):
    def __init__(self, num_pages=1, page_width=2.0, page_height=3.0, **kwargs):
        super().__init__(**kwargs)
        self.pages = []
        for i in range(num_pages):
            page = Rectangle(
                width=page_width,
                height=page_height,
                color=WHITE,
                fill_color=WHITE,
                fill_opacity=1
            )
            page.shift(RIGHT * i * 0.1)  # Slight offset to simulate thickness
            self.pages.append(page)
            self.add(page)

    def add_page(self):
        new_page = Rectangle(
            width=self.pages[0].width,
            height=self.pages[0].height,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=1
        )
        new_page.shift(RIGHT * len(self.pages) * 0.1)
        self.pages.append(new_page)
        self.add(new_page)
        return FadeIn(new_page)

# Define the GlueStick class
class GlueStick(VGroup):
    def __init__(self, stick_height=1.0, stick_width=0.3, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.body = Rectangle(
            width=stick_width,
            height=stick_height,
            color=color,
            fill_color=color,
            fill_opacity=1
        )
        self.cap = Circle(
            radius=stick_width / 2,
            color=color,
            fill_color=color,
            fill_opacity=1
        )
        self.cap.next_to(self.body, UP, buff=0)
        self.add(self.body, self.cap)

    def apply_glue(self, scrapbook, photo_or_note):
        return ApplyMethod(photo_or_note.next_to, scrapbook.pages[-1], UP, buff=0.1)

# Define the PhotoOrNote class
class PhotoOrNote(VGroup):
    def __init__(self, text="", width=1.5, height=1.0, color=YELLOW, **kwargs):
        super().__init__(**kwargs)
        self.note = Rectangle(
            width=width,
            height=height,
            color=color,
            fill_color=color,
            fill_opacity=1
        )
        self.text = Text(text, font_size=24).move_to(self.note.get_center())
        self.add(self.note, self.text)

# Define the main animation scene
class AppendFunctionAnimation(Scene):
    def construct(self):
        # Step 1: Display the title
        title = Text("append", font_size=72, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Step 2: Introduce the Scrapbook
        scrapbook = Scrapbook(num_pages=1)
        scrapbook_label = Text("Scrapbook (StringBuilder)", font_size=24, color=WHITE)
        scrapbook_label.next_to(scrapbook, DOWN)
        scrapbook_group = VGroup(scrapbook, scrapbook_label).move_to(LEFT * 2)
        self.play(FadeIn(scrapbook_group))

        # Step 3: Introduce the Glue Stick
        glue_stick = GlueStick()
        glue_stick_label = Text("Glue Stick (append)", font_size=24, color=WHITE)
        glue_stick_label.next_to(glue_stick, DOWN)
        glue_stick_group = VGroup(glue_stick, glue_stick_label).move_to(RIGHT * 2)
        self.play(FadeIn(glue_stick_group))

        # Step 4: Introduce the First Photo or Note
        first_note = PhotoOrNote("Vacation Photo")
        first_note_label = Text("New Text", font_size=24, color=WHITE)
        first_note_label.next_to(first_note, DOWN)
        first_note_group = VGroup(first_note, first_note_label).move_to(glue_stick.get_center() + UP * 1.5)
        self.play(FadeIn(first_note_group))

        # Step 5: Demonstrate the Append Process
        self.play(glue_stick.animate.shift(UP * 1.5))
        self.play(Indicate(glue_stick, color=YELLOW))
        self.play(glue_stick.apply_glue(scrapbook, first_note))
        self.play(scrapbook.add_page())
        self.wait(1)

        # Step 6: Add a Second Photo or Note
        second_note = PhotoOrNote("Birthday Note")
        second_note_label = Text("New Text", font_size=24, color=WHITE)
        second_note_label.next_to(second_note, DOWN)
        second_note_group = VGroup(second_note, second_note_label).move_to(glue_stick.get_center() + UP * 1.5)
        self.play(FadeIn(second_note_group))
        self.play(glue_stick.animate.shift(UP * 1.5))
        self.play(Indicate(glue_stick, color=YELLOW))
        self.play(glue_stick.apply_glue(scrapbook, second_note))
        self.play(scrapbook.add_page())
        self.wait(1)

        # Step 7: Add a Third Photo or Note
        third_note = PhotoOrNote("Graduation Photo")
        third_note_label = Text("New Text", font_size=24, color=WHITE)
        third_note_label.next_to(third_note, DOWN)
        third_note_group = VGroup(third_note, third_note_label).move_to(glue_stick.get_center() + UP * 1.5)
        self.play(FadeIn(third_note_group))
        self.play(glue_stick.animate.shift(UP * 1.5))
        self.play(Indicate(glue_stick, color=YELLOW))
        self.play(glue_stick.apply_glue(scrapbook, third_note))
        self.play(scrapbook.add_page())
        self.wait(1)

        # Step 8: Summarize the Metaphor
        self.play(FadeOut(glue_stick_group, first_note_group, second_note_group, third_note_group))
        summary_text = Text(
            "The append function is like a glue stick.\nIt adds new text to the StringBuilder.",
            font_size=36,
            color=WHITE
        )
        summary_text.move_to(UP * 2)
        self.play(Write(summary_text))
        self.wait(2)

        # Step 9: Final Scene
        self.play(FadeOut(scrapbook_group, summary_text))
        thanks = Text("Thanks for watching", font_size=48, color=WHITE)
        self.play(Write(thanks))
        self.wait(2)
        self.play(FadeOut(thanks))