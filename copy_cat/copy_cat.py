import json

from copy_cat.parsers.json_parser import JSONParser
from copy_cat.parsers.xml_parser import XMLParser
from copy_cat.services.td_service import TDService


def add_locations(schema_object):
    for child in schema_object['children']:
        child['location'] = f'{schema_object.get("location", schema_object["name"])}/{child["name"]}'
        add_locations(child)


def main_run(ps, token, org_id, design_name, body):
    # with open('resources/target_invoice_rsx.json', 'r') as file_data:
    #     design = json.load(file_data)

    # with open('resources/20013320221.dat', 'r') as file_data:
    #     test_data = main_(file_data)

    td_service = TDService('test', token)
    design = td_service.get_reversed_design(org_id, design_name)
    design = json.loads(design)
    add_locations(design)
    with open('tmp.xml', 'wb') as f:
        f.write(body)
    with open('tmp.xml', 'r') as f:
        test_data = XMLParser(f).parse()

    flatten_result = JSONParser(test_data).parse()

    ps.validate(flatten_result, design)
    # try:
    #     a = DesignObject.parse_obj(design)
    # except ValidationError as e:
    #     print(e)
