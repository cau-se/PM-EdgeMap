from abc import ABC, abstractmethod

class Network(ABC):

    @abstractmethod
    def add_network_function(self, name, func, clazz):
        pass

    @abstractmethod
    def get(self, name):
        pass

    @abstractmethod
    def get_address(self):
        pass

    @abstractmethod
    def has_node(self, node_id):
        pass

    @abstractmethod
    def send_message(self, node_id, endpoint, payload):
        pass

    @abstractmethod
    def broadcast(self, endpoint, payload):
        pass

    @abstractmethod
    def run(self, node):
        pass

    @abstractmethod
    def time_utilization(self, event_delta):
        pass

    @abstractmethod
    def resource_utilization(self, time_delta):
        pass


