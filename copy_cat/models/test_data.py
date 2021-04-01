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

    @property
    def no_root_location(self):
        return '/'.join(self.location.split('/')[2:])


DataObject.update_forward_refs()
