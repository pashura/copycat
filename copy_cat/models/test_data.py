from typing import List, Optional, Union

from copy_cat.models.base import BaseDesign


class TestDataObject(BaseDesign):
    attributes: Optional[dict]
    text: Optional[str]
    length: Optional[int]
    type: Optional[str]
    location: Optional[str]
    children: Optional[List['TestDataObject']]


TestDataObject.update_forward_refs()
