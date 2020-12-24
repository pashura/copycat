import json

from copy_cat.models.test_data import DataObject
from copy_cat.parsers.json_parser import JSONParser
from copy_cat.parsers.xml_parser import XMLParser
from copy_cat.validators.validator import Validator


class CopyCat:
    def __init__(self):
        self.validator = Validator()

    def run(self, design, body):
        # TODO: Move to local_run
        # with open('resources/target_invoice_rsx.json', 'r') as file_data:
        #     design = json.load(file_data)

        # with open('resources/company_target-Invoice-RSX-test-2.xml', 'r') as file_data:
        #     test_data = main_(file_data)

        design =  json.loads(design)
        self._add_locations(design)
        self._add_parent_info(design)
        self._clean_up_invisible_nodes(design)
        with open('tmp.xml', 'wb') as f:
            f.write(body)
        with open('tmp.xml', 'r') as f:
            test_data = XMLParser(f).parse()

        flatten_result = [DataObject(**result) for result in JSONParser(test_data).parse()]

        self.validator.validate(design, flatten_result)

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

