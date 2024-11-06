import BeautifulPhraser

class Filter:
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def process_data(self, data):
        return data
    
class CodeFilter(Filter):
    def __init__(self, command_handler, path):
        super().__init__(command_handler)
        self.path = path

    def process_data(self, data):
        phraser = BeautifulPhraser.Pharser(self.command_handler) 
        data_array = phraser.get_data_array(self.path)
        data_tags = []
        for item in data_array:
            data_tags.append(item.code)
        return data_tags
    
class DateFilter(Filter):
    def __init__(self, command_handler):
        super().__init__(command_handler)
    
    def process_data(self, data):
        #check for last date if no last date found download 10 years back
        return data

class 

class Pipe:
    def __init__(self,data, filters):
        self.data = data
        self.filters = filters

    def start_flow(self):
        for filter in self.filters:
            filter.process_data(self.data)
