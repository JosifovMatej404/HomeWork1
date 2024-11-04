class CommandHandler:
    def __init__(self, gui):
        self.gui = gui

    def clear_history(self):
        # Clear the command history
        self.gui.history_text.delete("1.0", "end")  # Clear all text
        self.gui.history_text.insert('end', ">>> ")  # Reset prompt
        self.gui.locked_index = self.gui.history_text.index("end-1c")  # Reset the locked index

    def default_response(self):
        self.gui.history_text.insert("end", "\nCommand not recognised. Input \"help\" for more info.")
        self.gui.lock_history()

    def help_response(self):
        self.gui.history_text.insert("end", "\nclear - clears the console")
        self.gui.lock_history()

    def execute_command(self, command):
        commands = {
            "clear": self.clear_history,
            "help": self.help_response
        }
        # Execute the command or provide a default response
        commands.get(command.lower(), self.default_response)()

