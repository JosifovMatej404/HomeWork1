from BeautifulPhraser import Pharser

class CommandHandler:
    def __init__(self, command_gui, drawing_gui):
        self.command_gui = command_gui
        self.drawing_gui = drawing_gui
        self.pharser = Pharser(command_gui)

    def clear_history(self):
        # Clear the command history
        self.command_gui.history_text.delete("1.0", "end")  # Clear all text
        self.command_gui.history_text.insert('end', ">>> ")  # Reset prompt
        self.command_gui.locked_index = self.command_gui.history_text.index("end-1c")  # Reset the locked index
        return

    def default_response(self):
        self.command_gui.history_text.insert("end", "\nCommand not recognised. Input \"help\" for more info.")
        self.command_gui.lock_history()
        return

    def help_response(self):
        self.command_gui.history_text.insert("end", "\nclear - clears the console\nget <name> - get specified supplier\nget suppliers - gets all available suppliers")
        self.command_gui.lock_history()
        return

    def get_data(self, input):
        if input == "none":  
            self.command_gui.history_text.insert("end", "\nIncorrect usage. Use get <name> for results.")
        else:
            self.command_gui.history_text.insert("end", "\nSearching for " + input)
            data = self.pharser.get_data(input)
            self.drawing_gui.populate_table(data)
        self.command_gui.lock_history()
        return

    def execute_command(self, command):
        command_array = command.split()
        commands = {
            "clear": self.clear_history,
            "help": self.help_response,
            "get": lambda: self.get_data(command_array[1] if len(command_array) > 1 else "none")
        }
        # Execute the command or provide a default response
        commands.get(command_array[0].lower(), self.default_response)()

