class QueryExecutor:
    def __init__(self, storage_manager, index_manager, wal_manager):
        self.storage = storage_manager
        self.index = index_manager
        self.wal = wal_manager

    def execute(self, plan, transaction):
        if plan.op_type == "INSERT":
            return self._insert(plan, transaction)
        elif plan.op_type == "GET":
            return self._get(plan, transaction)
        elif plan.op_type == "SCAN":
            return self._scan(plan, transaction)
        elif plan.op_type == "DELETE":
            return self._delete(plan, transaction)
        else:
            raise ValueError("UNKNOWN QUERY TYPE")

    # -------- Operations --------

    def _insert(self, plan, tx):
        # allocate storage page
        page = self.storage.allocate_page(page_type=2)

        # write value
        tx.write(page, 0, str(plan.value).encode())

        # index insert
        self.index.insert(tx.txid, plan.key, page.page_id)

        return True

    def _get(self, plan, tx):
        page_id = self.index.search(plan.key)
        if page_id is None:
            return None

        page = self.storage.fetch_page(page_id)
        data = tx.read(page, 0, 256)
        return data.rstrip(b"\x00")

    def _scan(self, plan, tx):
        results = []
        node = self.index.tree.root

        # go to leftmost leaf
        while not node.is_leaf:
            node = node.children[0]

        while node:
            for val in node.values:
                page = self.storage.fetch_page(val)
                data = tx.read(page, 0, 256)
                results.append(data.rstrip(b"\x00"))
            node = node.next

        return results

    def _delete(self, plan, tx):
        page_id = self.index.search(plan.key)
        if page_id is None:
            return False

        page = self.storage.fetch_page(page_id)
        tx.write(page, 0, b"\x00" * 256)   # logical delete
        return True
