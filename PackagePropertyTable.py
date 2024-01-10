class PackagePropertyTable:
    def __init__(self, size):
        self.table = {}
        self.size = size

    def create(self, key, value):
        if key not in self.table:
            self.table[key] = [value]
        else:
            self.table[key].append(value)

    def read(self, key):
        if key in self.table:
            return self.table[key]
        else:
            print("No packages found for address, do nothing.")
            return []

    def delete(self, key):
        if key in self.table:
            del self.table[key]