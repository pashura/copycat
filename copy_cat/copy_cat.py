from typing import Dict, List

from copy_cat.core.transformer.transformer import Transformer
from copy_cat.core.validators.validator import Validator
from copy_cat.models.design import DesignObject
from copy_cat.models.test_data import DataObject
from copy_cat.parsers.json_parser import JSONParser
from copy_cat.parsers.xml_parser import XMLParser


class CopyCat:
    def __init__(self):
        self.validator = Validator()
        self.transformer = Transformer()

    def run(self, design: Dict, reversed_design: Dict, body: str) -> List:
        design = DesignObject(**design)
        reversed_design = DesignObject(**reversed_design)

        for des in [design, reversed_design]:
            self._add_locations(des)
            self._clean_up_invisible_nodes(des)

        self._add_parent_info(reversed_design)

        test_data = XMLParser().parse(body)

        flatten_result = [
            DataObject(**result) for result in JSONParser().parse(test_data)
        ]

        self.validator.validate(reversed_design, flatten_result)

        result = self.transformer.transform(design, reversed_design, flatten_result)
        return result

    def _add_parent_info(self, schema_object: DesignObject) -> None:
        for child in schema_object.children:
            child.parent = schema_object
            self._add_parent_info(child)

    def _add_locations(self, schema_object: DesignObject) -> None:
        for child in schema_object.children:
            prefix = schema_object.location or schema_object.name
            child.location = f"{prefix}/{child.name}" if child.name else prefix
            self._add_locations(child)

    def _clean_up_invisible_nodes(self, schema_object: DesignObject) -> None:
        for child in schema_object.children:
            if not child.visible:
                self.__clean_up_node_with_its_children(child)
            self._clean_up_invisible_nodes(child)

    def __clean_up_node_with_its_children(self, schema_object: DesignObject) -> None:
        schema_object.visible = False
        for child in schema_object.children:
            self.__clean_up_node_with_its_children(child)
