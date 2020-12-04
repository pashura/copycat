from copy_cat.models.error import Error
from copy_cat.utils import get_test_data_object


class AtLeastOneOfValidator:
    def __init__(self):
        self.errors = []

    def validate(self, validations: list, test_data: list, location: list):
        for validation in validations:
            conditions = validation['rules'][0]['conditions']
            satisfied = False
            for condition in conditions:
                test_data_obj = get_test_data_object(test_data, f'{location}/{condition["element"]}')
                if test_data_obj and (not condition['value'] or condition['value'] == test_data_obj.value):
                    satisfied = True
                    break

            if not satisfied:
                elements = [f'{el["element"]}{"=" + el["value"] if el["value"] else ""}' for el in conditions]
                error_message = f'At least one of {",".join(elements)} is required'
                self.errors.append(Error(fieldName="", fieldPath=location, xpath="", error=error_message))

        return self.errors
