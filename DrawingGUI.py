import tkinter as tk
from tkinter import ttk  # Make sure to import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DrawingGUI:
    def __init__(self, parent):
        # Table setup
        self.table_frame = tk.Frame(parent)
        self.table_frame.pack(fill='x', pady=20)

        # Make sure ttk is imported, and Treeview is correctly used
        self.tree = ttk.Treeview(self.table_frame, columns=("Column1", "Column2", "Column3", "Column4"), show='headings')
        self.tree.heading("Column1", text="Column 1")
        self.tree.heading("Column2", text="Column 2")
        self.tree.heading("Column3", text="Column 3")
        self.tree.heading("Column4", text="Column 4")
        self.tree.pack(fill='x')

        # Chart setup
        self.chart_frame = None  # Will be reassigned
        self.fig, self.ax = plt.subplots()

        # Sample data; NEED TO GET DATA FROM MSE
        self.data = pd.DataFrame({
            'Column1': [1, 2, 3, 4, 5],
            'Column2': [10, 15, 20, 25, 30],
            'Column3': [5, 3, 8, 6, 4],
            'Column4': [51, 33, 83, 64, 45]
        })
        self.populate_table()

    def draw_chart(self):
        if self.chart_frame:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
            self.ax.clear()
            self.ax.plot(self.data['Column1'], self.data['Column2'], marker='o')
            self.ax.set_title("Sample Chart")
            self.ax.set_xlabel("Column 1")
            self.ax.set_ylabel("Column 2")
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def populate_table(self):
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=(row['Column1'], row['Column2'], row['Column3'], row['Column4']))
