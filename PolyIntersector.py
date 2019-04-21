import tkinter as tk
import pdb

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
            #print(screen_poly)
            self.canvas.create_polygon(screen_poly, activefill = poly.color)

    def show(self):
        self._root.mainloop()

class Polygon:
    def __init__(self, in_points, in_color):
        self.points = in_points
        self.color = in_color

def ConvPolyIntersection(poly1, poly2):
    """Computes the intersection of poly1 and poly2"""
    #helper function definitions:
    def vectorSub(v1, v2):
        """Computes v1 - v2"""
        return (v1[0] - v2[0], v1[1] - v2[1])
    def vectorPlus(v1, v2):
        """Computes v1 + v2"""
        return (v1[0] + v2[0], v1[1] + v2[1])
    def scalarMult(s, v):
        """Computes scalar s multiplied by vector v"""
        return (s*v[0], s*v[1])
    def vectorCross(v1, v2):
        """Computes the cross product of 2D vectors v1 and v2"""
        return (v1[0] * v2[1] - v1[1] * v2[0])
    def leftOf(a, b, c):
        """Determines if point c is to the left of line ab"""
        area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
        if area > 0:
            return 1
        elif area < 0:
            return -1
        else:
            return 0
    def segmentIntersection(p, p1, q, q1):
        """Computes the intersection of pp1 and qq1. Returns () if no intersection. Does not handle degenerate cases"""
        #pdb.set_trace()
        r = vectorSub(p1, p) #pp1 = p + tr
        s = vectorSub(q1, q) #qq1 = q + us

        if vectorCross(r, s) == 0:
            #print("Error: Degenerate segment intersection 0.")
            return ()
        
        denom = float(vectorCross(r,s))
        t = vectorCross(vectorSub(q,p), s) / denom #t = (q-p)*s/(r*s)
        u = vectorCross(vectorSub(q,p), r) / denom #u = (q-p)*r/(r*s)

        if (0.0 <= t <= 1.0) and (0.0 <= u <= 1.0):
            return vectorPlus(p, scalarMult(t, r)) #p + tr
        else:
            #print("Error: Degenerate segment intersection 1.")
            return ()
    def isInHalfPlane(p, q1, q2): #note these may need to be flipped
        """Checks if p is in the half plane of q1q2"""
        r = leftOf(q1,q2,p)
        if r == 1:
            return True
        else:
            return False

    #variable definitions
    P = poly1.points
    Q = poly2.points
    n = len(P)
    m = len(Q)
    p_index = 0
    q_index = 0
    inside = None
    firstIntersectFlag = True #flag indicating whether this is the first intersection
    firstIntersect = ()
    result = []

    #main loop
    for i in range(0, 2*(n+m)+1): #repeat no more that 2(|P|+|Q|) times
        #pdb.set_trace()
        p = P[p_index]
        p_1 = P[(p_index + n - 1) % n] #p_1 is the vertex before p

        q = Q[q_index]
        q_1 = Q[(q_index + m - 1) % m] #q_1 is the vertex before q

        intersection = segmentIntersection(p_1, p, q_1, q) #note these may need to be flipped
        if intersection != (): #if the two segments intersect
            if firstIntersectFlag:
                firstIntersect = intersection
                firstIntersectFlag = False
                result.append(intersection)
                if isInHalfPlane(p, q_1, q):
                    inside = "P"
                else:
                    inside = "Q"
            elif intersection == firstIntersect: #we are done
                return Polygon(result, 'purple')
            else:
                result.append(intersection)
                if isInHalfPlane(p, q_1, q):
                    inside = "P"
                else:
                    inside = "Q"
        
        #advance one of the edges
        if vectorCross(vectorSub(q, q_1), vectorSub(p, p_1)) >= 0:
            if isInHalfPlane(p, q_1, q):
                #advance(q)
                if inside == "Q":
                    result.append(q)
                q_index = (q_index + 1) % m
            else:
                #advance(p)
                if inside == "P":
                    result.append(p)
                p_index = (p_index + 1) % n
        else:
            if isInHalfPlane(q, p_1, p):
                #advance(p)
                if inside == "P":
                    result.append(p)
                p_index = (p_index + 1) % n
            else:
                #advance(q)
                if inside == "Q":
                    result.append(q)
                q_index = (q_index + 1) % m

    #there was no intersection or a degenerate case
    return Polygon([], "purple")

def main():
    window = Window(600)

    #poly1 = Polygon([(0,16),(5,8),(13,0),(19,2),(24,10),(24,26),(19,29),(13,32),(7,32),(3,29),(0,16)], 'blue')
    #poly2 = Polygon([(28,16),(16,32),(0,22),(3,10),(16,-3),(28,16)], 'red')

    #poly1 = Polygon([(0.0,0.0), (5.0,0.0), (5.0,5.0)],'blue')
    #poly2 = Polygon([(1.0,-1.0),(4.0,-.5),(3.0,8.0),(2.0,6.0)],'red')

    poly1 = Polygon([(0.0,0.0), (5.0,0.0), (5.0,5.0)],'blue')
    poly2 = Polygon([(1.0,-1.0),(4.0,-.5),(4.25,2),(3.0,8.0),(2.0,6.0)],'red')

    #poly1 = Polygon([(0,0),(3,0),(3,3),(0,3)], 'red')
    #poly2 = Polygon([(2,1),(4,1),(4,4),(2,4)], 'blue')
    poly3 = ConvPolyIntersection(poly1, poly2)

    if poly3.points != []:
        window.drawPolys([poly1, poly2, poly3])
        print(poly3.points)
    else:
        window.drawPolys([poly1, poly2])

    window.show()

if __name__=="__main__":
    main()
