class ConsistencyModel:
    STRONG = "STRONG"
    EVENTUAL = "EVENTUAL"
    CAUSAL = "CAUSAL"

class ConsistencyManager:
    def __init__(self, model=ConsistencyModel.STRONG):
        self.model = model

    def validate_read(self, quorum_ok):
        if self.model == ConsistencyModel.STRONG:
            return quorum_ok
        return True

    def validate_write(self, quorum_ok):
        if self.model == ConsistencyModel.STRONG:
            return quorum_ok
        return True
