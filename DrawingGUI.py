import tkinter as tk
from tkinter import ttk  # Make sure to import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import BeautifulPhraser

class DrawingGUI:
    def __init__(self, parent):
        # Table setup
        self.table_frame = tk.Frame(parent)
        self.table_frame.pack(fill='x', pady=20)
        
        # Chart setup
        self.chart_frame = None  # Will be reassigned
        self.fig, self.ax = plt.subplots()


    def initialize_headers(self, headers):
        for index in range(0, len(headers.headers)):
            self.tree.heading("Column" + str(index+1), text=headers.headers[index])
        self.tree.pack(fill='x')

    def get_headers(self, path):
        return BeautifulPhraser.Pharser.get_headers(path)

    def draw_chart(self):
        if self.chart_frame:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
            self.ax.clear()
            #self.ax.plot(self.data['Column1'], self.data['Column2'], marker='o')
            self.ax.set_title("Sample Chart")
            self.ax.set_xlabel("Column 1")
            self.ax.set_ylabel("Column 2")
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def populate_table(self, data):
        headers = self.get_headers("https://www.mse.mk/mk/issuers/free-market")
        self.tree = ttk.Treeview(self.table_frame, columns=("Column" + str(i) for i in range(len(headers.headers))), show='headings')
        self.initialize_headers(headers)
        formated_data = self.format_data(data)
        for index, row in formated_data.iterrows():
            self.tree.insert("", "end", values=(row['Column' + str(i)] for i in range(len(headers.headers))))

    def populate_supplier_table(self, data, target):
        headers = self.get_headers("https://www.mse.mk/en/stats/symbolhistory/" + str(target))
        if not headers: return
        self.tree = ttk.Treeview(self.table_frame, columns=("Column" + str(i) for i in range(len(headers.headers))), show='headings')
        self.initialize_headers(headers)
        formated_data = self.format_supplier_data(data)
        for index, row in formated_data.iterrows():
            self.tree.insert("", "end", values=(row['Column' + str(i)] for i in range(len(headers.headers))))

    def format_data(self, data):
        data_dict = {
            "Column1": [object.code for object in data],
            "Column2": [object.description for object in data],
            "Column3": [object.isin for object in data],
            "Column4": [object.total_hv for object in data]
        }

    def format_supplier_data(self, data):
        data_dict = {
            "Column1": [object.date for object in data],
            "Column2": [object.last_trade_price for object in data],
            "Column3": [object.max for object in data],
            "Column4": [object.min for object in data],
            "Column5": [object.avg_price for object in data],
            "Column6": [object.percent_change for object in data],
            "Column7": [object.volume for object in data],
            "Column8": [object.turnover_best_denars for object in data],
            "Column8": [object.total_turnover_denars for object in data],
        }
        return pd.DataFrame(data_dict)