import sys

from plotter import Plotter

from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, category=None):
        if category == "Outside":
            plt.plot(x, y, "ro", label='Outside')
        elif category == "Boundary":
            plt.plot(x, y, "bo", label='Boundary')
        elif category == "Inside":
            plt.plot(x, y, "go", label='Inside')
        else:
            plt.plot(x, y, "ko", label='Unclassified')

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()


# put all classes here before define the main function
class Geometry:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Point(Geometry):
    def __init__(self, x, y, category='None'):
        super().__init__('point')
        self.__x = x
        self.__y = y
        self.__category = category

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category


class Line(Geometry):
    def __init__(self, point_1, point_2):
        super().__init__('line')
        self.__point_1 = point_1
        self.__point_2 = point_2

    def get_point_1(self):
        return self.__point_1

    def get_point_2(self):
        return self.__point_2


class Polygon(Geometry):
    def __init__(self, points_list):
        super().__init__("polygon")
        self.__points_list = points_list

    def get_points_list(self):
        return self.__points_list

    def lines(self):
        res = []
        points = self.get_points_list()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a, point_b))
            point_a = point_b
        res.append(Line(point_a, points[0]))
        return res


class List():
    def __init__(self, number):
        self.number = number

    def minimum(self):
        res = self.number[0]
        for v in self.number[1:]:
            if v < res:
                res = v
        return res

    def maximum(self):
        res = self.number[0]
        for v in self.number[1:]:
            if v > res:
                res = v
        return res


class Classifier():

    def __init__(self, name, input_point, polygon):
        self.__name = name
        self.__input_point = input_point
        self.__polygon = polygon

    def get_input_point(self):
        return self.__input_point

    def get_polygon(self):
        return self.__polygon

    def min_bounding_rectangle_test(self):

        self.__polygon_points_list = self.__polygon.get_points_list()

        polygon_x_coordinates = []
        polygon_y_coordinates = []

        for i in self.__polygon_points_list:
            polygon_x_coordinates.append(i[0])
            polygon_y_coordinates.append(i[1])

        list_polygon_x = List(polygon_x_coordinates)
        list_polygon_y = List(polygon_y_coordinates)

        min_x = list_polygon_x.minimum()
        min_y = list_polygon_y.minimum()
        max_x = list_polygon_x.maximum()
        max_y = list_polygon_y.maximum()

        x = self.__input_point.get_x()
        y = self.__input_point.get_y()

        if x < min_x or x > max_x:
            self.__input_point.set_category("Outside")

        elif y < min_y or y > max_y:
            self.__input_point.set_category("Outside")

        else:
            self.__input_point.set_category("None")

        output_mbr = self.__input_point

        return output_mbr

    def point_on_line_test(self, line, point):
        # arguments are points to be tested,
        # x1, y1, x2, y2 define the line (lines of polygon)

        self.__line = line
        self.__point = point

        # # x3,y3 define the point to be tested (input points)
        x3 = self.__point.get_x()
        y3 = self.__point.get_y()
        # x1, y1, x2, y2 define the line (lines of polygon)

        point_1 = self.__line.get_point_1()
        x1 = point_1[0]
        y1 = point_1[1]

        point_2 = self.__line.get_point_2()
        x2 = point_2[0]
        y2 = point_2[1]

        # if the point is
        if (x3 < x1 and x3 < x2) or (x3 > x1 and x3 > x2) or (y3 < y1 and y3 < y2) or (y3 > y1 and y3 > y2):
            return False

        elif x1 == x2:
            if x3 == x1:
                return True
            else:
                return False
        else:
            y = (x3 - x1) * (y2 - y1) / (x2 - x1) + y1
            if y3 == y:
                return True
            else:
                return False

    # this method is to use point_on_line_test to test if input points in a point list are on the lines of a polygon
    def use_point_on_line_test(self):

        polygon_lines_list = self.__polygon.lines()

        if self.__input_point.get_category() == "None":

            for j in polygon_lines_list:
                pol_test_result = self.point_on_line_test(j, self.__input_point)

                if pol_test_result == True:
                    self.__input_point.set_category("Boundary")

        output_pol = self.__input_point
        return output_pol

    def ray_casting_test(self, line, point):

        self.__line = line
        self.__point = point

        # # x3,y3 define the point to be tested (input points)
        x3 = point.get_x()
        y3 = point.get_y()

        # x1, y1, x2, y2 define the line (lines of polygon)

        point_1 = self.__line.get_point_1()
        x1 = point_1[0]
        y1 = point_1[1]

        point_2 = self.__line.get_point_2()
        x2 = point_2[0]
        y2 = point_2[1]

        # divide the situation where the ray is cross to the line of polygon

        count = 0
        if y3 != y1 and y3 != y2:

            if y1 == y2:
                if y3 == y1:
                    # 射线和边重合
                    if x3 <= x1 or x3 <= x2:
                        count = count
                    else:
                        count = count
                else:
                    count = count

            else:
                x = (y3 - y1) * (x2 - x1) / (y2 - y1) + x1
                if y1 <= y3 <= y2 or y2 <= y3 <= y1:

                    if x >= x3:
                        count = count + 1
                else:
                    count = count

        # if the ray is crossing the vertices
        # check if the line which includes the vertice is up the ray, it will change the situation of the test point
        # so make the count plus one
        # it can be used for both of bottom ray and top ray because +2 and +0 will not have an influence for the results
        elif (x3 <= x1 and x3 <= x2):
            if y2 > y1 and y3 == y1:
                count = count + 1

            if y2 < y1 and y3 == y2:
                count = count + 1

        return count

    def use_ray_casting_test(self):

        polygon_lines_list = self.__polygon.lines()



        if self.__input_point.get_category() == "None":
            c = 0

            for j in polygon_lines_list:
                count = self.ray_casting_test(j, self.__input_point)
                c = c + count
            if c % 2 == 0:
                self.__input_point.set_category("Outside")
            else:
                self.__input_point.set_category("Inside")

        output_rca = self.__input_point
        return output_rca


class Reader():

    def __init__(self, name):
        self.__name = name

    def read_polygon(self):
        polygon_id = []
        polygon_x_coordinates = []
        polygon_y_coordinates = []

        with open("polygon.csv", "r") as p:
            for line in p.readlines():
                id = line.split(',')[0]
                polygon_id.append(id)

        with open("polygon.csv", "r") as p:
            for line in p.readlines():
                x = line.split(',')[1]
                polygon_x_coordinates.append(x)

        with open("polygon.csv", "r") as p:
            for line in p.readlines():
                y = line.split(',')[2]
                polygon_y_coordinates.append(y)

        polygon_id = [int(i) for i in polygon_id[1:]]
        polygon_x_coordinates = [float(i) for i in polygon_x_coordinates[1:]]
        polygon_y_coordinates = [float(i) for i in polygon_y_coordinates[1:]]

        # Turble Pair
        polygon_xy_coordinates = polygon_x_coordinates + polygon_y_coordinates

        n = 0
        polygon_coordinates = []
        for i in polygon_x_coordinates:
            r = (polygon_xy_coordinates[n], polygon_xy_coordinates[n + len(polygon_x_coordinates)])
            polygon_coordinates.append(r)
            n = n + 1

        polygon = Polygon(polygon_coordinates)
        return (polygon_x_coordinates, polygon_y_coordinates, polygon)


def main():

    file_path = sys.argv[0]
    print(file_path)

    plotter = Plotter()
    print("read polygon.csv")

    polygon_read = Reader("Polygon Reader")

    polygon = polygon_read.read_polygon()[2]
    polygon_x_coordinates = polygon_read.read_polygon()[0]
    polygon_y_coordinates = polygon_read.read_polygon()[1]


    print("Insert point information")
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))

    insert_point = Point(x, y)


    print("categorize point")

    pip_classifier = Classifier("PIP Classifier", insert_point, polygon)
    pip_classifier.min_bounding_rectangle_test()
    pip_classifier.use_point_on_line_test()
    pip_classifier.use_ray_casting_test()


    print("plot polygon and point")

    plotter.add_point(x, y, insert_point.get_category())

    plotter.add_polygon(polygon_x_coordinates, polygon_y_coordinates)

    plotter.show()


if __name__ == "__main__":
    main()


