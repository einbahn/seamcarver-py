import math
import sys
from itu.algs4.errors.errors import IllegalArgumentException
from itu.algs4.stdlib.color import Color
from itu.algs4.stdlib.picture import Picture
from collections import namedtuple

class SeamCarver:
    def __init__(self, picture: Picture):
        self._picture = picture
        self._energy = [[0 for c in range(self.width())] for r in range(self.height())]
        for row in range(self.height()):
            for col in range(self.width()):
                self._energy[row][col] = self.energy(col, row) 

    def picture(self):
        return self._picture

    def width(self):
        return self._picture.width()

    def height(self):
        return self._picture.height()

    def _calc_energy(self, color_a: Color, color_b: Color):
        return math.pow(color_a.getRed() - color_b.getRed(), 2) + math.pow(color_a.getBlue() - color_b.getBlue(), 2) + \
               math.pow(color_a.getGreen() - color_b.getGreen(), 2)

    def _validate_row_index(self, row):
        if row < 0 or row >= self.height():
            raise IllegalArgumentException()

    def _validate_column_index(self, col):
        if col < 0 or col >= self.width():
            raise IllegalArgumentException()

    def energy(self, x, y):
        try:
            self._validate_column_index(x - 1)
            self._validate_column_index(x + 1)
            self._validate_row_index(y - 1)
            self._validate_row_index(y + 1)
            return math.sqrt(self._calc_energy(self._picture.get(x - 1, y), self._picture.get(x + 1, y)) +
                             self._calc_energy(self._picture.get(x, y - 1), self._picture.get(x, y + 1)))
        except IllegalArgumentException:
            return 1000.0

    def find_vertical_seam(self):
        from pprint import pprint as pp
        Point = namedtuple("Point", ["col", "row"])
        def traverse_column(source):
            edge_to = dict()
            dist_to = dict()
            dist_to[source] = self._energy[source.row][source.col]
            edge_to[source] = None 
            def relax(from_p, to_p):
                weight = self._energy[to_p.row][to_p.col]
                prev_weight = dist_to[from_p]
                if dist_to[to_p] > prev_weight + weight:
                    dist_to[to_p] = prev_weight + weight
                    edge_to[to_p] = from_p 
            for row in range(self.height()):
                for col in range(self.width()):
                    dist_to[Point(col, row)] = math.inf
                    edge_to[Point(col, row)] = None

            ordered_p = []
            for n, row in enumerate(range(self.height()), 1):
                column_begin = source.col-n
                column_end = source.col+n
                for c in range(column_begin, column_end):
                    try:
                        self._validate_column_index(c)
                        ordered_p.append(Point(c, row))
                    except IllegalArgumentException:
                        pass
            dist_to[source] = self._energy[source.row][source.col]        
            for p in ordered_p:
                tpp = [
                    Point(p.col-1, p.row+1),
                    Point(p.col, p.row+1),
                    Point(p.col+1, p.row+1)
                ]
                for tp in tpp:
                    try:
                        self._validate_column_index(tp.col)
                        self._validate_row_index(tp.row)
                        relax(p, tp)
                    except IllegalArgumentException:
                        pass
            
            return edge_to, dist_to
        def last_row_min_weight(dist_to, edge_to):
            from collections import deque
            min_weight = math.inf
            min_point = None
            for c in range(self.width()):
                p = Point(c, self.height()-1)
                if dist_to[p] < min_weight:
                    min_weight = dist_to[p]
                    min_point = p
            seam = deque() 
            seam.appendleft(min_point)
            sp = edge_to[min_point]
            while sp is not None:
                seam.appendleft(sp)
                sp = edge_to[sp]
            return [p.col for p in seam], min_weight
        energy = math.inf 
        seam = None 
        for col in range(self.width()):
            e, d = traverse_column(Point(col, 0))
            s, total_energy = last_row_min_weight(d, e)
            if total_energy < energy:
                energy = total_energy
                seam = s
        print(seam)
        print("total energy: %.2f" % energy)

if __name__ == '__main__':
    pic = Picture(sys.argv[1])
    sc = SeamCarver(pic)
    sc.find_vertical_seam()
