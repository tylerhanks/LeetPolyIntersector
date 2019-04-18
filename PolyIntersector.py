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
    a = seg1[0]
    b = seg1[1]
    c = seg2[0]
    d = seg2[1]

    code = '?'

    denom = a[0] * (d[1] - c[1]) + b[0] * (c[1] - d[1]) + d[0] * (b[1] - a[1]) + c[0] * (a[1] - b[1])
    #denom = float(denom)

    if denom is 0:
        print("error divide by 0")
        return 0
    
    num = a[0] * (d[1] - c[1]) + c[0] * (a[1] - d[1]) + d[0] * (c[1] - a[1])
    float(num)
    if (num is 0.0) or (num is denom):
        code = 'v'
    s = num / denom
    num = -	(a[0] * (c[1] - b[1]) + b[0] * (a[1] - c[1]) + c[0] * (b[1] - a[1]))
    num = float(num)

    if (num is 0.0) or (num is denom):
        code = 'v'
    t = num / denom

    if 0.0 < s and s < 1.0 and 0.0 < t and t < 1.0:
        code = '1'
    elif 0.0 > s or s > 1.0 or 0.0 > t or t > 1.0:
        code = '0'
    
    x = a[0] + s * (b[0] - a[0])
    y = a[1] + t * (b[1] - a[1])

    return (code, (x,y))

def leftOf(a, b, c):
    area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

    if area > 0:
        return 1
    elif area < 0:
        return -1
    else:
        return 0

def pointSub(point1, point2):
    return (point2[0] - point1[0], point2[1], point1[1])

def InOut(inflag, aHB, bHA):
    if (aHB > 0):
        return "Pin"
    elif (bHA > 0):
        return "Qin"
    else:
        return inflag

def polyIntersection(P, Q):
    n = len(P)
    m = len(Q)
    a = 0
    b = 0
    aa = 0
    ba = 0
    FirstPoint = True
    inFlag = "Unknown"
    result = []

    a1 = (a + n -1) % n
    b1 = (b + m -1) % m

    A = pointSub(P[a], P[a1])
    B = pointSub(Q[b], Q[b1])

    cross = leftOf((0,0), A, B)
    aHB = leftOf(Q[b1], Q[b], P[a])
    bHA = leftOf(P[a1], P[a], Q[b])

    res = segmentIntersection([P[a1], P[a]], [Q[b1], Q[b]])
    code = res[0]
    p = res[1]

    if code is '1' or code is 'v':
        if inFlag is "Unknown" and FirstPoint:
            aa = ba = 0
            FirstPoint = False
            result.append((p[0], p[1]))
        result.append(p)
        inFlag = InOut(inFlag, aHB, bHA)

    elif cross >= 0:
        def Advance(a, aa, n, inside, v):
            if inside:
                result.append(v)
            return (aa+1, (a+1) % n)
        if bHA > 0:
            r = Advance(a, aa, n, inFlag is "Pin", P[a])
            aa = r[0]
            a = r[1]
        else:
            r = Advance(b, ba, m, inFlag is "Qin", Q[b])
            ba = r[0]
            b = r[1]
    else:
        if aHB > 0:
            r = Advance(b, ba, m, inFlag is "Qin", Q[b])
            ba = r[0]
            b = r[1]
        else:
            r = Advance(a, aa, n, inFlag is "Pin", P[a])
            aa = r[0]
            a = r[1]
    
    while((aa < n or ba < m) and (aa < 2 * n and ba < 2 * m)):
        a1 = (a + n -1) % n
        b1 = (b + m -1) % m

        A = pointSub(P[a], P[a1])
        B = pointSub(Q[b], Q[b1])

        cross = leftOf((0,0), A, B)
        aHB = leftOf(Q[b1], Q[b], P[a])
        bHA = leftOf(P[a1], P[a], Q[b])

        res = segmentIntersection([P[a1], P[a]], [Q[b1], Q[b]])
        code = res[0]
        p = res[1]

        if code is '1' or code is 'v':
            if inFlag is "Unknown" and FirstPoint:
                aa = ba = 0
                FirstPoint = False
                result.append((p[0], p[1]))
            result.append(p)
            inFlag = InOut(inFlag, aHB, bHA)

        elif cross >= 0:
            def Advance(a, aa, n, inside, v):
                if inside:
                    result.append(v)
                return (aa+1, (a+1) % n)
            if bHA > 0:
                r = Advance(a, aa, n, inFlag is "Pin", P[a])
                aa = r[0]
                a = r[1]
            else:
                r = Advance(b, ba, m, inFlag is "Qin", Q[b])
                ba = r[0]
                b = r[1]
        else:
            if aHB > 0:
                r = Advance(b, ba, m, inFlag is "Qin", Q[b])
                ba = r[0]
                b = r[1]
            else:
                r = Advance(a, aa, n, inFlag is "Pin", P[a])
                aa = r[0]
                a = r[1]
    
    if inFlag is "Unknown":
        print("FUCK")  

    return result
   

def main():
    window = Window(600)

    #poly1 = Polygon([(0,16),(5,8),(13,0),(19,2),(24,10),(24,26),(19,29),(13,32),(7,32),(3,29),(0,16)], 'blue')
    #poly2 = Polygon([(28,16),(16,32),(0,22),(3,10),(16,-3),(28,16)], 'red')

    poly1 = Polygon([(0,0), (5,0), (5,5)],'blue')
    poly2 = Polygon([(1,-1),(3,-1),(3,3),(1,3)],'red')

    print("Init")

    intersection = polyIntersection(poly1.points, poly2.points)
    poly3 = Polygon(intersection, 'purple')

    print("Didn't diverge")

    window.drawPolys([poly3, poly2, poly1])
    #test = Polygon
    #poly1.draw(window)
    #poly2.draw(window)

    #print(signedArea((0,0),(1,1),(1,0)))
    #window.drawPolys([poly2, poly1])
    window.show()

if __name__=="__main__":
    main()
