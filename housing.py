import csv
from collections import deque
from datetime import datetime

from ts_entropy_analysis.data_analyzer import Analyzer
import matplotlib.pyplot as plt


class PropertySale:
    def __init__(self, datesold, postcode, price, property_type, bedrooms):
        self.datesold = datetime.strptime(datesold, "%Y-%m-%d %H:%M:%S")
        self.postcode = postcode
        self.price = int(price)
        self.property_type = property_type
        self.bedrooms = int(bedrooms)

        self.entropy = None

    def get_data(self):
        return [self.postcode, self.price, self.bedrooms]

    def __str__(self):
        return f"entropy:{self.entropy} Date Sold: {self.datesold}, Postcode: {self.postcode}, Price: {self.price}, Property Type: {self.property_type}, Bedrooms: {self.bedrooms}"


def plot_property_sales(property_sales):
    dates = [sale.datesold for sale in property_sales]
    prices = [sale.price for sale in property_sales]
    bedrooms = [sale.bedrooms for sale in property_sales]
    entropy = [sale.entropy for sale in property_sales]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Date Sold')
    ax1.set_ylabel('Price and Bedrooms', color='tab:blue')
    ax1.scatter(dates, prices, label='Price', marker='o', color='tab:blue', alpha=0.5)
    ax1.scatter(dates, bedrooms, label='Bedrooms', marker='x', color='tab:blue', alpha=0.5)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Entropy', color='tab:red')
    ax2.scatter(dates, entropy, label='Entropy', marker='s', color='tab:red', alpha=0.5)
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Property Sales Over Time')
    fig.tight_layout()

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    plt.legend(lines, labels, loc='upper left')

    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def read_csv_file(file_path):
    property_sales = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            property_sale = PropertySale(
                row["datesold"],
                row["postcode"],
                row["price"],
                row["propertyType"],
                row["bedrooms"]
            )
            property_sales.append(property_sale)
    return property_sales


csv_file_path = "raw_sales.csv"
property_sales_list = read_csv_file(csv_file_path)

analysis = Analyzer()
deque(analysis.analyze(property_sales_list, 40, data_func="get_data", entropy_out="entropy"))

# Example usage to print the objects
for property_sale in property_sales_list:
    print(property_sale)

plot_property_sales(property_sales_list)