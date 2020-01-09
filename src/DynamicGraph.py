import matplotlib.pyplot as plt

class DynamicGraph():

    def __init__(self, title = '', ylabel = ''):
        plt.ion()

        self.xdata = []
        self.ydata = []
        self.x = 0

        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot(self.xdata, self.ydata, 'r-')

        # Graph Labels
        self.ax.set_title(title)
        self.ax.set_xlabel('Seconds')
        self.ax.set_ylabel(ylabel)

        self.ax.set_autoscaley_on(True)
        self.ax.set_autoscalex_on(True)
        #self.ax.set_xlim(self.min_x, self.max_x)

        self.ax.grid()

    def addValue(self, newValue):
        self.xdata.append(self.x)
        self.ydata.append(newValue)
        self.x += 1

        self.updateGraph()

    def updateValues(self, values):
        self.xdata = range(len(values))
        self.ydata = values

        self.updateGraph()

    def updateGraph(self):
        # Update data with the new and the old points
        self.lines.set_xdata(self.xdata)
        self.lines.set_ydata(self.ydata)

        # Rescaling
        self.ax.relim()
        self.ax.autoscale_view()

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
