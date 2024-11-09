import BeautifulPhraser
import SeleniumWorker
import FileManager
import os
import glob
import re
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class PipeFilterSystem:
    def initialize_system(self, parent, filters):
        self.parent = parent
        self.pipe = Pipe(filters)

    def filter_data(self):
        return self.pipe.start_flow()

class Filter:
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def process_data(self, data):
        return data
    
class CodeFilter(Filter):
    def process_data(self, data):
        phraser = BeautifulPhraser.Pharser(self.command_handler) 
        data_array = phraser.get_data("suppliers")
        data_tags = []
        for item in data_array:
            data_tags.append(item.code)
        return data_tags
    
class DateFilter(Filter):
    def __init__(self, command_handler):
        super().__init__(command_handler)
        self.directory = "supplier_data"
    
    def find_latest_date(self, code):
        # Create a pattern to match the filenames
        pattern = os.path.join(self.directory, f"{code}_data_*.csv")
        files = glob.glob(pattern)
        
        if files:
            # Get the latest file based on creation time
            latest_file = max(files, key=os.path.getctime)
            
            # Extract the date from the filename using a regular expression
            match = re.search(r'(\d{4}-\d{2}-\d{2})', latest_file)
            if match:
                return match.group(1)  # Return the matched date
        return None  # If no files are found, return None

    def get_data(self, data):
        need_update_array = []

        for code in data:
            file_name = self.find_latest_date(code)
            need_update_array.append([code, file_name])

        return need_update_array

    def process_data(self, data):
        need_update_array = self.get_data(data)
        return need_update_array

class LastFilter(Filter):
    def __init__(self, command_handler):
        super().__init__(command_handler)
        self.data = []

    def process_data(self, data):
        data_array = []
        year = datetime.datetime.now().year

        # Record the start time of the process
        start_time = time.time()

        # Create a function to process each item in a separate thread
        def process_item(item):
            try:
                worker = SeleniumWorker.SeleniumWorker()
                phraser = BeautifulPhraser.Pharser(self.command_handler)
                if item[1] is None:
                    # Run for 9 years and process data
                    for i in range(9):
                        worker.fetch_data_with_dates_and_key(f"01.01.{year-10+i}", f"01.01.{year-9+i}", item[0])
                        worker.merge_data(phraser.get_data_from_html(item[0], worker.return_html()))
                        worker.html = ""
                    print("Last Run.")
                    worker.fetch_data_with_dates_and_key(f"01.01.{year}", worker.get_current_date(), item[0])
                    worker.merge_data(phraser.get_data_from_html(item[0], worker.return_html()))
                    worker.html = ""

                    data_item = [worker.return_data(), item[0]]
                    data_array.append(data_item)
                    FileManager.save_data_to_csv(data_item[0], item[0])
                else:
                    current_date = worker.convert_from_name_to_date(item[1])
                    if worker.is_date_older_than_today(current_date):
                        worker.fetch_data_with_dates_and_key(current_date, worker.get_current_date(), item[0])
                        worker.merge_data(phraser.get_data_from_html(item[0], worker.return_html()))
                        worker.html = ""
                        data_item = [worker.return_data(), item[0]]
                        data_array.append(data_item)
                        FileManager.save_data_to_csv(data_item[0], item[0], True, item[1])
            except Exception as e:
                print(f"Error processing {item[0]}: {e}")

        # Create a thread pool with a limit on the number of threads (e.g., 10 threads)
        with ThreadPoolExecutor(max_workers=15) as executor:
            # Submit tasks to the thread pool
            for item in data:
                executor.submit(process_item, item)
        
        # Record the end time of the process
        end_time = time.time()

        # Calculate and print the time taken
        elapsed_time = end_time - start_time
        self.command_handler.command_gui.history_text.insert("end", f"Data update completed in {elapsed_time:.2f} seconds.")
        self.command_handler.command_gui.lock_history()
        return data_array

class Pipe:
    def __init__(self, filters):
        self.filters = filters

    def start_flow(self):
        processed_data = []
        for filter in self.filters:
            processed_data = filter.process_data(processed_data)
        return processed_data