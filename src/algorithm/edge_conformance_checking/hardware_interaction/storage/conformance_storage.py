from src.algorithm.data_structures.conformance_score import SConformanceScore
from src.algorithm.data_structures.conformance_values import SConformanceValues

class ConformanceStorage:
    def __init__(self, storage):
        self.storage = storage

    def store_conformance_values(self, conformance_values: SConformanceValues):
        self.storage[conformance_values.case_id] = conformance_values

    def retrieve_conformance_values(self, case_id):
        if case_id in self.storage:
            return self.storage.get_item(case_id, SConformanceValues)
        return SConformanceValues(case_id=case_id, last_activity=None, conformance=SConformanceScore(conformance_violations=0, path_length=0))

    def update_last_event_of_case(self, case_id, activity):
        conformance_values: SConformanceValues = self.retrieve_conformance_values(case_id)
        if conformance_values:
            self.store_conformance_values(SConformanceValues(case_id=case_id, last_activity=activity, conformance=conformance_values.conformance))
        else:
            self.store_conformance_values(SConformanceValues(case_id=case_id, last_activity=activity, conformance=SConformanceScore(conformance_violations=0, path_length=0)))

    def update_conformance(self, case_id, conformance):
        conformance_values: SConformanceValues = self.retrieve_conformance_values(case_id)
        if conformance_values:
            self.store_conformance_values(SConformanceValues(case_id=case_id, last_activity=conformance_values.last_activity, conformance=conformance))
        else:
            self.store_conformance_values(SConformanceValues(case_id=case_id, last_activity="", conformance=conformance))
