from BeautifulPhraser import Pharser
from PipeFilterSystem import *

class CommandHandler:
    def __init__(self, command_gui, drawing_gui):
        self.command_gui = command_gui
        self.drawing_gui = drawing_gui
        self.pharser = Pharser(self)

    def clear_history(self):
        # Clear the command history
        self.command_gui.history_text.delete("1.0", "end")  # Clear all text
        self.command_gui.history_text.insert('end', ">>> ")  # Reset prompt
        self.command_gui.locked_index = self.command_gui.history_text.index("end-1c")  # Reset the locked index

    def default_response(self):
        self.command_gui.history_text.insert("end", "\nCommand not recognised. Input \"help\" for more info.")
        self.command_gui.lock_history()

    def help_response(self):
        self.command_gui.history_text.insert("end", "\nclear - clears the console\nget <name> - display previous month for specified supplier\nget suppliers - display all available suppliers\nupdate all - update all supliers\nupdate <name> - update specified suplier -NOT YET IMPLEMENTED- ")
        self.command_gui.lock_history()

    def fail_response(self):
        self.command_gui.history_text.insert("end", "\nFailed to get data. Data doesnt exist or it's inaccessible.")

    def get_data(self, input):
        if input == "none":  
            self.command_gui.history_text.insert("end", "\nIncorrect usage. Use get <name> for results.")
        else:
            self.command_gui.history_text.insert("end", "\nSearching for " + input)
            data = self.pharser.get_data(input)
            if input == "suppliers": self.drawing_gui.populate_table(data)
            else: self.drawing_gui.populate_supplier_table(data, input)
        self.command_gui.lock_history()

    def update_data(self, query):
        filter1 = CodeFilter(self)
        filter2 = DateFilter(self)
        filter3 = LastFilter(self)
        self.command_gui.history_text.insert("end", "\nUpdating all suppliers...")
        self.command_gui.lock_history()

        if query == "all":
            pfs = PipeFilterSystem()
            pfs.initialize_system(self, [filter1, filter2, filter3])
            pfs.filter_data()
        

    def execute_command(self, command):
        command_array = command.split()
        commands = {
            "clear": self.clear_history,
            "help": self.help_response,
            "get": lambda: self.get_data(command_array[1] if len(command_array) > 1 else "none"),
            "update": lambda: self.update_data(command_array[1] if len(command_array) > 1 else "none")
        }
        # Execute the command or provide a default response
        commands.get(command_array[0].lower(), self.default_response)()

    

