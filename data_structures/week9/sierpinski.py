# ---------------------------------------------------------------
#                        Homework 5?
# ---------------------------------------------------------------
# Take a moment to familiarize yourself with visualize.py
# Especially, Point, which is a tuple, and draw_triangle 
# There are a couple functions to write here. 
#       - midpoint takes two points and returns their midpoint
#       - sierpinski takes a triangle and  recursively draws 
#         three smaller triangles at the corners of the larger
#         triangle
# 

import sys
from math import sqrt
 
from visualize import Point, clear, show, draw_triangle, save
 
 
def midpoint(p: Point, q: Point) -> Point:
    """Return the midpoint of the segment between p and q."""
 

 
def sierpinski(a: Point, b: Point, c: Point, depth: int) -> None:
    """
    Recursively draw a Sierpinski triangle with corners a, b, c.
 
    Base case:      depth == 0 -> outline the triangle with draw_triangle().
    Recursive case: find the midpoints of the three sides and recurse on
                    the three corner triangles: the bottom-left triangle,
                    the bottom-right triangle, and the top corner triangle,
                    with depth - 1.
    """
 
 
if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 5
 
    side = 1.0
    a = (0.0, 0.0)
    b = (side, 0.0)
    c = (side / 2, side * sqrt(3) / 2)
 
    clear()
    sierpinski(a, b, c, depth)
    show(f"Sierpinski triangle, depth {depth}")
    save(f"Sierpinski triangle, depth {depth}", f"triangle_{depth}.png")
