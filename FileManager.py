import os
import csv
import datetime


def format_supplier_data(data):
    """Format supplier data into a dictionary for easy saving to CSV files."""
    formatted_data = []
    for item in data:
        formatted_data.append({
            "Date": item.date,
            "Last Trade Price": item.last_trade_price,
            "Max": item.max,
            "Min": item.min,
            "Average Price": item.avg_price,
            "Percent Change": item.percent_change,
            "Volume": item.volume,
            "Turnover (Best)": item.turnover_best_denars,
            "Total Turnover": item.total_turnover_denars,
        })
    return formatted_data

def save_data_to_csv(data, code, append_mode=False, date=datetime.datetime.now().date()):
    """Save or append formatted supplier data to a CSV file named after the code."""
    directory = "supplier_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the filename based on the code and the current date
    filename = os.path.join(directory, f"{code}_data_{date}.csv")
    new_name = filename
    
    if append_mode:
        new_name = os.path.join(directory, f"{code}_data_{datetime.datetime.now()}.csv")

    # Format the data using format_supplier_data
    data = format_supplier_data(data)

    # Check if the file exists (for appending or writing header)
    file_exists = os.path.isfile(new_name)

    # Choose the mode based on append_mode
    mode = "a" if append_mode else "w"


    # Open the file and write the data
    with open(filename, mode=mode, newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        # Write the header only if the file doesn't exist or if appending is False
        if not file_exists or not append_mode:
            writer.writeheader()
        
        if append_mode:
            os.rename(filename, new_name)

        # Write the formatted data to the file
        writer.writerows(data)
    print(f"Data {'appended to' if append_mode else 'saved to'} '{filename}'.")
