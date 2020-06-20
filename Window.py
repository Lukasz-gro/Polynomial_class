import matplotlib as mpl
import Polynomial_class
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as Tkinter
import tkinter.messagebox as tkmb
import tkinter.simpledialog as tksd
import tkinter.filedialog as tkfd
import numpy as np
import warnings
mpl.use('TkAgg')

warnings.simplefilter('ignore', np.RankWarning)


class PolynomialClient(Tkinter.Tk, Polynomial_class.Polynomial):
    def __init__(self,degree, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self._quit)
        self.grid()
        self.toolbar_frame = Tkinter.Frame(self)
        self.toolbar_frame.grid()
        self.My_fig = plt.figure()
        self.Canvas = FigureCanvasTkAgg(self.My_fig, master=self)
        self.Toolbar = NavigationToolbar2Tk(self.Canvas, self.toolbar_frame)
        self.Toolbar.update()
        self.toolbar_frame.grid(column=1, row=0, sticky=Tkinter.W+ Tkinter.N+Tkinter.S)
        self.Canvas._tkcanvas.grid(column=1, row=1, rowspan=4, sticky=Tkinter.W+Tkinter.E+Tkinter.N+ Tkinter.S)

        self.pol_degree = Tkinter.Button(self, text="Polynomial degree", command=self.polynomial_degree)
        self.pol_degree.grid(column=0, row=1, sticky=Tkinter.E+Tkinter.S+Tkinter.W+Tkinter.N)

        self.data_read = Tkinter.Button(self, text="Read data from file", command=self.data)
        self.data_read.grid(column=0, row=2, sticky=Tkinter.E+Tkinter.S+Tkinter.W+Tkinter.N)

        self.fit_poly_graph = Tkinter.Button(self, text="Fit polynomial to data", command=self.fit_polynomial)
        self.fit_poly_graph.grid(column=0, row=3, sticky=Tkinter.E+Tkinter.S+Tkinter.W+Tkinter.N)

        self.save_cfg = Tkinter.Button(self, text="Save config", command=self.save_config)
        self.save_cfg.grid(column=0, row=4, sticky=Tkinter.E + Tkinter.S + Tkinter.W + Tkinter.N)

        self.QUIT = Tkinter.Button(text="QUIT", fg="blue", command=self._quit)
        self.QUIT.grid(column=0, row=0)

        self.x_data = []
        self.y_data = []
        self.coefficient = []
        self.degree = degree

    # saving the fitted polynomial
    def save_config(self):
        check = tkmb.askokcancel('Check', 'Have you fitted polynomial?')
        if check:
            name_of_file = tksd.askstring(title='Name of your file', prompt='Input', initialvalue='cfg.txt')
            if '.txt' in name_of_file:
                name_of_file = name_of_file[:-4]
            coef_new = [str(i) for i in self.coefficient]
            with open("{}.txt".format(name_of_file), "w") as f:
                f.write('\n'.join(coef_new))
        else:
            pass

    # degree of the polynomial that will be fitted
    def polynomial_degree(self):
        self.degree = -1

        while self.degree < 0 or type(self.degree) != int:
            self.degree = tksd.askinteger(title='Degree of the polynomial', prompt='Input', initialvalue='1')

    # reading the data to which polynomial will be fitted
    def data(self):
        new_data = tkfd.askopenfile(title='Directory of data', mode="r", initialdir=".")
        lines = new_data.readlines()

        for line in lines:
            self.x_data.append(float(line.split(',')[0]))
            self.y_data.append(float(line.split()[1]))

        counter = 0
        message_data = 'X \t Y\n'
        while counter < 5 and counter < len(self.x_data):
            message_data += str(self.x_data[counter])[:4] + "\t" + str(self.y_data[counter])[:4] + "\n"
            counter += 1
        tkmb.showinfo("I am your data!", message_data)

    # fitting polynomial
    def fit_polynomial(self):
        if self.degree == -1:
            self.polynomial_degree()
        if len(self.x_data) == 0:
            self.data()

        self.coefficient = np.polyfit(self.x_data, self.y_data, self.degree)[::-1]
        self.graph()

    # creating the graph
    def graph(self):
        min_value = min(self.x_data)
        max_value = max(self.x_data)
        x_range = np.linspace(min_value, max_value, int(max_value-min_value)*100)

        fitted_polynomial = Polynomial_class.Polynomial(self.coefficient)
        y_range = []
        for i in x_range:
            y_range.append(fitted_polynomial(i))

        self.ax1 = self.My_fig.add_subplot(111)
        self.ax1.plot(x_range, y_range)
        self.ax1.plot(self.x_data, self.y_data, "ro")
        self.Canvas.draw()

    # returning the polynomial
    def get_polynomial(self):
        self.coefficient = np.polyfit(self.x_data, self.y_data, self.degree)[::-1]
        fitted_polynomial = Polynomial_class.Polynomial(self.coefficient)
        return fitted_polynomial

    # exiting the app
    def _quit(self):
        print("Polynomial client has been turned off")
        app.quit()


while True:
    try:
        degree = int(input('Enter the degree of the polynomial:'))
    except ValueError:
        print('You need to input integer greater than zero')
        continue
    if degree < 0:
        print('You need to input integer greater than zero')
        continue
    else:
        break

app = PolynomialClient(degree, None)
