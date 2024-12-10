from manim import DARK_BROWN as BROWN
from manim import *
import random

# Define the Card class
class Card(VGroup):
    def __init__(self, label="", card_width=1.0, card_height=1.5, **kwargs):
        super().__init__(**kwargs)
        # Create the card rectangle
        self.card = Rectangle(
            width=card_width,
            height=card_height,
            color=WHITE,
            fill_color=BLUE_E,
            fill_opacity=1
        )
        # Create the label for the card
        self.label = Text(label, font_size=24, color=WHITE)
        self.label.move_to(self.card.get_center())
        # Add the card and label to the group
        self.add(self.card, self.label)

# Define the Deck class
class Deck(VGroup):
    def __init__(self, num_cards=10, card_spacing=0.5, **kwargs):
        super().__init__(**kwargs)
        self.cards = []
        for i in range(num_cards):
            card = Card(label=str(i + 1))
            card.move_to(RIGHT * i * card_spacing)
            self.cards.append(card)
            self.add(card)

    def shuffle(self):
        random.shuffle(self.cards)
        for i, card in enumerate(self.cards):
            card.move_to(RIGHT * i * 0.5)
        return self

# Define the Shuffler class
class Shuffler:
    @staticmethod
    def shuffle(deck):
        random.shuffle(deck.cards)
        for i, card in enumerate(deck.cards):
            card.move_to(RIGHT * i * 1.0)
        return deck

# Define the animation scene
class ShuffledFunctionAnimation(Scene):
    def construct(self):
        # Title Screen
        title = Text("shuffled", font_size=72, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Introduce the Deck
        deck = Deck(num_cards=10)
        deck.move_to(ORIGIN + DOWN * 1)
        self.play(Create(deck))
        
        # Explain the Deck
        deck_text = Text("This is a deck of cards.", font_size=36, color=WHITE).move_to(UP * 2)
        self.play(Write(deck_text))
        self.wait(3)
        self.play(FadeOut(deck_text))

        # Highlight the Cards
        card_text = Text("Each card represents an item in a list.", font_size=36, color=WHITE).move_to(UP * 2)
        self.play(Write(card_text))
        self.wait(3)
        self.play(FadeOut(card_text))

        # Introduce the Shuffler
        shuffle_text = Text("Let's shuffle the deck!", font_size=36, color=WHITE).move_to(UP * 2)
        self.play(Write(shuffle_text))
        self.wait(2)
        self.play(FadeOut(shuffle_text))

        # Shuffle the Deck
        self.play(*[card.animate.move_to(RIGHT * i * 1.0) for i, card in enumerate(random.sample(deck.cards, len(deck.cards)))])
        self.wait(1)

        # Explain the Shuffle
        shuffle_explanation = Text("The cards are now in a random order.", font_size=36, color=WHITE).move_to(UP * 2)
        self.play(Write(shuffle_explanation))
        self.wait(3)
        self.play(FadeOut(shuffle_explanation))

        # Reinforce the Metaphor
        metaphor_text = Text("The `shuffled` function works just like this!", font_size=36, color=WHITE).move_to(UP * 2)
        self.play(Write(metaphor_text))
        self.wait(3)
        self.play(FadeOut(metaphor_text))

        # Clear the Scene
        self.play(FadeOut(deck))

        # Closing Message
        closing_message = Text("Thanks for watching", font_size=48, color=WHITE)
        self.play(Write(closing_message))
        self.wait(2)
        self.play(FadeOut(closing_message))