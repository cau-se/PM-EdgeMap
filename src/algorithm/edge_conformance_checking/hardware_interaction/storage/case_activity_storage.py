from process_mining_core.datastructure.core.SEvent import SEvent
from process_mining_core.datastructure.core.event import Event

class CaseActivityStorage:

    def __init__(self, storage=dict()):
        self.storage = storage

    def get_activity_of_case(self, case_id):
        if case_id in self.storage:
            #return self.storage[case_id]
            return self.storage.get_item(case_id, SEvent)
        return None

    def store_event_for_case(self, event: Event):
        self.storage[event.caseid] = event
