class SimulatedCompute:

    def __init__(self, initial_time, initial_resource, throughput, payload):
        self.initial_time = initial_time
        self.initial_resource = initial_resource
        self.throughput = throughput
        self.consumed_time = 0
        self.consumed_resource = 0
        self.payload = payload

    def time_utilization(self, event_delta):
        utilization = self.consumed_time / event_delta
        return utilization

    def resource_utilization(self, velocity):
        utilization = (self.consumed_resource * velocity)# / self.throughput
        return utilization

    def reset_monitor(self):
        self.consumed_resource = 0
        self.consumed_time = 0

    def run(self, f, p=None):
        self.consumed_time = self.consumed_time + self.initial_time + (self.payload / self.throughput)
        self.consumed_resource = self.consumed_resource + self.initial_resource + self.payload
        if p:
            return f(p)
        else:
            return f()
