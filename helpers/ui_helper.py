from tkinter import ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import matplotlib.pyplot as plt


def create_combobox(root, values, width=20, state='readonly'):
    combo_box = ttk.Combobox(root, values=values, state=state, width=width, font='Arial 16')
    combo_box.current(0)

    return combo_box


def create_figure_canvas(master, fig_size=(16, 8)):
    # create figure and axes
    figure, axes = plt.subplots(figsize=fig_size)
    figure.subplots_adjust(bottom=0.3)

    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, master=master)

    # create the toolbar
    # NavigationToolbar2Tk(figure_canvas, master)

    return figure, axes, figure_canvas


def show_toast(msg, style):
    title = 'Success'

    if style == DANGER:
        title = 'Error'

    toast = ToastNotification(title=title, message=msg, position=(200, 10, 'ne'), duration=3000, bootstyle=style)
    toast.show_toast()
