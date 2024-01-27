from tkinter import Tk

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

from app import config
from app.Utils import add_settings


@add_settings("Эпюра", '400x400+200+100')
class DiagramWindow(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.data = np.array(config.interpolateData)
        self.graph()

    def graph(self):
        # figure, которая включает в себя plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)

        # Добавление subplot
        self.plot1 = fig.add_subplot(111)

        # Изобразить scatter
        self.s = 10
        x = np.linspace(0, self.data.shape[0]-1,num = self.data.shape[0])
        y = self.data[:, 2].flatten()

        plot = self.plot1.plot(x, y, color='k')
        # создать легенду с уникальными цветами из scatter
        self.plot1.set_xlabel('Точки')
        self.plot1.set_ylabel('R')
        # Создание Tkinter canvas
        # включение в нее Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig,
                                        master=self)
        self.canvas.draw()
        # размещение the Tkinter window
        self.canvas.get_tk_widget().pack()

        # создание Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,
                                       self)
        toolbar.update()

        # размещение toolbar в Tkinter window
        self.canvas.get_tk_widget().pack()