from typing import List, Optional, Union

from copy_cat.models.base import BaseDesign
from pydantic import Field, StrictBool


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


DesignObject.update_forward_refs()
