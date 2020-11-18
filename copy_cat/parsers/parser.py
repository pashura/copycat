import datetime

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

from copy_cat.utils import find_dictionary, traverse_path_in_schema_object


class Parser:
    def __init__(self):
        self.errors = []

    def process(self, test_data, schema):
        for ind, t in enumerate(test_data):
            location = t.get('location')[9:]
            location, reps = self.get_reps_and_location(location)

            el = traverse_path_in_schema_object(schema, location)
            if not el:
                print(location + " is not in design")
            else:
                self.length_validator(el, t)
                self.data_type_validator(el, t)
                self.choices_validator(el, t)
        self.requirements_validator(test_data, schema)

    @staticmethod
    def get_reps_and_location(location):
        reps = []
        new_paths = []
        paths = location.split('/')
        for path in paths:
            if '[' in path:
                reps.append({
                    "rep_name": path.split('[')[0],
                    "rep_number": path.split('[')[1][:1]
                })
            new_paths.append(path.split('[')[0])
        return '/'.join(new_paths), reps

    @staticmethod
    def _get_date_format(date_string: str) -> datetime:
        try:
            parsed_date = parse_date(date_string)
            curr_datetime = datetime.datetime.now()
            if str(parsed_date.time()) == '00:00:00':
                return datetime.date
            elif parsed_date.date() == curr_datetime.date():
                return datetime.time
            return datetime.datetime
        except (TypeError, ValueError, OverflowError, ParserError) as e:
            # print(e)
            # raise ValueError
            pass

    def length_validator(self, design_object, test_data):
        BIG_NUMBER = "2222222222"
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        if int(restriction_obj.get('maxLength', BIG_NUMBER)) < int(test_data.get('length')):
            error = str(f'Given data: \'{test_data.get("text")}\' with length ' +
                        str(test_data.get('length'))) + ' is bigger then max length of the element: ' + \
                    design_object.get('attributes', [])[0].get('maxLength', BIG_NUMBER)
            self.errors.append({
                "fieldName": test_data['name'],
                "fieldPath": design_object['location'],
                "xpath": test_data["location"],
                "error": error,
            })

    def data_type_validator(self, design_object, test_data):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        expected_data_type = restriction_obj.get('displayName')

        #  Date validator
        if expected_data_type == 'Date':
            date_data_type_ = self._get_date_format(test_data.get('text'))
            if date_data_type_ is None:
                error = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> 'String'"
                self.errors.append({
                    "fieldName": test_data['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data["location"],
                    "error": error,
                })

        #  Time validator
        if expected_data_type == 'Time':
            date_data_type_ = self._get_date_format(test_data.get('text'))
            if date_data_type_ is None:
                error = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> 'String'"
                self.errors.append({
                    "fieldName": test_data['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data["location"],
                    "error": error,
                })

        # Float validator
        if expected_data_type == 'Decimal':
            decimal_data_type_ = test_data.get('type').strip().replace("'", "")
            if decimal_data_type_ != 'float' and decimal_data_type_ != 'int':
                error = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> '{decimal_data_type_}'"
                self.errors.append({
                    "fieldName": test_data['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data["location"],
                    "error": error,
                })

        # Integer validator
        if expected_data_type == 'Integer':
            decimal_data_type_ = test_data.get('type').strip().replace("'", "")
            if decimal_data_type_ != 'int':
                error = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> '{decimal_data_type_}'"
                self.errors.append({
                    "fieldName": test_data['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data["location"],
                    "error": error,
                })

    def choices_validator(self, design_object, test_data):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        if restriction_obj.get('displayName') == 'StringSet':

            quals = design_object.get("qualifiers", '').split(',')
            quals = [i.strip() for i in quals]
            if test_data.get('text') not in quals and not restriction_obj.get("dropExtraRecords") \
                    and restriction_obj.get('displayName') == 'StringSet':
                error = f" Qualifier {test_data.get('text')} is not valid. Possible choices -> {quals}"
                self.errors.append({
                    "fieldName": test_data['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data["location"],
                    "error": error,
                })

    def requirements_validator(self, test_data, schema):
        for child in schema['children']:
            if child.get('visible') is True and child.get('minOccurs') == '1' and not child.get('children'):
                test_data_obj = next((i for i in test_data if i["location"].removeprefix("/").replace('[', "").replace(']', "").replace('1', "").replace('2', "").replace('3', "")
                                      == child.get('location')), None)
                if not test_data_obj:
                    error = f"Missing mandatory {child['name']} in {schema['name']} record"
                    self.errors.append({
                        "fieldName": "",
                        "fieldPath": child['location'],
                        "xpath": "",
                        "error": error,
                    })
            self.requirements_validator(test_data, child)
