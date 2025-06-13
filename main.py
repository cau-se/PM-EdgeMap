from src.algorithm.edge_conformance_checking.ecc_algorithm import EdgeConformanceCheckingAlgorithm
from src.simulation.simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator(
        topology_directory="topology",
        result_directory="results"
    )

    simulator.run(
        algorithm=lambda: EdgeConformanceCheckingAlgorithm(learning_events=100),
        topology_key="mec",
        metric_name="bla",
        metrics=["data-network-resource"],
        velocity=100,
        evaluation_batch=100
    )