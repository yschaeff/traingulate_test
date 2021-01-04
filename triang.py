#!/usr/bin/env python3

import tkinter as tk
from math import sqrt, pi, sin, cos, asin, acos

red = "#FF0000"
green = "#476042"
blue = "#0000FF"
black = "#000000"
white = "#FFFFFF"
colors = (green, red, blue, black, white)

class Point():
    R = 5
    def __init__(self, x, y, canvas):
        R = Point.R
        self.x = x
        self.y = y
        self.canvas = canvas
        self.create()
    def create(self):
        R = Point.R
        self.tkobj = self.canvas.create_oval(self.x-R, self.y-R, self.x+R, self.y+R, fill=green)
    def setcircle(self, circle):
        self.circle = circle
    def distance(self, x, y):
        return sqrt(pow(x-self.x, 2) + pow(y-self.y, 2))
    def destroy(self):
        self.canvas.delete(self.tkobj)
    def moveto(self, x, y):
        topleft = x-Point.R, y-Point.R
        self.canvas.moveto(self.tkobj, *topleft)
        self.x, self.y = x, y
        self.circle.update()

class Circle():
    def __init__(self, m, c, canvas):
        self.m = m
        self.c = c
        m.setcircle(self)
        c.setcircle(self)
        r = self.radius()
        x0, y0 = m.x-r, m.y-r
        x1, y1 = m.x+r, m.y+r
        self.canvas = canvas
        self.tkobj = self.canvas.create_oval(x0, y0, x1, y1, width=3)
        #self.create()
    def create(self):
        r = self.radius()
        x0, y0 = self.m.x-r, self.m.y-r
        x1, y1 = self.m.x+r, self.m.y+r
        self.tkobj = self.canvas.create_oval(x0, y0, x1, y1, width=3)
    def radius(self):
        return self.m.distance(self.c.x, self.c.y)
    def destroy(self):
        self.canvas.delete(self.tkobj)
    def update(self):
        r =  self.m.distance(self.c.x, self.c.y)
        x0, y0 = self.m.x-r, self.m.y-r
        x1, y1 = self.m.x+r, self.m.y+r
        self.canvas.coords(self.tkobj, x0,y0, x1,y1)

def distance(x, y, x1, y1):
    return sqrt(pow(x-x1, 2) + pow(y-y1, 2))

circles = []
handles = []
selected = None
selected_is_new = False

def press(event):
    global selected, selected_is_new
    x, y = event.x, event.y

    ## find out if handle nearby, if so select it.
    nearby = filter(lambda h: h.distance(x,y) < Point.R, handles)
    for handle in nearby:
        selected = handle
        selected_is_new = False
        break

    if not selected:
        m = Point(x, y, w)
        c = Point(x, y, w)
        handles.append(m)
        selected = c
        selected_is_new = True
        circle = Circle(m, c, w)
        circles.append(circle)

def drag(event):
    global selected
    x, y = event.x, event.y
    if not selected: return
    selected.moveto(x, y)
    plot(event)

def release(event):
    global selected, selected_is_new
    drag(event)
    if selected_is_new:
        handles.append(selected)
    selected = None

class Line:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
    def bisect(self):
        x0 = (self.p1[0] + self.p0[0])/2
        y0 = (self.p1[1] + self.p0[1])/2
        x1 = (self.p0[0] - x0) * cos(pi/2) - (self.p0[1] - y0) * sin(pi/2) + x0
        y1 = (self.p0[0] - x0) * sin(pi/2) + (self.p0[1] - y0) * cos(pi/2) + y0
        return Line((x0, y0), (x1, y1))
    def __str__(self):
        return f"({self.p0[0]},{self.p0[1]})({self.p1[0]},{self.p1[1]})"
    def intersect(self, L):
        #print(self, L)
        p0x = self.p0[0]
        p0y = self.p0[1]
        p1x = self.p1[0]
        p1y = self.p1[1]

        l0x = L.p0[0]
        l0y = L.p0[1]
        l1x = L.p1[0]
        l1y = L.p1[1]

        if (p1x == p0x): #special case with vertical line
            b = (l1y-l0y) / (l1x - l0x)
            x = p1x
            y = b * (x-l0x) + l0y
        elif (l1x == l0x): #special case with vertical line
            a = (p1y-p0y) / (p1x - p0x)
            x = l1x
            y = a * (x-p0x) + p0y
        else:
            a = (p1y-p0y) / (p1x - p0x)
            b = (l1y-l0y) / (l1x - l0x)

            x = (a*p0x - b*l0x - p0y + l0y) / (a - b)
            y = a * (x-p0x) + p0y
        return (x, y)

def sign(i):
    return i>=0

def plot2(x0, y0, x1, y1, r1, enum):
    #print(x0, y0, x1, y1, r1)
    # wat is de huidige hoek?
    #x = x0-x1
    #y = y0-y1
    #d = sqrt(pow(x, 2) + pow(y, 2))
    #x /= d
    #y /= d
    #if sign(x) == sign(y):
        #T = asin(x) # this is wrong only half the time...
    #else:
        #T = asin(-x) # this is wrong only half the time...


    F0 = x0, y0
    F1 = x1, y1
    #construct candidate line towards P
    points = []
    STEPS=100
    for step in range(STEPS):
        t = 0.1 + (step * 2 * pi) / STEPS
        #t = T - 0.5*pi + (step * pi) / STEPS


        #find V
        xv = sin(t) * r1 + x1
        yv = cos(t) * r1 + y1
        V = xv, yv
        L1 = Line(F1, V)
        L2 = Line(V, F0)
        B = L2.bisect()

        #if step == 300:
            #xxx = w.create_oval(xv-3, yv-3, xv+3, yv+3)
            #xxx = w.create_line(*F1, *V)
            #xxx = w.create_line(*V, *F0)
            #xxx = w.create_line(*B.p0, *B.p1)
        try:
            P = L1.intersect(B)
            d1 = distance(*P, *F0)
            d2 = distance(*P, *F1)

            if d1 < d2:
                points.append(P)
            #xxx = w.create_oval(P[0]-3, P[1]-3, P[0]+3, P[1]+3)
            #if step == 300:
                #xxx = w.create_line(*P, *B.p0)
                #xxx = w.create_line(*P, *V)
        except ZeroDivisionError:
            print("skip")
        #print(step, xv, yv)
    if len(points) > 1:
        P1 = points[0]
        for P2 in points[1:]:
            if distance(*P1, *P2) < 500:
                xxx = w.create_line(*P1, *P2, fill=colors[enum%len(colors)], width=2)
            P1 = P2

def plot_pair(C1, C2, enum):
    r1 = C1.radius()
    r2 = C2.radius()
    if r1 > r2:
        C1, C2 = C2, C1
        r1, r2 = r2, r1
    plot2(C1.m.x, C1.m.y, C2.m.x, C2.m.y, r2-r1, enum)


def plot(event):
    if len(circles) < 2: return
    w.delete("all")
    for h in handles:
        h.create()
    for c in circles:
        c.create()

    for i1 in range(len(circles)):
        for i2 in range(i1+1, len(circles)):
            C1 = circles[i1]
            C2 = circles[i2]
            plot_pair(C1, C2, i2)

    #C1 = circles[0]
    #C2 = circles[1]
    #plot_pair(C1, C2)



def move(e):
    pass

def delete(event):
    global selected
    if selected: return
    if not circles:
        w.delete("all")
        return
    c = circles.pop()
    c.destroy()
    h = handles.pop()
    h.destroy()
    h = handles.pop()
    h.destroy()

def list_obj(event):
    print(circles)
    print(handles)
    print(selected)
    print(selected_is_new)

master = tk.Tk()
w = tk.Canvas(master)
w.pack(expand = True, fill = tk.BOTH)
w.bind("<Motion>", move)
w.bind("<B1-Motion>", drag)
w.bind("<Button-1>", press)
w.bind("<ButtonRelease-1>", release)
w.bind_all("<Key-d>", delete)
w.bind_all("<Key-l>", list_obj)
w.bind_all("<Key-q>", exit)
w.bind_all("<Key-w>", plot)
print(dir(w))
tk.mainloop()
