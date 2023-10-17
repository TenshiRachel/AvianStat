from tkinter import ttk, Frame
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)
import matplotlib.pyplot as plt


def create_combobox(root, values, width=20, state='readonly'):
    combo_box = ttk.Combobox(root, values=values, state=state, width=width, font='Arial 16')
    # Set initial value to first item of value
    combo_box.current(0)

    return combo_box


def create_figure_canvas(master, fig_size=(16, 8)):
    # create figure and axes
    figure, axes = plt.subplots(figsize=fig_size)
    figure.subplots_adjust(bottom=0.3)

    # Create frame to hold figure
    frame = Frame(master, highlightbackground='black', highlightthickness=1)
    frame.pack(fill=BOTH, expand=1, padx=(20, 0))

    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, master=frame)

    return figure, axes, figure_canvas, frame


def show_toast(msg, style):
    title = 'Success'

    if style == DANGER:
        title = 'Error'

    # Show success or error toast notification to user
    toast = ToastNotification(title=title, message=msg, position=(200, 10, 'ne'), duration=3000, bootstyle=style)
    toast.show_toast()
