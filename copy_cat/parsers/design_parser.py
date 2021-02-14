class DesignParser:
    def __init__(self):

        self.result = []

    def parse(self, design_data: dict, test_data):
        self._parse_design(design_data, test_data)

    def _parse_design(self, design: dict, test_data):
        design_fields = {}
        self._parse_children(design, design_fields, test_data)

    def _parse_children(self, current_element: dict, design_fields: dict, test_data, group_path: str = ''):
        pass

    def _parse_group(self, group: dict, test_data):
        pass

    def _parse_field(self, field_: dict, field_path, test_data):
        pass


