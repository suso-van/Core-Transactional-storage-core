class FailureDomainManager:
    def __init__(self):
        self.domains = {}  # node_id -> domain

    def assign_domain(self, node_id, domain):
        self.domains[node_id] = domain

    def domain_of(self, node_id):
        return self.domains.get(node_id, "default")

    def validate_replication(self, nodes):
        domains = set(self.domain_of(n) for n in nodes)
        return len(domains) > 1  # multi-domain replication
