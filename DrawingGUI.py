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
        self.tree = ttk.Treeview(self.table_frame, columns=[], show='headings')
        self.tree.pack(fill='x')

        # Chart setup
        self.chart_frame = None  # Will be reassigned
        self.fig, self.ax = plt.subplots()


<<<<<<< HEAD
    def initialize_headers(self, headers):
        print(headers.headers)
        for index in range(0, len(headers.headers)):
            self.tree.heading("Column" + str(index+1), text=headers.headers[index])
        self.tree.pack(fill='x')

    def get_headers(self,path):
=======
    def get_headers(self, path):
>>>>>>> 3e6bd582d79d20839ee03362c85030522a44d74f
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

    def initialize_headers(self, headers):
        # Initialize column headers for the Treeview
        columns = ["Column" + str(i + 1) for i in range(len(headers.headers))]
        self.tree["columns"] = columns

        for index, header in enumerate(headers.headers):
            self.tree.heading(columns[index], text=header)
        

    def populate_table(self, data):
<<<<<<< HEAD
        self.initialize_headers(self.get_headers("https://www.mse.mk/mk/issuers/free-market"))
        formated_data = self.format_data(data)
        for index, row in formated_data.iterrows():
            self.tree.insert("", "end", values=(row['Column1'], row['Column2'], row['Column3'], row['Column4']))
=======
        # Get headers for all suppliers from the specified URL
        headers = self.get_headers("https://www.mse.mk/mk/issuers/free-market")

        self.clear_table()
        self.tree = ttk.Treeview(self.table_frame, columns=("Column" + str(i+1) for i in range(len(headers.headers))), show='headings')
        self.initialize_headers(headers)

        formatted_data = self.format_data(data)
        for index, row in formatted_data.iterrows():
            values = [row["Column" + str(i+1)] for i in range(len(headers.headers))]
            self.tree.insert("", "end", values=values)

        self.tree.pack(fill='x')

    def populate_supplier_table(self, data, target):
        # Get headers for the supplier table from the specified URL
        headers = self.get_headers(f"https://www.mse.mk/en/stats/symbolhistory/{target}")

        if not headers:
            return
        
        self.clear_table()
        self.initialize_headers(headers)
        formatted_data = self.format_supplier_data(data)
        for index, row in formatted_data.iterrows():
            values = [row["Column" + str(i+1)] for i in range(len(headers.headers))]
            self.tree.insert("", "end", values=values)

        self.tree.pack(fill='x')
>>>>>>> 3e6bd582d79d20839ee03362c85030522a44d74f

    def format_data(self, data):
        data_dict = {
            "Column1": [object.code for object in data],
            "Column2": [object.description for object in data],
            "Column3": [object.isin for object in data],
            "Column4": [object.total_hv for object in data]
        }
        return pd.DataFrame(data_dict)

    def clear_table(self):
        # Remove all rows
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Remove all columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree["columns"] = ()  # Reset columns
        
        self.tree.pack_forget()  # Hide the tree until new columns are set


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
            "Column9": [object.total_turnover_denars for object in data],
        }
        return pd.DataFrame(data_dict)