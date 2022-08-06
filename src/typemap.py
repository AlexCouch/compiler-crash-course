from dataclasses import dataclass

@dataclass
class Type:
    name: str

class TypeMap:
    def __init__(self):
        self.__type_map = {}
