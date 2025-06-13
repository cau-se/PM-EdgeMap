import json
from time import sleep

from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from hello_topology import HelloTopology
from node_sink import NodeSink
from topology_factory import TopologyFactory
from topology_monitor import TopologyMonitor

class Simulator:
    def __init__(self, topology_directory, result_directory):
        self.topology_directory = topology_directory
        self.result_directory = result_directory
        self.topology_monitor: TopologyMonitor = TopologyMonitor()
        self.topology: HelloTopology = None

    def run(self, algorithm, topology_key, metric_name, metrics, velocity=100, evaluation_batch=100):
        self.velocity = velocity
        self.evaluation_batch = evaluation_batch
        self.topology = TopologyFactory(
            f"{self.topology_directory}/{topology_key}.yaml",
            self.topology_monitor).parse()
        self.topology.deploy_algorithm_on_nodes_with_category("edge", algorithm)
        self.topology.run_all()
        self._run_event_factory(self.topology)
        result = self.topology_monitor.get_summed_average_metrics(metrics)

        with open(f"{self.result_directory}/{metric_name}-{topology_key}.txt", 'w+') as filehandle:
            json.dump(result, filehandle)

    def _run_event_factory(self, topology):
        sleep(1)
        content_root = "../EventFactoryConfigs"
        event_factory = EventFactory()
        event_factory \
            .add_file(f"{content_root}/simulation/countbased.yaml") \
            .add_process_simulator(XesProcessSimulator(f"{content_root}/MainProcess.xes"))
            #.add_directory(f"{content_root}/datasource/assemblyline") \
        # .add_process_simulator(DefProcessSimulator(dict(), IncreasingCaseIdProvider(), ConstantCountProvider(1)))

        sinks = []
        for node in topology.get_nodes():
            sink = NodeSink(node, node.datasources)
            sinks.append(sink)
            event_factory.add_sink(
                node.node_id,
                sink
            )
        event_factory.run(self._hook)

    def _hook(self, i):
        if i % self.evaluation_batch == 0:
            self.topology.monitor(1, velocity=self.velocity)
