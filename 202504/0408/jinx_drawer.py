import turtle
import random
import math

def setup_screen():
    """设置画布"""
    screen = turtle.Screen()
    screen.title("金克斯卡通画")
    screen.bgcolor("white")
    screen.setup(800, 800)
    return screen

def create_turtle():
    """创建并设置画笔"""
    t = turtle.Turtle()
    t.speed(0)  # 最快速度
    t.hideturtle()  # 隐藏画笔
    return t

def draw_circle(t, x, y, radius, color):
    """画圆"""
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()
    t.penup()

def draw_face(t):
    """画脸"""
    # 脸
    draw_circle(t, 0, 0, 100, "#FFE4E1")
    
    # 眼睛
    draw_circle(t, -30, 20, 15, "white")
    draw_circle(t, 30, 20, 15, "white")
    draw_circle(t, -30, 20, 8, "black")
    draw_circle(t, 30, 20, 8, "black")
    
    # 腮红
    draw_circle(t, -40, -10, 10, "#FFB6C1")
    draw_circle(t, 40, -10, 10, "#FFB6C1")

def draw_hair(t):
    """画头发"""
    t.penup()
    t.goto(-100, 0)
    t.pendown()
    t.setheading(0)
    t.fillcolor("#FF69B4")
    t.begin_fill()
    
    # 左头发
    t.forward(200)
    t.right(90)
    t.forward(150)
    t.right(90)
    t.forward(200)
    t.right(90)
    t.forward(150)
    t.end_fill()
    
    # 右头发
    t.penup()
    t.goto(100, 0)
    t.pendown()
    t.setheading(180)
    t.fillcolor("#FF69B4")
    t.begin_fill()
    t.forward(200)
    t.left(90)
    t.forward(150)
    t.left(90)
    t.forward(200)
    t.left(90)
    t.forward(150)
    t.end_fill()

def draw_mouth(t):
    """画嘴巴"""
    t.penup()
    t.goto(-20, -20)
    t.pendown()
    t.setheading(-60)
    t.circle(30, 120)
    t.setheading(60)
    t.circle(30, 120)

def draw_weapon(t):
    """画武器"""
    # 鱼骨头
    t.penup()
    t.goto(120, 0)
    t.pendown()
    t.setheading(45)
    t.fillcolor("#FFD700")
    t.begin_fill()
    for _ in range(4):
        t.forward(50)
        t.right(90)
    t.end_fill()

def main():
    screen = setup_screen()
    t = create_turtle()
    
    # 绘制各个部分
    draw_hair(t)
    draw_face(t)
    draw_mouth(t)
    draw_weapon(t)
    
    # 添加文字
    t.penup()
    t.goto(0, -150)
    t.color("black")
    t.write("金克斯", align="center", font=("Arial", 20, "bold"))
    
    screen.mainloop()

if __name__ == "__main__":
    main() 