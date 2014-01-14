from math import pi, pow
from sys import exit


class Math(object):

    def __init__(self):
        self.funcs = {
            1: self.perim_rect,  2: self.perim_circle,  3: self.area_rect,
            4: self.area_circle, 5: self.area_cube,     6: self.area_cylinder,
            7: self.area_trap,   8: self.usage_str,     9: exit
        }

    def perim_rect(self, l, w):
        return (2 * l) + (2 * w)

    def perim_circle(self, r):
        return 2 * pi * r

    def area_rect(self, l, w):
        return l * w

    def area_circle(self, r):
        return pi * pow(r, 2)

    def area_cube(self, a):
        return 6 * pow(a, 2)

    def area_cylinder(self, r, h):
        return (2 * pi * pow(r, 2)) + (2 * pi * r * h)

    def area_trap(self, b1, b2, h):
        return ((b1 + b2) * h) / 2

    def usage_str(self):
        return """Usage:

Enter a method number, followed by the arguments.
Single line, space seperated.

Methods:
    1. perim_rect(l, w)
    2. perim_circle(r)
    3. area_rect(l, w)
    4. area_circle(r)
    5. area_cube(a)
    6. area_cylinder(r, h)
    7. area_trap(b1, b2, h)
    8. Print this message again
    9. Quit
"""


if __name__ == '__main__':
    m = Math()

    print(m.usage_str())

    while True:
        # Get user input
        user_input = input('> ').rstrip()
        cmd, *args = user_input.split(' ')

        # Convert input to ints
        try:
            cmd = int(cmd)
            args = [int(arg) for arg in args]
        except ValueError as e:
            print('Error: {}'.format(e))
            continue

        # Attempt to call the function.
        try:
            print('Result: {}'.format(m.funcs[cmd](*args)))
        except KeyError:
            print('Invalid option: {}'.format(cmd))
        except TypeError as e:
            print('Bad argument count: {}'.format(e))
