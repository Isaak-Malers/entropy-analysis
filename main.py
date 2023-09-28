import csv
from collections import deque

from ts_entropy_analysis.data_analyzer import Analyzer
import matplotlib.pyplot as plt
from datetime import datetime


class FlowData:
    def __init__(self, agency_cd, site_no, datetime_str, flow_depth):
        self.agency_cd = agency_cd
        self.site_no = site_no
        self.datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        self.flow_depth = float(flow_depth)
        self.entropy = None

    def get_data(self):
        return [self.flow_depth]

    def __str__(self):
        return f"entropy: {self.entropy} Agency: {self.agency_cd}, Site No: {self.site_no}, Datetime: {self.datetime}, Flow Depth: {self.flow_depth}"


def plot_timeseries(flow_data_list):
    # Extract datetime, flow depth, and entropy data for plotting
    datetime_values = [data.datetime for data in flow_data_list]
    flow_depth_values = [data.flow_depth for data in flow_data_list]
    entropy_values = [data.entropy for data in flow_data_list]

    # Create a time series plot with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot flow depth on the left y-axis
    ax1.plot(datetime_values, flow_depth_values, label='Flow Depth', color='tab:blue')
    ax1.set_xlabel('Datetime')
    ax1.set_ylabel('Flow Depth', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for entropy on the right
    ax2 = ax1.twinx()
    ax2.plot(datetime_values, entropy_values, label='Entropy', color='tab:red')
    ax2.set_ylabel('Entropy', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Adjust the y-axis limits for entropy to better show fluctuations
    minEntropy = min(filter(lambda x: x is not None, entropy_values))
    maxEntropy = max(filter(lambda x: x is not None, entropy_values))
    ax2.set_ylim(minEntropy * .99, maxEntropy * 1.01)

    # Title and legend
    plt.title('Time Series of Flow Depth and Entropy')
    plt.legend(loc='upper left')

    # Show the plot
    plt.tight_layout()
    plt.show()


def parse_csv_to_objects(csv_file_path):
    flow_data_list = []

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            if len(row) == 4:  # Check if the row has the expected number of columns
                flow_data = FlowData(row[0], row[1], row[2], row[3])
                flow_data_list.append(flow_data)

    return flow_data_list


csv_file_path = './sample.csv'
flow_data_objects = parse_csv_to_objects(csv_file_path)

analysis = Analyzer()
deque(analysis.analyze(flow_data_objects, 6, data_func="get_data", entropy_out="entropy"), maxlen=0)

plot_timeseries(flow_data_objects)
