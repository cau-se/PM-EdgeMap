from typing import Dict
from compute.compute import Compute
from node_monitor import NodeMonitor
from storage.storage import Storage
from network.fw.network import Network

class ComputingNode:

    def __init__(
            self,
            node_id,
            data_network,
            control_network,
            compute_generator,
            storage_generator,
            category,
            datasources,
            monitor
    ):
        self.node_id = node_id
        self.data_network: Network = data_network
        self.control_network: Network = control_network
        self.compute_generator = compute_generator
        self.storage_generator = storage_generator
        self.category = category
        self.datasources = datasources
        self.monitor: NodeMonitor = monitor
        self.storages: Dict[str, Storage] = dict()
        self.computes: Dict[str, Compute] = dict()

    def get_storage(self, name):
        storage_name = f"{self.node_id}-{name}"
        new_storage = self.storage_generator(storage_name)
        self.storages[name] = new_storage
        return new_storage

    def get_compute(self, name):
        compute_name = f"{self.node_id}-{name}"
        new_compute = self.compute_generator(compute_name)
        self.computes[name] = new_compute
        return new_compute

    def run_monitor(self, event_delta, time_delta):
        for storage in self.storages:
            self.monitor.add_value(f"storage-{storage}-time", self.storages[storage].time_utilization(event_delta))
            self.monitor.add_value(f"storage-{storage}-resource", self.storages[storage].resource_utilization(time_delta))

        for compute in self.computes:
            self.monitor.add_value(f"compute-{compute}-time", self.computes[compute].time_utilization(event_delta))
            self.monitor.add_value(f"compute-{compute}-resource", self.computes[compute].resource_utilization(time_delta))

        self.monitor.add_value(f"data-network-resource", self.data_network.resource_utilization(time_delta))
        self.monitor.add_value(f"data-network-time", self.data_network.time_utilization(event_delta))
        self.monitor.add_value(f"control-network-resource", self.control_network.resource_utilization(time_delta))
        self.monitor.add_value(f"control-network-time", self.control_network.time_utilization(event_delta))


    def reset_monitor(self):
        for storage in self.storages:
            self.storages[storage].reset_monitor()
        for compute in self.computes:
            self.computes[compute].reset_monitor()
        self.data_network.reset_monitor()
        self.control_network.reset_monitor()

    def run(self):
        self.data_network.run(self)
