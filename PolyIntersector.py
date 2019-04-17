import tkinter as tk

class Window:
    def __init__(self, in_dimension):
        self._root = tk.Tk()
        self._dimension = in_dimension
        self._origin = self._dimension/2
        self.canvas = tk.Canvas(self._root, width = self._dimension, height = self._dimension, bg = 'grey')
        self.canvas.grid()

    def drawPolys(self, poly_list):
        abs_list = []
        
        for poly in poly_list:
            for point in poly.points:
                abs_list.append((abs(point[0]), abs(point[1])))
        
        extreme_x = max(abs_list, key = lambda p: p[0])[0]
        extreme_y = max(abs_list, key = lambda p: p[1])[1]

        if extreme_x > extreme_y:
            extreme_val = extreme_x
        else:
            extreme_val = extreme_y
        
        scale = (self._dimension / 2) / extreme_val

        def world_to_screen(point):
            return (point[0]*scale + self._origin, point[1]*(-scale) + self._origin)

        for poly in poly_list:
            screen_poly = []
            for point in poly.points:
                screen_poly.append(world_to_screen(point))
            print(screen_poly)
            self.canvas.create_polygon(screen_poly, activefill = poly.color)

    def show(self):
        self._root.mainloop()

class Polygon:
    def __init__(self, in_points, in_color):
        self.points = in_points
        self.color = in_color

def segmentIntersection(seg1, seg2):
    pass

def signedArea(a, b, c):
    area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

    if area > 0:
        return 1
    elif area < 0:
        return -1
    else:
        return 0

def polyIntersection(poly1, poly2):
    n = len(poly1)
    m = len(poly2)
    a = 0
    b = 0



def main():
    window = Window(600)
    poly1 = Polygon([(0,0), (3,3),(3,-3)], 'red')
    poly2 = Polygon([(-2,2),(2,2),(2,-2),(-2,-2)], 'blue')
    #test = Polygon
    #poly1.draw(window)
    #poly2.draw(window)
    window.drawPolys([poly2, poly1])
    window.show()

if __name__=="__main__":
    main()
