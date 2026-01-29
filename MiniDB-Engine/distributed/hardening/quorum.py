class QuorumManager:
    def __init__(self, replication_factor=3):
        self.replication_factor = replication_factor

    def write_quorum(self):
        # majority quorum
        return (self.replication_factor // 2) + 1

    def read_quorum(self):
        return (self.replication_factor // 2) + 1

    def check_write(self, acks):
        return acks >= self.write_quorum()

    def check_read(self, responses):
        return responses >= self.read_quorum()
