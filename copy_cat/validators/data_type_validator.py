import datetime

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

from copy_cat.models.error import Error
from copy_cat.utils import find_dictionary
from copy_cat.validators.abstract_validator import AbstractValidator


class DataTypeValidator(AbstractValidator):
    def validate(self, design_object, test_data_object):
        self.data_type_validator(design_object, test_data_object)

    def data_type_validator(self, design_object, test_data_object):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        expected_data_type = restriction_obj.get('displayName')
        error_message = ''
        # TODO: Fix error messages to be similar to web xd

        #  Date/Time validator
        if expected_data_type in ['Date', 'Time']:
            data_type_ = self._get_date_format(test_data_object.value)
            if data_type_ == 'String':
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> '{data_type_}'"

        # Float validator
        if expected_data_type == 'Decimal':
            data_type_ = test_data_object.type
            if data_type_ != 'float' and data_type_ != 'int':
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> '{data_type_}'"

        # Integer validator
        if expected_data_type == 'Integer':
            data_type_ = test_data_object.type
            if data_type_ != 'int':
                error_message = f"DataType is incorrect. Should be -> '{expected_data_type}'. Found -> '{data_type_}'"

        if error_message:
            self.errors_container.append(Error(fieldName=test_data_object.name,
                                               designPath=design_object['location'],
                                               xpath=test_data_object.location,
                                               errorMessage=error_message))

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
            return 'String'
