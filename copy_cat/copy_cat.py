import json

from copy_cat.core.transformer.transformer import Transformer
from copy_cat.models.test_data import DataObject
from copy_cat.parsers.json_parser import JSONParser
from copy_cat.parsers.xml_parser import XMLParser
from copy_cat.core.validators.validator import Validator


class CopyCat:
    def __init__(self):
        self.validator = Validator()
        self.transformer = Transformer()

    def run(self, design, reversed_design, body):
        design = json.loads(design)
        reversed_design = json.loads(reversed_design)
        self._add_locations(design)
        self._add_locations(reversed_design)
        self._add_parent_info(reversed_design)
        self._clean_up_invisible_nodes(design)
        self._clean_up_invisible_nodes(reversed_design)

        test_data = XMLParser().parse(body)

        flatten_result = [DataObject(**result) for result in JSONParser().parse(test_data)]

        self.validator.validate(reversed_design, flatten_result)
        self.transformer.transform(design, reversed_design, flatten_result)

    def _add_parent_info(self, schema_object):
        for child in schema_object['children']:
            child['parent'] = schema_object
            self._add_parent_info(child)

    def _add_locations(self, schema_object):
        for child in schema_object['children']:
            child['location'] = f'{schema_object.get("location", schema_object["name"])}/{child["name"]}'
            self._add_locations(child)

    def _clean_up_invisible_nodes(self, schema_object):
        for child in schema_object.get("children", []):
            if not child.get("visible"):
                self.__clean_up_node_with_its_children(child)
            self._clean_up_invisible_nodes(child)

    def __clean_up_node_with_its_children(self, schema_object):
        schema_object["visible"] = False
        for child in schema_object.get("children", []):
            self.__clean_up_node_with_its_children(child)

