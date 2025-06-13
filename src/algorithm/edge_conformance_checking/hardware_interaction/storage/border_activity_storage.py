class BorderActivityStorage:

    def __init__(self, storage):
        self.storage = storage

    def store_activity(self, start_activity):
        self.storage.add(start_activity)

    def retrieve_activities(self):
        return self.storage