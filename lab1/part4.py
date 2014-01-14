from math import sqrt, acos, pi
from part3 import Math

class MathSubClass(Math):

    def hyp(self, a, b):
        return sqrt(pow(a, 2) + pow(b, 2))

    def theta(self, a, b, c):
        """theta(a,b,c) -> (<A, <B, <C)"""
        # Compute in rad
        angleA = (pow(b, 2) + pow(c, 2) - pow(a, 2)) / (2 * b * c)
        angleB = (pow(c, 2) + pow(a, 2) - pow(b, 2)) / (2 * c * a)
        # Convert to deg
        angleA = 180 * acos(angleA) / pi
        angleB = 180 * acos(angleB) / pi

        return (angleA, angleB, (180.0 - angleA - angleB))
