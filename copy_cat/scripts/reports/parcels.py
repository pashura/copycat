import json
import time
from collections import defaultdict, Counter

import xlsxwriter

from copy_cat.copy_cat import CopyCat
from copy_cat.services.parcel_service import ParcelService


def _parse_data(data):
    result_ = []

    for key1, value1 in data.items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                result_.append({
                    'parcel_uid': value3,
                    'company_name': key1
                })
    return result_


def make_report(design, reversed_design, data):
    cc = CopyCat()
    ps = ParcelService()

    parcels = _parse_data(data)
    for index, parcel in enumerate(parcels):
        # if index == 20:
        #     break
        try:
            test_data = ps.get_parcel_data(parcel['parcel_uid'])
            cc.run(design, reversed_design, test_data)
            if len(cc.validator.errors_container.errors()):
                parcel.update(errors=cc.validator.errors_container.errors())
        except Exception as e:
            print(e)
        finally:
            cc.validator.errors_container.clean()
    result = [p for p in parcels if p.get('errors')]

    d = defaultdict(list)
    for r in result:
        for e in r['errors']:
            for k, v in e.items():
                if k == 'errorMessage':
                    value = f'{e.get("designPath", "")}  ~  {v}'
                    d[value].append(r['parcel_uid'])

    report_ = []
    for k, v in d.items():
        report_.append({
            'designPath': k.split('~')[0].strip(),
            'error': k.split('~')[1].strip(),
            'parcels': v,
            'count': len(v)
        })
    return report_


def load_to_xslx(filename_, result_):
    print()
    print('Loading data to excel...')
    start_time = time.time()

    workbook = xlsxwriter.Workbook(filename_)
    worksheet = workbook.add_worksheet()

    worksheet.write(f'A1', 'Error')
    worksheet.write(f'B1', 'Count')
    worksheet.write(f'C1', 'Parcel')

    for i, el in enumerate(sorted(result_.items(), key=lambda l: len(l[1]))):
        worksheet.write(f'A{i + 2}', str(el[0]))
        worksheet.write(f'B{i + 2}', len(el[1]))
        worksheet.write(f'C{i + 2}', '; '.join(el[1]))

    print(f'Request completed in {time.time() - start_time:.2f}')
    workbook.close()


if __name__ == '__main__':
    document = 'Invoices'
    org_id = '146727697690965488373260637295707385270'
    design_name = 'Target_DisruptiveNetwork_RSX_7.7_Invoices_to_X12_4010_Transaction-810'
    with open(f'resources/TargetCorporation7.7{document}.json', 'r') as file_data:
        data_ = json.load(file_data)

    report = make_report(org_id, design_name, data_)

    load_to_xslx('report_parcels', Counter(report))

# Add Unable to retrieve file by '11975884751' parcel uid to report
# Fix 'NoneType' object has no attribute 'groups'
