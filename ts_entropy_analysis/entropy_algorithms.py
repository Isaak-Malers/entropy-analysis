import gzip


class Entropy:

    def compress_and_calculate_ratio(self, *to_compress):
        concatenated_data = b"".join(to_compress)
        compressed_data = gzip.compress(concatenated_data, compresslevel=3)
        compression_ratio = len(compressed_data) / len(concatenated_data)
        return compression_ratio
