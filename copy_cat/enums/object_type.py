from enum import Enum


class ObjectType(Enum):
    ELEMENTS = 'elements'
    ELEMENT = 'element'
    SEGMENT = 'segment'

    def __str__(self):
        return str(self.value)
