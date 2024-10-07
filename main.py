import turtle
import random

# Set up the screen
wn = turtle.Screen()
wn.title("Breakout Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -230)
ball.dx = 0.75  # Initial ball speed in the x direction
ball.dy = 0.75  # Initial ball speed in the y direction
ball_speed_increment = 0.05  # Speed increment after each paddle hit

# Bricks
bricks = []

# Create a grid of bricks
rows = 5
cols = 10  # Increased the number of columns to fit the screen better
brick_width = 75
brick_height = 30
brick_padding = 10
x_offset = -360  # Adjust the offset to center the bricks horizontally
y_offset = 250

for row in range(rows):
    for col in range(cols):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(random.choice(["blue", "green", "yellow", "orange", "purple"]))
        brick.shapesize(stretch_wid=1.5, stretch_len=3.5)
        brick.penup()
        x = x_offset + (col * (brick_width + brick_padding))
        y = y_offset - (row * (brick_height + brick_padding))
        brick.goto(x, y)
        bricks.append(brick)

# Score
score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Lives
lives = 3
pen_lives = turtle.Turtle()
pen_lives.speed(0)
pen_lives.color("white")
pen_lives.penup()
pen_lives.hideturtle()
pen_lives.goto(-300, 260)
pen_lives.write(f"Lives: {lives}", align="center", font=("Courier", 24, "normal"))


# Paddle movement
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        x += 50
    paddle.setx(x)


def paddle_left():
    x = paddle.xcor()
    if x > -350:
        x -= 50
    paddle.setx(x)


# Keyboard bindings
wn.listen()
wn.onkeypress(paddle_right, "Right")
wn.onkeypress(paddle_left, "Left")

# Game loop
try:
    while True:
        wn.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border collision detection (left and right walls)
        if ball.xcor() > 390:
            ball.setx(390)
            ball.dx *= -1

        if ball.xcor() < -390:
            ball.setx(-390)
            ball.dx *= -1

        # Top wall
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        # Bottom wall - Lose a life
        if ball.ycor() < -290:
            ball.goto(0, -230)
            ball.dy = 0.75  # Reset speed when life is lost
            ball.dx = 0.75
            lives -= 1
            pen_lives.clear()
            pen_lives.write(f"Lives: {lives}", align="center", font=("Courier", 24, "normal"))
            if lives == 0:
                pen.clear()
                pen.write("Game Over", align="center", font=("Courier", 36, "normal"))
                break

        # Paddle collision detection
        if (ball.ycor() > -240 and ball.ycor() < -230) and (
                ball.xcor() > paddle.xcor() - 50 and ball.xcor() < paddle.xcor() + 50):
            ball.sety(-230)
            ball.dy *= -1

            # Gradually increase ball speed after hitting paddle
            ball.dx += ball.dx * ball_speed_increment
            ball.dy += ball.dy * ball_speed_increment

        # Brick collision detection
        for brick in bricks:
            if (ball.ycor() > brick.ycor() - 20 and ball.ycor() < brick.ycor() + 20) and (
                    ball.xcor() > brick.xcor() - 40 and ball.xcor() < brick.xcor() + 40):
                ball.dy *= -1
                brick.goto(1000, 1000)  # Move the brick off-screen
                bricks.remove(brick)  # Remove the brick from the list
                score += 10
                pen.clear()
                pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
                break  # Exit loop after one brick collision to avoid multiple collisions in one frame

        # Win condition (all bricks destroyed)
        if len(bricks) == 0:
            pen.clear()
            pen.write("You Win!", align="center", font=("Courier", 36, "normal"))
            break

except turtle.Terminator:
    print("Game closed prematurely")

# Ensure the window stays open
turtle.done()
