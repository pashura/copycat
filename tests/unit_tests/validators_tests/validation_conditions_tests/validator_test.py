# from unittest.mock import Mock, call, patch
#
# from copy_cat.validators.validation_conditions.exceptions import UnsupportedValidationConditionTypeError
# from copy_cat.validators.validation_conditions.validator import ValidationConditionsValidator
# from tests.unit_tests.validators_tests.validation_conditions_tests import DummyValidator
#
#
# class TestValidationConditionsValidator:
#     def setup_method(self):
#         self.validator = ValidationConditionsValidator()
#         self.test_data = []
#
#     @patch.object(ValidationConditionsValidator, '_validate_conditions')
#     @patch.object(ValidationConditionsValidator, '_validate_children')
#     def test_validate(self, mock__validate_children, mock__validate_conditions):
#         mock_design_object = {'children': []}
#         self.validator.validate(mock_design_object, self.test_data)
#         mock__validate_conditions.assert_called_with(mock_design_object, self.test_data)
#         mock__validate_children.assert_called_with(mock_design_object['children'], self.test_data)
#
#     @patch.object(ValidationConditionsValidator, '_validate_conditions')
#     def test__validate_children(self, mock__validate_conditions):
#         mock_design_object = {'children': [{'name': 'first'}, {'name': 'second'}, {'name': 'third'}]}
#         self.validator._validate_children(mock_design_object['children'], self.test_data)
#
#         mock__validate_conditions.assert_has_calls(
#             [
#                 call(mock_design_object['children'][0], []),
#                 call(mock_design_object['children'][1], []),
#                 call(mock_design_object['children'][2], [])
#             ]
#         )
#
#     @patch.object(ValidationConditionsValidator, '_get_grouped_validation_conditions')
#     @patch('copy_cat.validators.validation_conditions.validator.validation_condition_factory')
#     def test__validate_conditions(
#             self, mock_validation_condition_factory, mock__get_grouped_validation_conditions
#     ):
#         validations = [{'type': 'Supported Type 1'}, {'type': 'Supported Type 2'}]
#         mock_design_object = {'visible': True, 'location': 'location', 'validation': validations}
#         mock_validator = DummyValidator()
#         mock_validator.validate = Mock()
#
#         mock__get_grouped_validation_conditions.return_value = {'Supported Type 1': [{1}], 'Supported Type 2': [{2}]}
#         mock_validation_condition_factory.side_effect = [mock_validator, UnsupportedValidationConditionTypeError()]
#
#         self.validator._validate_conditions(mock_design_object, self.test_data)
#
#         mock__get_grouped_validation_conditions.assert_called_with(validations)
#         mock_validation_condition_factory.assert_has_calls([call('Supported Type 1'), call('Supported Type 2')])
#         assert mock_validator.validate.mock_calls == [call([{1}], [], 'location')]
#
#     @patch.object(ValidationConditionsValidator, '_get_grouped_validation_conditions')
#     @patch('copy_cat.validators.validation_conditions.validator.validation_condition_factory')
#     def test__validate_conditions_design_object_is_not_visible(
#             self, mock_validation_condition_factory, mock__get_grouped_validation_conditions
#     ):
#         validations = [{'type': 'Supported Type 1'}, {'type': 'Supported Type 2'}]
#         mock_design_object = {'visible': False, 'location': 'location', 'validation': validations}
#
#         self.validator._validate_conditions(mock_design_object, self.test_data)
#
#         mock__get_grouped_validation_conditions.assert_not_called()
#         mock_validation_condition_factory.assert_not_called()
#
#     @patch.object(ValidationConditionsValidator, '_get_grouped_validation_conditions')
#     @patch('copy_cat.validators.validation_conditions.validator.validation_condition_factory')
#     def test__validate_conditions_no_validations(
#             self, mock_validation_condition_factory, mock__get_grouped_validation_conditions
#     ):
#         mock_design_object = {'visible': True, 'location': 'location'}
#
#         self.validator._validate_conditions(mock_design_object, self.test_data)
#
#         mock__get_grouped_validation_conditions.assert_not_called()
#         mock_validation_condition_factory.assert_not_called()
#
#     def test__get_grouped_validation_conditions(self):
#         mock_validation_condition = {'type': 'type', 'conditions': [], 'results': [], 'rules': []}
#         mock_validation_conditions = [
#             dict(mock_validation_condition, type='type1'),
#             dict(mock_validation_condition, type='type2'),
#             dict(mock_validation_condition, type='type2'),
#             dict(mock_validation_condition, type='type3'),
#             dict(mock_validation_condition, type='type3'),
#             dict(mock_validation_condition, type='type3'),
#         ]
#         actual = self.validator._get_grouped_validation_conditions(mock_validation_conditions)
#         assert len(actual) == 3
#         assert len(actual['type1']) == 1
#         assert len(actual['type2']) == 2
#         assert len(actual['type3']) == 3
