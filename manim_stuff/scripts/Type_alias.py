from manim import DARK_BROWN as BROWN
from manim import *
import manimpango
manimpango.register_font("/home/ynoviello/Downloads/JetBrainsSans-Regular.ttf" )

# Librarian class
class Librarian(VGroup):
    def __init__(self, librarian_height=1.0, start_position=ORIGIN, colour=BLUE_D, **kwargs):
        super().__init__(**kwargs)
        self.librarian_height = librarian_height
        # Create the head
        self.head = Circle(radius=self.librarian_height * 0.3)
        self.head.set_color(colour)
        self.head.set_fill(colour, opacity=1)
        # Create the body
        self.body = Rectangle(width=self.librarian_height * 0.7, height=self.librarian_height)
        self.body.set_color(colour)
        self.body.set_fill(colour, opacity=1)
        # Position the head above the body
        self.head.next_to(self.body, UP, buff=0.1)
        # Move the librarian to the starting position
        self.move_to(start_position)
        # Add the librarian parts to the VGroup
        self.add(self.head, self.body)

# Book class
class Book(VGroup):
    def __init__(self, title="", book_height=1.0, position=ORIGIN, colour=GREEN_D, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.book_height = book_height
        # Create the book cover
        cover = Rectangle(
            width=self.book_height * 0.6,
            height=self.book_height,
            color=colour,
            fill_color=colour,
            fill_opacity=1
        )
        # Add the title as text on the book
        title_text = Text(self.title, font_size=12, color=WHITE, weight=BOLD)
        title_text.scale_to_fit_width(cover.width * 0.9)
        title_text.move_to(cover.get_center())
        # Add the cover and title to the book
        self.add(cover, title_text)
        # Move the book to the specified position
        self.move_to(position)

# Nickname class
class Nickname(Text):
    def __init__(self, nickname="", position=ORIGIN, **kwargs):
        super().__init__(nickname, font_size=24, color=YELLOW, **kwargs)
        self.move_to(position)

# Main animation class
class TypeAlias(Scene):
    def construct(self):
        # Title Screen
        title = Text("Type Alias", font_size=64, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Scene Setup
        librarian = Librarian(start_position=[-4, -2, 0])
        book = Book(
            title="The Comprehensive Guide to Advanced Quantum Mechanics and Its Applications",
            position=[0, 0, 0]
        )
        self.play(FadeIn(librarian), FadeIn(book))
        self.wait(1)

        # Librarian Assigns a Nickname
        self.play(librarian.animate.move_to([-1, -1, 0]))
        text1 = Text("This title is too long!", font_size=24).move_to([-1, 1, 0])
        self.play(Write(text1))
        self.wait(2)
        self.play(FadeOut(text1))

        text2 = Text(
            "Assigning nickname 'Quantum Guide' to 'The Comprehensive Guide to Advanced Quantum Mechanics and Its Applications'",
            font_size=18
        ).move_to([0, 2, 0])
        self.play(Write(text2))
        self.wait(3)
        self.play(FadeOut(text2))

        # Nickname Appears
        nickname = Nickname("Quantum Guide", position=[2, 0, 0])
        arrow = Arrow(start=book.get_right(), end=nickname.get_left(), color=WHITE)
        self.play(FadeIn(nickname), GrowArrow(arrow))
        self.wait(2)

        # Librarian Refers to the Book Using the Nickname
        self.play(librarian.animate.move_to([3, -1, 0]))
        text3 = Text("Referring to book as 'Quantum Guide'", font_size=24).move_to([3, 1, 0])
        self.play(Write(text3))
        self.wait(2)

        # Simplification Highlight
        self.play(FadeOut(book), FadeOut(arrow))
        text4 = Text("Type aliases simplify complex types!", font_size=24).move_to([0, 3, 0])
        self.play(Write(text4))
        self.wait(3)
        self.play(FadeOut(text4), FadeOut(nickname), FadeOut(librarian))

        # Conclusion
        thanks = Text("Thanks for watching", font_size=48, color=WHITE)
        self.play(Write(thanks))
        self.wait(2)
        self.play(FadeOut(thanks))