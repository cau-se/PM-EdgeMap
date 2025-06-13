from hello_network import HelloNetwork

class ComputingTopology:

    def __init__(self):
        self.networks = dict()
        self.nodes = dict()
        self.network_address_resolution = HelloNetwork()

    def add_network(self, network_id, network):
        self.networks[network_id] = network

    def get_network(self, network_id):
        return self.networks[network_id]()

    def add_node(self, node_id, node):
        self.nodes[node_id] = node
        self.network_address_resolution.add_network_address(node_id, node.control_network.get_address())

    def get_node(self, node_id):
        return self.nodes[node_id]

    def get_nodes(self):
        return self.nodes.values()

    def deploy_algorithm(self, node_id, algorithm):
        algorithm.assign_to_node(self.nodes[node_id])

    def deploy_algorithm_on_nodes_with_category(self, category, algorithm):
        for node in self.get_nodes():
            if node.category == category:
                self.deploy(algorithm(), node.node_id)

    def deploy(self, algorithm, node_id):
        algorithm.run_on_node(self.nodes[node_id])

    def run(self, node_id):
        self.nodes[node_id].run()

    def run_all(self):
        for node in self.get_nodes():
            node.run()

    def monitor(self, event_delta, velocity):
        for node in self.get_nodes():
            node.run_monitor(event_delta, velocity)
        for node in self.get_nodes():
            node.reset_monitor()