from process_mining_core.datastructure.core.counted_directly_follows_relation import CountedDirectlyFollowsRelation
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph
from src.algorithm.data_structures.conformance_values import SConformanceValues
from src.algorithm.edge_conformance_checking.hardware_interaction.storage.border_activity_storage import \
    BorderActivityStorage
from src.algorithm.edge_conformance_checking.hardware_interaction.storage.case_activity_storage import \
    CaseActivityStorage
from src.algorithm.edge_conformance_checking.hardware_interaction.storage.conformance_storage import ConformanceStorage


class EdgeConformanceCheckingStorage:

    def __init__(self, storage_df, storage_case, storage_conformance):
        self.directly_follows_storage: CountedDirectlyFollowsRelation = CountedDirectlyFollowsRelation(storage_df)
        self.case_activity_storage: CaseActivityStorage = CaseActivityStorage(storage_case)
        self.conformance_storage: ConformanceStorage = ConformanceStorage(storage_conformance)
        self.end_activity_storage: BorderActivityStorage = BorderActivityStorage(set())
        self.start_activity_storage: BorderActivityStorage = BorderActivityStorage(set())

    def store_start_activity(self, start_activity):
        self.start_activity_storage.store_activity(start_activity)

    def store_end_activity(self, end_activity):
        self.start_activity_storage.store_activity(end_activity)

    def store_event_for_case(self, event):
        self.case_activity_storage.store_event_for_case(event)

    def store_conformance_values(self, case_id, last_activity, current_conformance):
        self.conformance_storage.store_conformance_values(SConformanceValues(case_id=case_id, last_activity=last_activity, conformance=current_conformance))

    def update_conformance(self, case_id, conformance):
        self.conformance_storage.update_conformance(case_id, conformance)

    def update_last_event_of_case(self, case_id, activity):
        self.conformance_storage.update_last_event_of_case(case_id, activity)

    def retrieve_conformance_values(self, case_id):
        return self.conformance_storage.retrieve_conformance_values(case_id)

    def get_activity_of_case(self, case_id):
        return self.case_activity_storage.get_activity_of_case(case_id)

    def get_directly_follows_graph(self):
        return DirectlyFollowsGraph(self.directly_follows_storage, self.start_activity_storage.retrieve_activities(), self.end_activity_storage.retrieve_activities())

    def get_directly_follows_relations(self):
        return self.directly_follows_storage.keys()

    def store_directly_follows_relation(self, directly_follows_relation):
        self.directly_follows_storage.insert(directly_follows_relation)

    def store_conformance_of_case(self, payload):
        super().store_conformance_of_case(payload)


