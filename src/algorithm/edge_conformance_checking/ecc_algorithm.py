import time

from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

from src.algorithm.data_structures.conformance_score import SConformanceScore
from src.algorithm.edge_conformance_checking.hardware_interaction.ecc_compute import EdgeConformanceCheckingCompute
from src.algorithm.edge_conformance_checking.hardware_interaction.ecc_storage import EdgeConformanceCheckingStorage
from src.hardware_component.network.network_interface import Network
from src.topology.computing_node import ComputingNode

class EdgeConformanceCheckingAlgorithm:
    def __init__(
        self,
        learning_events
    ):
        self.node_id = None
        self.processed_events = 0
        self.learning_events = learning_events

    def run_on_node(self, node: ComputingNode):
        self.node_id: str = node.node_id
        self.monitor = node.monitor
        self.storage: EdgeConformanceCheckingStorage = EdgeConformanceCheckingStorage(
            node.get_storage("df"),
            node.get_storage("case"),
            node.get_storage("conform")
        )
        self.cpu = EdgeConformanceCheckingCompute(node.get_compute("cpu"))
        self.network: Network = node.control_network

        self.network.add_network_function("event", self.process_event, Event)
        self.network.add_network_function("timestamp", self.get_timestamp_of_case, str)
        self.network.add_network_function("conformance", self.get_conformance_of_case, None)
        self.network.add_network_function("conformance_get", self.conformance_get, None)
        self.network.add_network_function("dfg", self.get_directly_follows_graph, None)

    def process_event(self, event):
        self.processed_events = self.processed_events + 1
        if self.processed_events < 100:
            self.discover(event)
        else:
            self.get_conformance_of_case(event)
        return ""

    def discover(self, event):
        start = time.time()
        activity = event.activity
        last_event: Event = self.storage.get_activity_of_case(event.caseid)

        node_with_timestamp = self.network.broadcast(endpoint="timestamp", payload=event.caseid)
        predecessor_node = self.cpu.get_predecessor_node(last_event, node_with_timestamp)
        self.storage.store_event_for_case(event)

        predecessor = None
        if predecessor_node:
            self.storage.store_start_activity(event.activity)
            predecessor = predecessor_node
        elif last_event:
            predecessor = last_event.activity
        else:
            self.storage.store_start_activity(event.activity)

        if predecessor:
            self.storage.store_directly_follows_relation(
                DirectlyFollowsRelation(
                    predecessor=predecessor,
                    successor=activity
                )
            )
        end = time.time()
        self.monitor.add_value("discover_times", end-start)

    def get_timestamp_of_case(self, case_id):
        last_event: Event = self.storage.get_activity_of_case(case_id)
        if last_event:
            last_timestamp = last_event.timestamp
            return last_timestamp
        return None

    def get_conformance_of_case(self, event):
        start = time.time()
        conformance_values = self.storage.retrieve_conformance_values(event.caseid)

        last_activity = conformance_values.last_activity
        print(last_activity)
        dfg: DirectlyFollowsGraph = self.storage.get_directly_follows_graph()

        current_conformance = None
        if last_activity:
            print("Inner activity")
            current_conformance = SConformanceScore(
                path_length=conformance_values.conformance.path_length,
                conformance_violations=conformance_values.conformance.conformance_violations
            )
        else:
            for node in dfg.get_predecessors_of_activity(event.activity):
                if self.network.has_node(node):
                    print("Inbound activity")
                    current_conformance = self.network.send_message(node, "conformance_get", event.caseid)
                    break
        if not current_conformance:
            print("Start activity")
            current_conformance = SConformanceScore(
                path_length=0,
                conformance_violations=0
            )

        conformance_update = self.cpu.compute_conformance(dfg, last_activity, event.activity)
        conformance = SConformanceScore(
            path_length=current_conformance.path_length + conformance_update.path_length,
            conformance_violations=current_conformance.conformance_violations + conformance_update.conformance_violations
        )
        self.storage.update_conformance(
            event.caseid,
            SConformanceScore(
                conformance_violations=conformance.conformance_violations,
                path_length=conformance.path_length
            )
        )
        self.storage.update_last_event_of_case(event.caseid, event.activity)
        end = time.time()
        self.monitor.add_value("conformance_times", end - start)
        self.monitor.add_value("conformance", conformance.conformance_violations / conformance.path_length)
        return conformance

    def conformance_get(self, case_id):
        return self.storage.retrieve_conformance_values(case_id).conformance

    def get_directly_follows_graph(self, payload):
        return self.storage.get_directly_follows_graph()