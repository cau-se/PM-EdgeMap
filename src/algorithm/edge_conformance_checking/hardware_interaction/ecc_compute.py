import heapq
import time

from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph
from s_conformance_score import SConformanceScore

class EdgeConformanceCheckingCompute:

    def __init__(self, compute):
        self.compute_time_metrics = []
        self.compute = compute

    def get_predecessor_node(self, last_event, nodes_with_timestamp_of_latest_event):
        start = time.time()

        if last_event:
            latest_timestamp = last_event.timestamp
        else:
            latest_timestamp = None

        predecessor_node = None
        if nodes_with_timestamp_of_latest_event:
            for node in nodes_with_timestamp_of_latest_event:
                timestamp = nodes_with_timestamp_of_latest_event[node]
                if self.compute.run(lambda: not latest_timestamp or timestamp > latest_timestamp):
                    latest_timestamp = timestamp
                    predecessor_node = node

        end = time.time()
        self.compute_time_metrics.append(end-start)
        print(f"get_predecessor_node: {end-start}")
        return predecessor_node

    def compute_conformance(self, directly_follows_graph: DirectlyFollowsGraph, last_activity, next_activity):
        start = time.time()
        if not last_activity:
            if next_activity in directly_follows_graph.start_activities:
                return SConformanceScore(path_length=1, conformance_violations=0)
            return SConformanceScore(path_length=1, conformance_violations=1)

        result = None
        if not self.has_item(directly_follows_graph, next_activity):
            return SConformanceScore(path_length=1, conformance_violations=1)
        else:
            shortest_path = self.get_path_to_activity(directly_follows_graph, last_activity, next_activity)
            if shortest_path:
                violations = len(shortest_path) - len({last_activity,next_activity})
            else:
                result = SConformanceScore(path_length=1, conformance_violations=1)
                return result
            if violations == 0:
                result =  SConformanceScore(path_length=1, conformance_violations=0)
                return result
            result = SConformanceScore(path_length=violations, conformance_violations=violations)

        end = time.time()

        self.compute_time_metrics.append(end-start)
        print(f"compute_conformance: {end-start}")
        return result

    def has_item(self, directly_follows_graph: DirectlyFollowsGraph, item):
        for dfr in directly_follows_graph.get_relations():
            if dfr.predecessor == item or dfr.successor == item:
                return True
        return False

    def get_neighbours(self, dfg: DirectlyFollowsGraph, pointer):
        neighbours = []
        for relation in dfg.get_relations():
            if relation.predecessor == pointer:
                neighbours.append(relation.successor)
        return neighbours

    def get_path_to_activity(self, dfg, pointer, target):
        if not self.has_item(dfg, pointer) or not self.has_item(dfg, target):
            return None  # One or both edges don't exist in the graph

        distances = {pointer: 0}
        priority_queue = [(0, pointer, [])]  # (distance, current_edge, path)

        while priority_queue:
            current_distance, current_edge, path = heapq.heappop(priority_queue)

            if current_edge == target:
                print(f"Path {path + [current_edge]}")
                return path + [current_edge]

            if current_distance > distances.get(current_edge, float('inf')):
                continue

            for neighbor_edge in self.get_neighbours(dfg, current_edge):
                distance = current_distance + 1
                if self.compute.run(lambda: distance < distances.get(neighbor_edge, float('inf'))):
                    distances[neighbor_edge] = distance
                    heapq.heappush(priority_queue, (distance, neighbor_edge, path + [current_edge]))
        return None
