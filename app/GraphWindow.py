import copy
from tkinter import Tk, Button

from app import config

#Библиотеки для анализа и визуализации
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from scipy.spatial import Delaunay

from app.DiagramWindow import DiagramWindow
from app.ErrorWindow import ErrorWindow
from app.Utils import add_settings


@add_settings("Окно визуализации", '400x450+200+100')
class GraphWindow(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.data = np.array(config.data)
        self.point1 = None
        self.point2 = None
        self.point1Bool = True
        self.drawLine = None
        self.drawLineBool = False
        self.point1Scatter = None
        self.point2Scatter = None
        self.numberOfPoints = 18
        self.interpolationPoints = None
        self.pointsScatterInterpolant = None
        self.canvas = None

        self.button_visual = Button(self, text='Построить эпюру', padx=150, pady=20,
                               command=lambda: self.create_diagram()).pack()

        if (self.data.shape[0]==0):
            ErrorWindow(self, config.errorData)
        else:
            if (self.data.shape[1] != 3):
                ErrorWindow(self, config.errorDataImport)
            else:
                self.graph()

    def graph(self):
        # figure, которая включает в себя plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)

        # Добавление subplot
        self.plot1 = fig.add_subplot(111)


        # Изобразить scatter
        self.s = 10
        x = self.data[:, 0].flatten()
        y = self.data[:, 1].flatten()
        colors = [self.data[:, 2].flatten()]
        scatter = self.plot1.scatter(x, y, c=colors, s=self.s, cmap='viridis')
        # создать легенду с уникальными цветами из scatter
        legend1 = self.plot1.legend(*scatter.legend_elements(),
                            loc="upper right", title="R")
        self.plot1.add_artist(legend1)
        # Создание Tkinter canvas
        # включение в нее Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig,
                                   master=self)
        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.onpick)
        # размещение the Tkinter window
        self.canvas.get_tk_widget().pack()

        # создание Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,
                                       self)
        toolbar.update()

        # размещение toolbar в Tkinter window
        self.canvas.get_tk_widget().pack()

    def onpick(self,event):
        tb = plt.get_current_fig_manager().toolbar  # +++
        print(repr(tb.mode), bool(tb.mode))  # +++
        if not tb.mode:  # +++
            clickPoint = np.array((event.xdata, event.ydata))
            #Поиск ближайшей точки и назначение ее для расчета
            dists=[]
            for point in self.data[:,0:2]:
                dists.append(GraphWindow.distance(clickPoint,point))

            idx_min = np.array(dists).flatten().argmin()
            if (self.point1Bool):
                self.point1 = copy.deepcopy(self.data[idx_min,:])
                self.point1Bool = False
                self.point1Scatter = self.drawPoint(self.point1, self.point1Scatter)
            else:
                self.point2 = copy.deepcopy(self.data[idx_min, :])
                self.point1Bool = True
                self.drawLineBool = True
                self.point2Scatter =self.drawPoint(self.point2, self.point2Scatter)

            #Проверка на прорисовку линии
            if (self.drawLineBool):
                if (self.drawLine != None):
                    print(self.drawLine)
                    self.drawLine[0].remove()
                self.drawLine = self.plot1.plot([self.point1[0], self.point2[0]],
                                                [self.point1[1], self.point2[1]], color='k')
                #разбиение отрезка на точки и их прорисовка
                deltaX = (self.point2[0]-self.point1[0])/(self.numberOfPoints+1)
                deltaY = (self.point2[1] - self.point1[1]) / (self.numberOfPoints+1)
                self.interpolationPoints = np.zeros((self.numberOfPoints,3))
                for item in range(self.numberOfPoints):
                    self.interpolationPoints[item, 0] = self.point1[0] + deltaX*(item+1)
                    self.interpolationPoints[item, 1] = self.point1[1] + deltaY * (item + 1)

                #Триангуляция Делоне
                self.interpolationPoints[:,2] = self.DeloneTriangulation(self.data[:,:2],
                                         self.data[:,2],
                                         self.interpolationPoints[:,:2],2)
                config.interpolateData = []
                config.interpolateData = [list(self.point1)]
                for item in self.interpolationPoints:
                    config.interpolateData.append(list(item))
                config.interpolateData.append(list(self.point2))

                if (self.pointsScatterInterpolant != None):
                    self.pointsScatterInterpolant.remove()
                self.pointsScatterInterpolant = self.plot1.scatter(self.interpolationPoints[:,0], self.interpolationPoints[:,1],
                                   c=self.interpolationPoints[:,2].flatten(), s=self.s, cmap='viridis')

                self.canvas.draw()

    def drawPoint(self, point1, point1Scatter):
        if (point1Scatter != None):
            point1Scatter.remove()
        point1Scatter = self.plot1.scatter(point1[0], point1[1], c=-10, s=self.s * 2, cmap='viridis')
        self.canvas.draw()
        return point1Scatter

    def DeloneTriangulation(self,points, values, p, n):
        #https://stackoverflow.com/questions/30373912/interpolation-with-delaunay-triangulation-n-dim
        # dimension of the problem (in this example I use 3D grid,
        # but the method works for any dimension n>=2)
        #n = 2
        # my array of grid points (array of n-dimensional coordinates)
        #points = [[1, 2], [2, 3], ...]
        # each point has some assigned value that will be interpolated
        # (e.g. a float, but it can be a function or anything else)
        #values = [7, 8, ...]
        # a set of points at which I want to interpolate (it must be a NumPy array)
        #p = np.array([[1.5, 2.5, 3.5], [1.1, 2.2, 3.3], ...])

        # create an object with triangulation
        tri = Delaunay(points)
        """
        plt.triplot(points[:, 0], points[:, 1], tri.simplices)
        plt.plot(points[:, 0], points[:, 1], 'o')
        plt.show()
        """
        # find simplexes that contain interpolated points
        s = tri.find_simplex(p)
        # get the vertices for each simplex
        v = tri.vertices[s]
        # get transform matrices for each simplex (see explanation bellow)
        m = tri.transform[s]

        # for each interpolated point p, mutliply the transform matrix by
        # vector p-r, where r=m[:,n,:] is one of the simplex vertices to which
        # the matrix m is related to (again, see bellow)
        #for i in range(len(p)): b[i] = m[i, :n, :n].dot(p[i] - m[i, n, :]) аналог нижней строчки
        b = np.einsum('ijk,ik->ij', m[:, :n, :n], p - m[:, n, :])

        # get the weights for the vertices; `b` contains an n-dimensional vector
        # with weights for all but the last vertices of the simplex
        # (note that for n-D grid, each simplex consists of n+1 vertices);
        # the remaining weight for the last vertex can be copmuted from
        # the condition that sum of weights must be equal to 1
        w = np.c_[b, 1 - b.sum(axis=1)]

        #Now, v contains indices of vertex points for each simplex and w holds corresponding weights.
        # To get the interpolated values p_values at set of points p,
        # we do (note: values must be NumPy array for this):
        #for i in range(len(p)): p_values[i] = np.inner(values[v[i]], w[i])
        p_values = np.einsum('ij,ij->i', values[v], w)
        return p_values

    def create_diagram(self):
        if len(config.interpolateData)>0:
            dW = DiagramWindow()
            dW.mainloop()
        else:
            ErrorWindow(self, config.errorTextInterpolate)

    @staticmethod
    def distance(point_1, point_2):
        return ((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2) ** 0.5
