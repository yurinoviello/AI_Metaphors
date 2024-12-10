from manim import DARK_BROWN as BROWN
from manim import *

# Define the TrafficOfficer class
class TrafficOfficer(VGroup):
    def __init__(self, officer_height=1.0, position=ORIGIN, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.officer_height = officer_height
        # Create the head
        self.head = Circle(radius=self.officer_height * 0.3, color=color, fill_opacity=1)
        # Create the body
        self.body = Rectangle(width=self.officer_height * 0.5, height=self.officer_height, color=color, fill_opacity=1)
        self.body.next_to(self.head, DOWN, buff=0.1)
        # Add head and body to the officer
        self.add(self.head, self.body)
        # Position the officer
        self.move_to(position)

    def direct_north(self):
        return Text("Go Straight", color=GREEN).next_to(self, UP, buff=0.5)

    def direct_else(self):
        return Text("Take Another Route", color=RED).next_to(self, UP, buff=0.5)

# Define the Car class
class Car(VGroup):
    def __init__(self, car_length=1.0, position=ORIGIN, color=YELLOW, **kwargs):
        super().__init__(**kwargs)
        self.car_length = car_length
        # Create the body of the car
        self.body = Rectangle(width=self.car_length * 1.5, height=self.car_length * 0.7, color=color, fill_opacity=1)
        # Create the wheels
        self.wheel1 = Circle(radius=self.car_length * 0.2, color=BLACK, fill_opacity=1)
        self.wheel2 = Circle(radius=self.car_length * 0.2, color=BLACK, fill_opacity=1)
        self.wheel1.next_to(self.body, DOWN, buff=0.1).shift(LEFT * self.car_length * 0.5)
        self.wheel2.next_to(self.body, DOWN, buff=0.1).shift(RIGHT * self.car_length * 0.5)
        # Add body and wheels to the car
        self.add(self.body, self.wheel1, self.wheel2)
        # Position the car
        self.move_to(position)

    def move_straight(self):
        return self.animate.shift(UP * 2)

    def take_alternate_route(self):
        return self.animate.shift(RIGHT * 2)

# Define the Intersection class
class Intersection(VGroup):
    def __init__(self, size=3.0, **kwargs):
        super().__init__(**kwargs)
        # Create the vertical road
        self.vertical_road = Rectangle(width=size * 0.3, height=size, color=GRAY, fill_opacity=1)
        # Create the horizontal road
        self.horizontal_road = Rectangle(width=size, height=size * 0.3, color=GRAY, fill_opacity=1)
        # Add roads to the intersection
        self.add(self.vertical_road, self.horizontal_road)
        self.horizontal_road.rotate(PI / 2)

# Define the animation scene
class ElseBranchScene(Scene):
    def construct(self):
        # Step 1: Display the title
        title = Text("Else Branch", color=WHITE).scale(1.5)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Step 2: Set the scene
        intersection = Intersection(size=3.0)
        self.play(Create(intersection))
        traffic_officer = TrafficOfficer(position=UP * 0.5)
        self.play(FadeIn(traffic_officer))

        # Step 3: Introduce the Traffic Officer
        officer_text = Text("I decide where cars go!", color=WHITE).scale(0.5).next_to(traffic_officer, UP, buff=0.5)
        self.play(Write(officer_text))
        self.wait(2)
        self.play(FadeOut(officer_text))

        # Step 4: Introduce the first car (North Direction)
        car_north = Car(position=DOWN * 2)
        self.play(FadeIn(car_north))
        north_text = Text("Coming from the north?", color=WHITE).scale(0.5).next_to(traffic_officer, UP, buff=0.5)
        self.play(Write(north_text))
        self.wait(2)
        self.play(FadeOut(north_text))

        # Step 5: Traffic Officer directs the car (North)
        go_straight_text = traffic_officer.direct_north()
        self.play(Write(go_straight_text))
        self.play(car_north.move_straight())
        self.play(FadeOut(go_straight_text))

        # Step 6: Introduce the second car (Else Condition)
        car_else = Car(position=LEFT * 2, color=BLUE)
        self.play(FadeIn(car_else))
        else_text = Text("Not from the north?", color=WHITE).scale(0.5).next_to(traffic_officer, UP, buff=0.5)
        self.play(Write(else_text))
        self.wait(2)
        self.play(FadeOut(else_text))

        # Step 7: Traffic Officer directs the car (Else)
        take_route_text = traffic_officer.direct_else()
        self.play(Write(take_route_text))
        self.play(car_else.take_alternate_route())
        self.play(FadeOut(take_route_text))

        # Step 8: Summarize the concept
        summary_text = Text("If not north, then else!", color=WHITE).scale(0.7).to_edge(UP)
        self.play(Write(summary_text))
        self.wait(2)
        self.play(FadeOut(summary_text))

        # Step 9: Clear the scene
        self.play(FadeOut(traffic_officer), FadeOut(intersection), FadeOut(car_north), FadeOut(car_else))

        # Step 10: End with a thank you message
        thank_you = Text("Thanks for watching", color=WHITE).scale(1.2)
        self.play(Write(thank_you))
        self.wait(2)
        self.play(FadeOut(thank_you))