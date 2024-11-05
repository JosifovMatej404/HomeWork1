import tkinter as tk
from CommandHandler import CommandHandler

class CommandGUI:
    def __init__(self, parent, drawing_gui):
        self.parent = parent
        self.drawing_gui = drawing_gui

        # Create the text widget for command input
        self.history_text = tk.Text(parent, height=15, wrap='word', state='normal')
        self.history_text.pack(fill='both', expand=True)
        self.history_text.insert('end', ">>> ")  # Start with the command prompt
        self.history_text.mark_set("input_start", "end-1c")
        self.history_text.bind("<Return>", self.process_command)
        self.history_text.bind("<KeyPress>", self.restrict_cursor)
        self.history_text.bind("<BackSpace>", self.prevent_deletion)
        self.history_text.bind("<Escape>", self.select_current_line)
        self.history_text.bind("<Control-a>", self.select_current_line)  # Custom Ctrl + A behavior
        self.history_text.bind("<Control-Shift-Up>", lambda e: "break")  # Disable Ctrl + Shift + Up
        self.history_text.bind("<Key>", self.prevent_overwrite)  # Prevent overwriting the history
        self.history_text.focus_set()

        # Lock everything above the prompt
        self.locked_index = self.history_text.index("end-1c")

        # Initialize the command handler
        self.command_handler = CommandHandler(self, drawing_gui)

    def restrict_cursor(self, event=None):
        # Ensure the cursor does not move before the locked index
        current_index = self.history_text.index("insert")
        if self.history_text.compare(current_index, "<", self.locked_index):
            self.history_text.mark_set("insert", self.locked_index)
            return "break"
        return

    def prevent_deletion(self, event=None):
        # Prevent deletion of committed text
        current_index = self.history_text.index("insert")
        if self.history_text.compare(current_index, "<=", self.locked_index):
            return "break"  # Stop the event from propagating
        return

    def prevent_overwrite(self, event=None):
        # Allow typing in the current line only
        current_index = self.history_text.index("insert")
        if self.history_text.compare(current_index, "<", self.locked_index):
            return "break"  # Prevent typing in previous commands
        return

    def select_current_line(self, event=None):
        # Custom behavior for Ctrl + A to select only the current input line
        input_start = self.locked_index  # Start of the input line (after >>>)
        input_end = self.history_text.index("end-1c")
        self.history_text.tag_remove("sel", "1.0", "end")  # Clear any previous selection
        self.history_text.tag_add("sel", input_start, input_end)  # Select only the current input line
        self.history_text.mark_set("insert", input_end)  # Move the cursor to the end of the input
        return "break"  # Override the default behavior

    def lock_history(self):
        self.history_text.insert('end', f"\n>>> ")
        self.history_text.configure(state='disabled')
        self.history_text.configure(state='normal')
        self.history_text.mark_set("input_start", "end-1c")
        self.locked_index = self.history_text.index("end-1c")
        self.history_text.see("end")

    def process_command(self, event=None):
        # Get the command input
        input_start = self.locked_index
        command = self.history_text.get(input_start, "end-1c").strip()
        if command:
            self.command_handler.execute_command(command)
        return "break"  # Prevent the default newline behavior
