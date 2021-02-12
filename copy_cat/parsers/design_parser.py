import re


class DesignParser:
    def __init__(self):

        self.result = []

    def parse(self, design_data: dict, test_data):
        self._parse_design(design_data, test_data)

    def _parse_design(self, design: dict, test_data):
        design_fields = {}
        self._parse_children(design, design_fields, test_data)

    def _parse_children(self, current_element: dict, design_fields: dict,
                        test_data, group_path: str = ''):
        for child in current_element.get('children', []):
            if child.get('visible'):
                child_name = child.get('name') or child.get('ref')
                if child.get('children', []):
                    new_group_path = child_name if not group_path else f'{group_path}/{child_name}'
                    self._parse_children(child, design_fields,
                                         test_data, new_group_path)
                    # self._parse_group(child, test_data)
                else:
                    field_path = child_name if not group_path else f"{group_path}/{child_name}"
                    self._parse_field(child, field_path, test_data)

        # self._parse_conditional_sources(
        #     current_element.get('conditionalSourcing', []), group_path, design_fields
        # )

    def _parse_group(self, group: dict, test_data):
        for test_data_obj in test_data:
            for child in group.get('children', []):
                if not child.get('children'):
                    sourcing = child.get('sourcing', {}).get('location', '')

                    # self._parse_field(child, '', test_data)


                    if not test_data_obj.used and re.sub('\[[0-9]\]+', '', test_data_obj.location.removeprefix('/')) == sourcing:
                        test_data_obj.used = True
                        self.result.append(test_data_obj)
                        continue

        # self._process_group_info(group)

    def _parse_field(self, field_: dict, field_path, test_data):
        # restriction = self._get_restriction(field)
        sourcing = field_.get('sourcing', {}).get('location', '')
        if sourcing:

            # '/Invoice/LineItem[1]/ChargesAllowances[2]/AllowChrgIndicator'

            valid = next((test_data_obj for test_data_obj in test_data
                          if test_data_obj.location.removeprefix('/') == sourcing and
                          not test_data_obj.used), None)

            if valid:
                valid.used = True
                self.result.append(valid)
            else:
                print(sourcing)
                valid = next(
                    (test_data_obj for test_data_obj in test_data
                     if not test_data_obj.used
                     and re.sub('\[[0-9]\]+', '', test_data_obj.location.removeprefix('/')) == sourcing
                     ), None)
                if valid:
                    # print(valid)
                    valid.used = True
                    self.result.append(valid)


