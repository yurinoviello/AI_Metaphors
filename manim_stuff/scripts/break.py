import manimpango
manimpango.register_font('/home/ynoviello/Downloads/JetBrainsSans-Regular.ttf')
from manim import DARK_BROWN as BROWN
from manim import *

# Define the Person class
class Person(VGroup):
    def __init__(self, person_height=1.0, start_position=ORIGIN, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.person_height = person_height
        # Create the head
        self.head = Circle(radius=self.person_height * 0.3, color=color, fill_opacity=1)
        # Create the body
        self.body = Rectangle(width=self.person_height * 0.5, height=self.person_height, color=color, fill_opacity=1)
        self.body.next_to(self.head, DOWN, buff=0.1)
        # Add the head and body to the person
        self.add(self.head, self.body)
        self.move_to(start_position)

    def walk_to(self, target_position):
        return self.animate.move_to(target_position)

    def stop(self):
        return FadeOut(self)

    def collect_leaves(self, leaves):
        return [leaf.animate.move_to(self.get_center() + UP * 0.5) for leaf in leaves]

# Define the Tree class
class Tree(VGroup):
    def __init__(self, tree_height=1.0, position=ORIGIN, color=GREEN, **kwargs):
        super().__init__(**kwargs)
        self.tree_height = tree_height
        # Create the trunk
        trunk = Rectangle(
            width=self.tree_height * 0.2,
            height=self.tree_height,
            color=GRAY_BROWN,
            fill_opacity=1
        )
        trunk.shift(DOWN * self.tree_height / 2)
        # Create the foliage
        foliage = Triangle(
            color=color,
            fill_opacity=1
        )
        foliage.scale(self.tree_height)
        foliage.next_to(trunk, UP, buff=0)
        # Add trunk and foliage to the tree
        self.add(trunk, foliage)
        # Move the tree to the specified position
        self.move_to(position)

# Define the SpecificTree class
class SpecificTree(Tree):
    def __init__(self, **kwargs):
        super().__init__(color=YELLOW, **kwargs)

# Define the Forest class
class Forest(VGroup):
    def __init__(self, num_trees=10, tree_spacing=2.0, target_tree_index=5, **kwargs):
        super().__init__(**kwargs)
        self.trees = []
        for i in range(num_trees):
            position = LEFT * (num_trees / 2 - i) * tree_spacing
            if i == target_tree_index:
                tree = SpecificTree(position=position)
            else:
                tree = Tree(position=position)
            self.trees.append(tree)
            self.add(tree)

# Define the Leaf class
class Leaf(Circle):
    def __init__(self, position=ORIGIN, **kwargs):
        super().__init__(
            radius=0.1,
            color=GREEN,
            fill_opacity=1,
            **kwargs
        )
        self.move_to(position)

# Main animation class
class BreakStatementAnimation(Scene):
    def construct(self):
        # Title Screen
        title = Text("break", color=WHITE, font_size=72)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Scene Setup
        forest = Forest(num_trees=10, tree_spacing=2.0, target_tree_index=5)
        self.play(Create(forest))
        self.wait(1)

        # Introduce the Person
        person = Person(start_position=forest.trees[0].get_center() + DOWN * 0.5)
        self.play(FadeIn(person))
        self.wait(1)

        # Start the Search
        for i, tree in enumerate(forest.trees):
            # Walk to the tree
            self.play(person.walk_to(tree.get_center() + DOWN * 0.5))
            # Display "Is this the tree?"
            question_text = Text("Is this the tree?", color=WHITE, font_size=24).next_to(person, UP)
            self.play(Write(question_text))
            self.wait(1)
            self.play(FadeOut(question_text))

            # Check if it's the specific tree
            if isinstance(tree, SpecificTree):
                # Display "This is the one!"
                found_text = Text("This is the one!", color=WHITE, font_size=24).next_to(tree, UP)
                self.play(Write(found_text))
                self.wait(1)
                self.play(FadeOut(found_text))
                break
            else:
                # Display "Not the right tree."
                not_found_text = Text("Not the right tree.", color=WHITE, font_size=24).next_to(tree, UP)
                self.play(Write(not_found_text))
                self.wait(1)
                self.play(FadeOut(not_found_text))

        # Stop the Search
        stop_text = Text("No need to search further.", color=WHITE, font_size=24).next_to(person, UP)
        self.play(Write(stop_text))
        self.wait(1)
        self.play(FadeOut(stop_text))

        # Collect the Leaves
        leaves = [Leaf(position=forest.trees[5].get_center() + UP * 0.5 + RIGHT * i * 0.3) for i in range(3)]
        for leaf in leaves:
            self.add(leaf)
        collect_text = Text("Collecting the leaves.", color=WHITE, font_size=24).next_to(person, UP)
        self.play(Write(collect_text))
        self.wait(1)
        self.play(FadeOut(collect_text))
        self.play(*person.collect_leaves(leaves))
        self.wait(1)

        # End the Scene
        self.play(FadeOut(person), FadeOut(forest), *[FadeOut(leaf) for leaf in leaves])
        thanks_text = Text("Thanks for watching", color=WHITE, font_size=36)
        self.play(Write(thanks_text))
        self.wait(2)
        self.play(FadeOut(thanks_text))