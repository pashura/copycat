import datetime

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

from copy_cat.utils import find_dictionary


class DataTypeValidator:
    def __init__(self):
        self.errors = []

    def validate(self, design_object, test_data_object):
        self.data_type_validator(design_object, test_data_object)

    def data_type_validator(self, design_object, test_data_object):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        expected_data_type = restriction_obj.get('displayName')

        #  Date/Time validator
        if expected_data_type in ['Date', 'Time']:
            date_data_type_ = self._get_date_format(test_data_object.get('text'))
            if date_data_type_ is None:
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> 'String'"
                self.errors.append({
                    "fieldName": test_data_object['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data_object["location"],
                    "error": error_message,
                })

        # Float validator
        if expected_data_type == 'Decimal':
            decimal_data_type_ = test_data_object.get('type').strip().replace("'", "")
            if decimal_data_type_ != 'float' and decimal_data_type_ != 'int':
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. " \
                                f"Found -> '{decimal_data_type_}'"
                self.errors.append({
                    "fieldName": test_data_object['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data_object["location"],
                    "error": error_message,
                })

        # Integer validator
        if expected_data_type == 'Integer':
            decimal_data_type_ = test_data_object.get('type').strip().replace("'", "")
            if decimal_data_type_ != 'int':
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. " \
                                f"Found -> '{decimal_data_type_}'"
                self.errors.append({
                    "fieldName": test_data_object['name'],
                    "fieldPath": design_object['location'],
                    "xpath": test_data_object["location"],
                    "error": error_message,
                })

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
        except (TypeError, ValueError, OverflowError, ParserError):
            pass
