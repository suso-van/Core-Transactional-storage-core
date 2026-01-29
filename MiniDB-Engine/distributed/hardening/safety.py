class SafetyManager:
    def validate_leader(self, leader, alive_nodes):
        return leader in alive_nodes

    def validate_replica_set(self, replicas):
        return len(replicas) > 0

    def validate_commit(self, quorum_ok, leader_ok):
        return quorum_ok and leader_ok
