from pydantic import Field, StrictBool, root_validator
from typing import List, Optional, Union

from models.base import BaseDesign


class Attribute(BaseDesign):
    id: int
    element_type: str = Field(alias='elementType')
    base: str
    display_name: str = Field(alias='displayName')
    min_length: Optional[str] = Field(alias='minLength')
    max_length: Optional[str] = Field(alias='maxLength')
    has_enum: Optional[bool] = Field(alias='hasEnum')
    edi_id: Optional[str] = Field(alias='ediId')
    edi_data_type: Optional[str] = Field(alias='EDIDataType')


class Sourcing(BaseDesign):
    name: str
    location: str
    is_repeatable: Optional[StrictBool] = Field(alias='isRepeatable')
    has_enum: StrictBool = Field(alias='hasEnum')
    documentation: Optional[str] = Field(min_length=-1)


class QualifierCondition(BaseDesign):
    converts: str
    custom_description: Optional[str] = Field(alias='customDescription')
    qualifier: str
    min_occurs: Union[int, str] = Field(alias='minOccurs')


class HiddenSchema(BaseDesign):
    source: bool
    version: str
    document: str
    format: str


class ViewedSchema(BaseDesign):
    source: bool
    version: str
    document: str
    format: str


class DesignMeta(BaseDesign):
    hidden_schema: HiddenSchema = Field(alias='hiddenSchema')
    viewed_schema: ViewedSchema = Field(alias='viewedSchema')
    reversed: bool


class DesignObject(BaseDesign):
    id: int
    element_type: str = Field(alias='elementType')
    min_occurs: str = Field(alias='minOccurs')
    has_enum: bool = Field(alias='hasEnum')
    visible: bool
    children: List['DesignObject']
    attributes: List[Attribute]
    name: str
    sourcing: Optional[Sourcing]
    qualifiers: Optional[str]

    conditional_sourcing: Optional[List] = Field(alias='conditionalSourcing')
    validation: Optional[List]
    max_occurs: Optional[str] = Field(alias='maxOccurs')
    design_meta: Optional[DesignMeta] = Field(alias='designMeta')

    location: Optional[str]

    # # this is required to prevent RecursionError in pydantic;
    # class Config:
    #     validate_assignment_exclude = "parent"
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # Add this Item as a child of its parent
    #     parent = kwargs.get("parent", None)
    #     if parent:
    #         parent.append_child(self)
    #
    #     # Add this Item as a parent of its child
    #     for c in kwargs.get("children", []):
    #         self.append_child(c, self.path, kwargs.get('name'))

    # def __contains__(self, item):
    #     """Recursive containment."""
    #     for c in self.children:
    #         if item == c or item in c:
    #             return True

    # def __iter__(self, recurse=True):
    #     yield self
    #     for c in self.children:
    #         yield c
    #         yield from iter(c)

    # @property
    # def hierarchical_id(self):
    #     return (f"{self.parent.id}." if self.parent else "") + str(self.id)

    # def append_child(self, other, path, parent_name):
    #     # if other not in self.children:
    #     #     self.children.append(other)
    #     # print(self)
    #     # path.append[self.name]
    #     current = f'{parent_name}/{other.get("name")}'
    #     if len(path):
    #         print(current)
    #         if current.startswith(path[-1]):
    #             # path = path[:-1]
    #             path.append(other.get("name"))
    #             print('/'.join(path))
    #     else:
    #         path.append(current)
    #

        # if len(path):
        #     path.append('/'.join(path) + f'{parent_name}/{other.get("name")}')
        # else:
        #     path.append(f'{parent_name}/{other.get("name")}')
        # path.append(other.get('name'))
        # print(path)
        # other['parent'] = self

    # def get_child(self, id_):
    #     """Return the child with the given *id*."""
    #     for c in self.children:
    #         if c.id == id_:
    #             return c
    #     raise ValueError(id_)

    # @property
    # def gid(self):
    #     return f"{self.name}/{self.name}"

    # @root_validator(pre=True)
    # def extract_foo(cls, v):
    #     return v['children']


DesignObject.update_forward_refs()
