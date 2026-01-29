import random
import string

class WorkloadGenerator:
    def __init__(self, size=100):
        self.size = size

    def random_key(self):
        return "key_" + "".join(random.choices(string.ascii_lowercase, k=6))

    def random_value(self):
        return "val_" + "".join(random.choices(string.ascii_letters, k=10))

    def operations(self):
        for _ in range(self.size):
            yield {
                "key": self.random_key(),
                "value": self.random_value()
            }
