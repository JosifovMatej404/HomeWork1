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

def get_field_names(data):
    for key in data:
        pass

def save_data_to_csv(data, code):
    """Save formatted supplier data to a CSV file named after the code, appending data without rewriting headers."""

    # Define the directory and create it if it doesn't exist
    directory = "supplier_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the filename based on the code and the current date
    filename = os.path.join(directory, f"{code}_data_{datetime.datetime.now().date()}.csv")

    # Check if the file already exists and has content
    file_exists = os.path.isfile(filename)
    has_content = file_exists and os.path.getsize(filename) > 0

    # Write data to CSV file in append mode
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        # Only write headers if the file doesn't already have content
        if not has_content:
            writer.writeheader()
        
        # Append data rows
        writer.writerows(data)

    print(f"Data saved successfully for code '{code}' in '{filename}'.")
