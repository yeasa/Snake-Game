from turtle import Screen, Turtle
import time
import random

"""....SNAKE class starts here..."""
"""by calling this class object it create the 3block snake  and can keep moving by calling move() method."""
coordinates = [(0, 0), (-20, 0), (-40, 0)]
up = 90
down = 270
left = 180
right = 0


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.initial_length = 3

    def create_snake(self):
        for cord in coordinates:
            """create new segments"""
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(cord)
            self.segments.append(new_segment)

    def add_segment(self):
        # increase in length after eating food
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        x = self.segments[self.initial_length - 1].xcor() + 20
        y = self.segments[self.initial_length - 1].ycor()
        self.initial_length += 1
        new_segment.goto(x=x, y=y)
        self.segments.append(new_segment)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            """move by following the head(tracing)"""
            new_x = self.segments[i - 1].xcor()
            new_y = self.segments[i - 1].ycor()
            self.segments[i].goto(new_x, new_y)
        self.head.forward(20)

    def up(self):
        if self.head.heading() != down:
            self.head.setheading(up)
        # if is to fix bug== snake cannot trace back/ move backwards"""

    def down(self):
        if self.head.heading() != up:
            self.head.setheading(down)

    def left(self):
        if self.head.heading() != right:
            self.head.setheading(left)

    def right(self):
        if self.head.heading() != left:
            self.head.setheading(right)

    def restart(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]
        self.initial_length = 3


"""Snake class ends here"""

"""FOOD CLASS STARTS HERE"""


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("blue")
        self.speed("fastest")
        self.new_food()

    def new_food(self):
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.goto(x=x, y=y)


"""food class ends here"""

"""SCORE CLASS STARTS HERE"""


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt", mode="r") as highest:
            self.high_score = int(highest.read())
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 270)
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(f"score = {self.score} High Score = {self.high_score}", align="center",
                   font=("Courier", 20, "normal"))

    def score_update(self):
        self.score += 1
        self.write_score()

    def restart(self):
        self.high_score = max(self.high_score, self.score)
        with open("data.txt", mode="w") as highest:
            highest.write(f"{self.high_score}")
        self.score = 0
        self.write_score()

    # def gameover(self):
    #     self.goto(x=0, y=0)
    #     self.write("GameOver",  align="center", font=("Courier", 15, "normal"))


"""score class ends here"""

""""......MAIN STARTS FROM HERE....."""

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)
snake = Snake()
food = Food()
score = Score()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.2)
    snake.move()

    # detect collision with food
    if snake.head.distance(food) < 15:
        snake.add_segment()
        food.new_food()
        score.score_update()

    # detect collision with wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        snake.restart()
        score.restart()

    # detect coollision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            score.restart()
            snake.restart()

screen.exitonclick()
