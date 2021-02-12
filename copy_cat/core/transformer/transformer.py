import re

from copy_cat.enums.object_type import ObjectType
from copy_cat.parsers.design_parser import DesignParser
from copy_cat.utils import get_reps_and_location, traverse_path_in_schema_object, find_dictionary


class Transformer:
    def __init__(self):
        self.result = """
P8PSALLAPPDEV
D810
"""
        self.temp_res = {}
        self.temp_res_list = []
        self.temp_res_nested = {}

        self.locations = []

    def transform(self, design, reversed_design, test_data):

        dp = DesignParser()
        self._collect_locations(design)

        dp.parse(design, test_data)


        # a = next(('/'.join(test_data_obj.location.split('/')[2:]) for test_data_obj in test_data), None)
        # self.temp_res_nested = current = {}
        for test_data_obj in test_data:
        # for test_data_obj in dp.result:
            location = '/'.join(test_data_obj.location.split('/')[2:])
            location, reps = get_reps_and_location(location)

            design_object = traverse_path_in_schema_object(reversed_design, location)
            if not design_object:
                print(location + " is not in design")
            elif design_object.get('visible'):
                if source_location := self.get_source_location(design_object):
                    value = test_data_obj.value
                    restriction_obj = find_dictionary(design_object.get("attributes"), "elementType",
                                                      "restriction") or {}

                    if restriction_obj.get('displayName') in ['Date', 'Time']:
                        value = value.replace("-", "").replace(":", "")

                    segment = self.generate_feds_segment(source_location)
                    element = self.generate_feds_element(source_location, value)

                    if len(reps):

                        for i, rep in enumerate(reps):
                            segment += f"_{reps[i]['rep_number']}"
                        obj = {
                            'location': '/'.join(source_location.split('/')[:-2]),
                            'reps': reps
                        }

                    # prev = object()
                    # [prev:=v for v in self.temp_res_list if prev!=v]
                    parents = sorted(['/'.join(source_location.split('/')[:k-1]) for k, i in enumerate(source_location.split('/')) if source_location.split('/')[:k-1] and len(source_location.split('/')[:k-1])> 1])
                    one_result = {
                        'segment': segment,
                        'elements': [element],
                        'location': '/'.join(source_location.split('/')[:-1]),
                        'parent': '/'.join(source_location.split('/')[:-2]) if len(reps) else '',
                        'first_element': source_location,
                        'parents': parents,
                        'level': len(parents)
                    }

                    if self.temp_res.get(segment) is None:
                        self.temp_res[segment] = [element]

                        self.temp_res_list.append(one_result)
                    else:
                        self.temp_res[segment].append(element)

                        current = next((item for item in self.temp_res_list if item.get('segment', '') == segment), {})

                        current['elements'].append(element)

                    tmp_parents = sorted(['/'.join(source_location.split('/')[:k-1])
                                          for k, i in enumerate(source_location.split('/'))
                                          if source_location.split('/')[:k-1]])

                    self.populate_dict(source_location.split('/'), self.temp_res_nested, one_result, reps)
        self.sort_result()
        self.transform_to_feds()

    def populate_dict(self, item, existing_dict, one_result, reps, full_path=None):
        if len(item) == 1:
            existing_dict[item[0]] = one_result
        else:
            head, tail = item[0], item[1:]
            original_head = head

            # end = '_'.join(one_result.get('segment').split('_')[1:])
            # # print(f"end => {end} ")
            # if head != 'Transaction-810' and not head.endswith(f'_{end}'):
            #     head = re.sub('-[A-Z0-9]*', f'-{one_result.get("segment")}', head, flags=re.DOTALL)
            #
            # print(f"head => {head} ")
            # print(f"tail => {tail} ")

            # if len(reps) and head != 'Transaction-810':
            #     for i, rep in enumerate(reps):
            #         if not head.endswith(reps[0]['rep_number']):
            #             head += f"-{reps[0]['rep_number']}"
            #         existing_dict.setdefault(head, {})
            # else:
            #     existing_dict.setdefault(head, {})
            if len(reps) and head != 'Transaction-810':
                r = reps[-2] if len(reps) > 1 else reps[-1]
                head += f"-{r['rep_number']}"

                # for i, rep in enumerate(reps):
                #     # if not head.endswith(rep['rep_number']):
                #     #     head += f"-{rep['rep_number']}"
                #     if i == 0:
                #         head += f"-{rep['rep_number']}"

            existing_dict.setdefault(head, {})

            self.populate_dict(
                tail,
                existing_dict[head],
                one_result,
                reps,
                full_path="/".join([x for x in (full_path, original_head) if x is not None])
            )

    @staticmethod
    def generate_feds_segment(source_location):
        # Removed S
        return f"{(source_location.split('/')[-2]).split('-')[-1]}"

    @staticmethod
    def generate_feds_element(source_location, value):
        split_source = source_location.split('/')
        return f"E0{(split_source[-1]).removeprefix((split_source[-2]).split('-')[-1])}000{value}"

    @staticmethod
    def get_source_location(design_object):
        return design_object.get('sourcing', {}).get('location')

    def _collect_locations(self, schema_object):
        for child in schema_object['children']:
            self.locations.append(child.get('location'))
            self._collect_locations(child)

    @staticmethod
    def conditional_sort(ls, f):
        y = iter(sorted(w for w in ls if f(w)))
        return [w if not f(w) else next(y) for w in ls]

    def sort_result(self):
        for i in self.temp_res_list:
            for key, value in i.items():
                if key == ObjectType.ELEMENTS:
                    i[key] = sorted(value)
        self.conditional_sort(self.temp_res_list, lambda w: 'a' in w)
        # self.temp_res_list.sort(key=lambda x: (self.locations.index(x['location']), self.locations.index(x['first_element'])))
        self.temp_res_list.sort(key=lambda x: tuple([self.locations.index(i) for i in x['parents']]))

    def transform_to_feds(self):
        for i in self.temp_res_list:
            for key, value in i.items():
                if key == ObjectType.SEGMENT:
                    self.result += f"{value.split('-')[0]}\n"
                elif key == ObjectType.ELEMENTS:
                    for el in value:
                        self.result += f"{el}\n"

    # def transform_v2(self, design, reversed_design, test_data):

        # dp = DesignParser()
        # self._collect_locations(design)
        #
        # dp.parse(design, test_data)

