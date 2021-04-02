from typing import List, Optional, Union, TypeVar, Generic

from pydantic import Field, StrictBool
from pydantic.generics import GenericModel

from copy_cat.models.base import BaseDesign

# TODO: TypeVar should be removed after getting rid of ParentObject
T = TypeVar("T")


class Attribute(BaseDesign):
    id: int
    element_type: str = Field(alias="elementType")
    base: Optional[str]
    display_name: Optional[str] = Field(alias="displayName")
    drop_extra_records: Optional[str] = Field(alias="dropExtraRecords")
    min_length: Optional[str] = Field(alias="minLength")
    max_length: Optional[str] = Field(alias="maxLength")
    has_enum: Optional[bool] = Field(alias="hasEnum")
    edi_id: Optional[str] = Field(alias="ediId")
    edi_data_type: Optional[str] = Field(alias="EDIDataType")


class Sourcing(BaseDesign):
    name: str
    location: str
    is_repeatable: Optional[StrictBool] = Field(alias="isRepeatable")
    has_enum: StrictBool = Field(alias="hasEnum")
    documentation: Optional[str] = Field(min_length=-1)

    @property
    def parent_name(self) -> str:
        return self.location.split("/")[-2]

    @property
    def is_composite(self) -> bool:
        return "Composite" in self.parent_name

    @property
    def record_name(self):
        return self.location.split("/")[-3 if self.is_composite else -2]


class QualifierCondition(BaseDesign):
    converts: str
    custom_description: Optional[str] = Field(alias="customDescription")
    qualifier: str
    min_occurs: Union[int, str] = Field(alias="minOccurs")


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
    hidden_schema: HiddenSchema = Field(alias="hiddenSchema")
    viewed_schema: ViewedSchema = Field(alias="viewedSchema")
    reversed: Optional[bool]


class DesignObject(GenericModel, Generic[T]):
    id: int
    element_type: str = Field(alias="elementType")
    min_occurs: str = Field(alias="minOccurs")
    max_occurs: Optional[str] = Field(alias="maxOccurs")
    has_enum: bool = Field(alias="hasEnum")
    visible: bool
    children: List["DesignObject"]
    attributes: List[Attribute]
    name: str
    sourcing: Optional[Sourcing]
    qualifiers: Optional[str]

    conditional_sourcing: Optional[List] = Field(alias="conditionalSourcing")
    validation: Optional[List] = []
    design_meta: Optional[DesignMeta] = Field(alias="designMeta")
    suffix: Optional[str]

    location: Optional[str]
    skip_children: Optional[str] = Field(alias="skipChildren")
    parent: Optional["ParentObject[T]"]

    @property
    def restriction(self) -> Attribute or None:
        return next(
            (dic for dic in self.attributes if dic.element_type == "restriction"), None
        )

    def get_child_by_location(self, path: str) -> "DesignObject" or None:
        for element in path.split("/"):
            if not (self := self.__find_child(element)):
                break
        return self

    def __find_child(self, name: str) -> "DesignObject":
        for child in self.children:
            if (
                child.name if not child.suffix else (child.name + child.suffix)
            ) == name:
                return child


class ParentObject(DesignObject, GenericModel, Generic[T]):
    children: Union["T", "DesignObject[T]"]


DesignObject.update_forward_refs()
ParentObject.update_forward_refs()
