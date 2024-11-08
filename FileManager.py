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
    """Save formatted supplier data to a CSV file named after the code."""
    directory = "supplier_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the filename based on the code and the current date
    filename = os.path.join(directory, f"{code}_data_{datetime.datetime.now().date()}.csv")


    data = format_supplier_data(data)


    # Write data to CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved successfully for code '{code}' in '{filename}'.")
