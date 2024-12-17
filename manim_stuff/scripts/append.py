import manimpango
manimpango.register_font('./resources/JetBrainsSans-Regular.ttf')
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
        # Create the body of the glue stick
        body = Rectangle(
            width=stick_width,
            height=stick_height,
            color=color,
            fill_color=color,
            fill_opacity=1
        )
        # Create the cap of the glue stick
        cap = Rectangle(
            width=stick_width * 1.2,
            height=stick_height * 0.2,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=1
        )
        cap.next_to(body, UP, buff=0)
        self.add(body, cap)

    def apply_glue(self, scrapbook, photo_or_note):
        # Simulate attaching a photo or note to the scrapbook
        scrapbook.add_page()
        return FadeIn(photo_or_note)

# Define the PhotoOrNote class
class PhotoOrNote(VGroup):
    def __init__(self, content="", width=1.5, height=1.0, color=YELLOW, **kwargs):
        super().__init__(**kwargs)
        # Create the note or photo rectangle
        self.rect = Rectangle(
            width=width,
            height=height,
            color=color,
            fill_color=color,
            fill_opacity=1
        )
        # Add text content to the note or photo
        self.text = Text(content, font_size=24)
        self.text.move_to(self.rect.get_center())
        self.add(self.rect, self.text)

    def move_to_scrapbook(self, scrapbook):
        # Move the photo or note to the scrapbook's position
        return self.animate.move_to(scrapbook.pages[-1].get_center())

# Main animation scene
class AppendFunctionAnimation(Scene):
    def construct(self):
        # Step 1: Display the title
        title = Text("append", font_size=72, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Step 2: Introduce the Scrapbook
        scrapbook = Scrapbook()
        scrapbook.move_to(LEFT * 2)
        self.play(FadeIn(scrapbook))

        # Step 3: Introduce the Glue Stick
        glue_stick = GlueStick()
        glue_stick.move_to(RIGHT * 2 + DOWN * 1)
        self.play(FadeIn(glue_stick))

        # Step 4: Introduce the First Photo or Note
        first_note = PhotoOrNote(content="Vacation Photo")
        first_note.move_to(UP * 2 + RIGHT * 3)
        self.play(FadeIn(first_note))

        # Step 5: Explain the Metaphor
        metaphor_text1 = Text("The scrapbook is like a StringBuilder.", font_size=24)
        metaphor_text1.move_to(DOWN * 3)
        self.play(Write(metaphor_text1))
        self.wait(2)
        self.play(FadeOut(metaphor_text1))

        metaphor_text2 = Text("The glue stick is like the append function.", font_size=24)
        metaphor_text2.move_to(DOWN * 3)
        self.play(Write(metaphor_text2))
        self.wait(2)
        self.play(FadeOut(metaphor_text2))

        # Step 6: Attach the First Photo or Note
        append_text1 = Text("Using append...", font_size=20)
        append_text1.next_to(glue_stick, UP, buff=0.5)
        self.play(Write(append_text1))
        self.play(glue_stick.animate.move_to(first_note.get_center()))
        self.play(first_note.move_to_scrapbook(scrapbook), scrapbook.add_page())
        self.play(FadeOut(append_text1))

        # Step 7: Introduce the Second Photo or Note
        second_note = PhotoOrNote(content="Birthday Note")
        second_note.move_to(UP * 2 + RIGHT * 3)
        self.play(FadeIn(second_note))

        # Step 8: Attach the Second Photo or Note
        append_text2 = Text("Appending more...", font_size=20)
        append_text2.next_to(glue_stick, UP, buff=0.5)
        self.play(Write(append_text2))
        self.play(glue_stick.animate.move_to(second_note.get_center()))
        self.play(second_note.move_to_scrapbook(scrapbook), scrapbook.add_page())
        self.play(FadeOut(append_text2))

        # Step 9: Show the Filled Scrapbook
        final_text = Text("The scrapbook grows with each append.", font_size=24)
        final_text.move_to(DOWN * 3)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text))

        # Step 10: Clear the Scene
        self.play(FadeOut(scrapbook), FadeOut(glue_stick), FadeOut(first_note), FadeOut(second_note))

        # Step 11: End with a Thank You Message
        thank_you = Text("Thanks for watching", font_size=72, color=WHITE)
        self.play(Write(thank_you))
        self.wait(2)
        self.play(FadeOut(thank_you))