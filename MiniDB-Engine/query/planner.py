class QueryPlan:
    def __init__(self, op_type, key=None, value=None):
        self.op_type = op_type   # INSERT, GET, SCAN, DELETE
        self.key = key
        self.value = value

class QueryPlanner:
    def plan_insert(self, key, value):
        return QueryPlan("INSERT", key=key, value=value)

    def plan_get(self, key):
        return QueryPlan("GET", key=key)

    def plan_scan(self):
        return QueryPlan("SCAN")

    def plan_delete(self, key):
        return QueryPlan("DELETE", key=key)
