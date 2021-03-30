import json
import os
import unittest

from copy_cat.copy_cat import CopyCat
from tests.integration_tests import RESOURCES_DIR_TARGET_INVOICE


def pre_load_data(resource_directory):
    data = tuple()
    file_names = ('design.json', 'reversed_design.json', 'rsx_test_data_failed.xml', 'rsx_test_data_passed.xml',
                  'errors.json', 'transform_result.feds')
    for file_name in file_names:
        with open(os.path.join(resource_directory, file_name), 'rb' if file_name.endswith('.xml') else 'r') as f:
            data += (f.read(),)

    return data


class IntegrationTestRun(unittest.TestCase):
    RESOURCES_DIR = ''

    def __init__(self, *args, **kwargs):
        super(IntegrationTestRun, self).__init__(*args, **kwargs)

    def test_run(self):
        if not self.RESOURCES_DIR:
            return
        data = pre_load_data(self.RESOURCES_DIR)

        cc = CopyCat()
        cc.run(data[0], data[1], data[2])
        assert json.loads(data[4]) == cc.validator.errors_container.errors()
        cc.validator.errors_container.clean()

        cc = CopyCat()
        cc.run(data[0], data[1], data[3])
        # assert [] == cc.validator.errors_container.errors()
        self.assertEqual([], cc.validator.errors_container.errors())
        assert data[5] == '\n'.join(cc.transformer.transformation_result)
        # assert data[5] == cc.transformer.result


class IntegrationTestRunTargetInvoice(IntegrationTestRun):
    RESOURCES_DIR = RESOURCES_DIR_TARGET_INVOICE


if __name__ == '__main__':
    unittest.main()
