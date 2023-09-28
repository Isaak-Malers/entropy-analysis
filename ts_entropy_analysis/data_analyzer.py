from ts_entropy_analysis.data_ingest import Ingest
from ts_entropy_analysis.entropy_algorithms import Entropy


class Analyzer:
    def __init__(self):
        self.entropy = Entropy()
        self.ingest = Ingest()

    def analyze(self, data: list, data_smoothing: int = 2, data_func: str = None, entropy_out: str = "entropy") -> [float]:
        """
        Given a [data] list, "magically" adds entropy data to each datapoint.

        :param data: a list of data objects.
        :param data_smoothing: how many objects on either side of a datapoint do you want to compare it to?
        :param data_func: name of a function to pull data out of each object in the data param list.  if left None it will use the entire object
        :param entropy_out: name of a field to store the entropy value at in each object in the data param list.  If left default it will use 'entropy'
        :return: yields each entropy value consecutively.  This is probably not all that useful.
        """

        def get_index(index: int):
            if index<0:
                return data[0]
            if index >= len(data):
                return data[-1]
            return data[index]

        def get_data(data_object):
            if data_func is None:
                return data_object
            try:
                func = getattr(data_object, data_func)
                return func()
            except AttributeError:
                raise ValueError(f"{data_func} not found on object type: {type(data_object)}")

        def put_data(data_object, value):
            try:
                setattr(data_object, entropy_out, value)
            except AttributeError:
                raise ValueError(f"{entropy_out} not foun don object type: {type(data_object)}")

        for i in range(0, len(data)):
            convolution_range = []
            for ci in range(i - data_smoothing, i + data_smoothing + 1):
                convolution_range.append(get_data(get_index(ci)))

            to_compress = self.ingest.ingest_list_with_pickle(convolution_range)
            entropy = self.entropy.compress_and_calculate_ratio(to_compress)
            put_data(data[i], entropy)
            yield entropy
