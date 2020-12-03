import json

from copy_cat.parsers.json_parser import JSONParser
from copy_cat.parsers.xml_parser import XMLParser
from copy_cat.validators.validator import Validator


class CopyCat:
    def __init__(self):
        self.validator = Validator()
        self.errors = []

    def run(self, design, body):
        # TODO: Move to local_run
        # with open('resources/target_invoice_rsx.json', 'r') as file_data:
        #     design = json.load(file_data)

        # with open('resources/20013320221.dat', 'r') as file_data:
        #     test_data = main_(file_data)

        design = json.loads(design)
        self._add_locations(design)
        with open('tmp.xml', 'wb') as f:
            f.write(body)
        with open('tmp.xml', 'r') as f:
            test_data = XMLParser(f).parse()

        flatten_result = JSONParser(test_data).parse()

        self.validator.validate(flatten_result, design)
        self.errors = self.validator.errors

    def _add_locations(self, schema_object):
        for child in schema_object['children']:
            child['location'] = f'{schema_object.get("location", schema_object["name"])}/{child["name"]}'
            self._add_locations(child)
