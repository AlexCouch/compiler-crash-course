from dataclasses import dataclass
from typing import Optional

@dataclass
class CanonName:
    name: str
    parent: 'Optional[CanonName]'

    def __eq__(self, other):
        assert isinstance(other, 'CanonName')
        return self.str == other.str and self.parent == other.parent

    def __lt__(self, other):
        assert isinstance(other, 'CanonName')
        return self.parent == other

    def __gt__(self, other):
        assert isinstance(other, 'CanonName')
        return self == other.parent

    def __add__(self, other):
        assert isinstance(other, str)
        return CanonName(other, self)
