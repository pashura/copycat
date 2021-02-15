from typing import List, Optional

from pydantic import Field

from copy_cat.models.base import BaseDesign


class DataObject(BaseDesign):
    type: Optional[str]
    name: Optional[str]
    value: Optional[str] = Field(alias='text')
    length: Optional[int]
    location: Optional[str]
    children: Optional[List['DataObject']]

    used: Optional[bool]
    index: Optional[int]


DataObject.update_forward_refs()
