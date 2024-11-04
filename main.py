# main.py
import tkinter as tk
from CommandGUI import CommandGUI
from DrawingGUI import DrawingGUI

root = tk.Tk()
root.title("MacBot Analyst")

# Create the main container frame to arrange all components
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Top frame for the table
top_frame = tk.Frame(main_frame)
top_frame.pack(fill='x', pady=5, padx=20)

# Bottom frame to split the chart and command areas
bottom_frame = tk.Frame(main_frame)
bottom_frame.pack(fill='both', expand=True, pady=20)

# Left frame for the command input area
left_frame = tk.Frame(bottom_frame)
left_frame.pack(side='left', fill='both', expand=True, padx = 20)

# Right frame for the chart area
right_frame = tk.Frame(bottom_frame)
right_frame.pack(side='right', fill='both', expand=True, padx = 20)

# Instantiate the drawing GUI (table and chart)
drawing_gui = DrawingGUI(top_frame)  # Table in the top frame

# Reassign the chart frame to the right frame and draw the chart there
drawing_gui.chart_frame = right_frame
drawing_gui.draw_chart()  # Call a method to redraw the chart in the new frame

# Instantiate the command GUI (command input area)
command_gui = CommandGUI(left_frame)  # Command area in the left frame

root.mainloop()
