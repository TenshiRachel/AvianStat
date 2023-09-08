from tkinter import *
from tkinter import ttk
from helper import clean_plane_data
import pandas as pd


root = Tk()
root.title('Avian Stat')

data = pd.read_csv('./Airplane_Crashes_Since_1908.csv')

data = clean_plane_data(data)
