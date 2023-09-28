import pickle


class Ingest:

    def __init__(self):
        self.ingestionSettings = {}

    def ingest_list_with_pickle(self, to_ingest: []):
        pickled = []
        for item in to_ingest:
            pickled.append(self.ingest_with_pickle(item))
        return b"".join(pickled)

    def ingest_with_pickle(self, to_ingest):
        try:
            # Note:  pickle.loads can load this data back into the type
            serialized_data = pickle.dumps(to_ingest)
            return serialized_data
        except Exception as e:
            print(f"Serialization failed: {str(e)}")
            return None
