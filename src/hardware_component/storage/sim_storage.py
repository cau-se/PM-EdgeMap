import threading
from typing import Dict

class SimulatedStorage(Dict):

    def __init__(self, initial_time, initial_resource, throughput, payload):
        super().__init__()
        self.initial_time = initial_time
        self.initial_resource = initial_resource
        self.throughput = throughput
        self.consumed_time = 0
        self.consumed_resource = 0
        self.payload = payload
        self.lock = threading.Lock()

    def time_utilization(self, event_delta):
        utilization = self.consumed_time / event_delta
        return utilization

    def resource_utilization(self, velocity):
        utilization = (self.consumed_resource * velocity) / self.throughput
        return utilization

    def reset_monitor(self):
        self.consumed_resource = 0
        self.consumed_time = 0

    def __setitem__(self, __key, __value):
        self.consumed_time = self.consumed_time + self.initial_time + (self.payload / self.throughput)
        self.consumed_resource = self.consumed_resource + self.initial_resource + self.payload
        super().__setitem__(__key, __value)

    def get_item(self, item, clazz):
        return self.__getitem__(item)

    def __getitem__(self, item):
        self.consumed_time = self.consumed_time + self.initial_time + (self.payload / self.throughput)
        self.consumed_resource = self.consumed_resource + self.initial_resource + self.payload
        return super().__getitem__(item)