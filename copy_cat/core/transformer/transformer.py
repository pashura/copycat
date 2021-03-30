from operator import itemgetter

from copy_cat.enums.object_type import ObjectType
from copy_cat.utils import get_reps_and_location, traverse_path_in_schema_object, find_dictionary


class Transformer:
    def __init__(self):
        self.transformation_result = []
        self.temp_res = {}
        self.temp_res_list = []
        self.temp_res_nested = {}

        self.locations = []

    def transform(self, design, reversed_design, test_data):
        self._collect_locations(design)

        self._add_header()
        self._add_doc_number(design)
        self._process_test_data(test_data, reversed_design)
        self._sort_result()
        self._transform_to_feds()

    def _add_header(self):
        # Get hub id from Company Aggregator
        hub_id = 'hub'
        self.transformation_result.append(f'P{hub_id}ALLAPPDEV')

    def _add_doc_number(self, design):
        # TODO: Removed D - document
        self.transformation_result.append(f"D{design.get('name').removeprefix('Transaction-')}")

    def _process_test_data(self, test_data, reversed_design):
        for test_data_obj in test_data:
            location, reps = get_reps_and_location('/'.join(test_data_obj.location.split('/')[2:]))

            design_object = traverse_path_in_schema_object(reversed_design, location)
            if not design_object:
                print(location + " is not in design")
            elif design_object.get('visible'):
                if source_location := self.__get_source_location(design_object):
                    value = self.__update_value_for_date_and_time(design_object, test_data_obj.value)
                    segment = self.__generate_feds_segment(source_location)
                    element = self.__generate_feds_element(source_location, value)
                    segment = self.__update_segment_for_repetitions(segment, reps)
                    parents = self.__get_all_parents(source_location)

                    full_obj = self.__create_full_obj(parents, segment, element, source_location, reps)

                    self.__collect_data(segment, element, full_obj)
                    self.__populate_dict(source_location.split('/'), self.temp_res_nested, full_obj, reps)

    @staticmethod
    def __generate_feds_segment(source_location):
        # TODO: Removed S - segment
        record_index = -3 if 'Composite' in source_location.split('/')[-2] else -2
        return f"S{source_location.split('/')[record_index].split('-')[-1]}"

    @staticmethod
    def __generate_feds_element(source_location, value):
        # TODO: Removed E - element
        # TODO: Process composites
        split_source = source_location.split('/')
        composite_id = source_location.split('/')[-1].split('-')[-1]
        is_comp = 'Composite' in split_source[-2]
        record_index = -3 if is_comp else -2
        prefix_to_remove = f"{split_source[-2][:-2]}" if is_comp else split_source[record_index].split('-')[-1]
        zeros = f"0{composite_id}" if is_comp else "000"
        if is_comp:
            return f"E0{split_source[-2].removeprefix(prefix_to_remove)}{zeros}{value}"
        return f"E0{split_source[-1].removeprefix(prefix_to_remove)}{zeros}{value}"

    def _collect_locations(self, schema_object):
        for child in schema_object['children']:
            self.locations.append(child.get('location'))
            self._collect_locations(child)

    @staticmethod
    def conditional_sort(ls, f):
        return [w if not f(w) else next(iter(sorted(w for w in ls if f(w)))) for w in ls]

    def _sort_result(self):
        for i in self.temp_res_list:
            for key, value in i.items():
                if key == ObjectType.ELEMENTS.value:
                    i[key] = sorted(value)
        self.conditional_sort(self.temp_res_list, lambda w: 'a' in w)
        self.temp_res_list.sort(key=lambda x: self.locations.index(x['location']))

        paths = [m['updated_location'] for m in self.temp_res_list]
        sorted_paths = self.sort_stuff(paths)
        self.temp_res_list.sort(key=lambda x: sorted_paths.index(x['updated_location']))

    def _transform_to_feds(self):
        for i in self.temp_res_list:
            for key, value in i.items():
                if key == ObjectType.SEGMENT.value:
                    self.transformation_result.append(f"{value.split('_')[0]}")
                elif key == ObjectType.ELEMENTS.value:
                    for el in value:
                        self.transformation_result.append(el)

    @staticmethod
    def __get_source_location(design_object):
        # TODO: Process conditional sourcing
        return design_object.get('sourcing', {}).get('location')

    @staticmethod
    def __update_value_for_date_and_time(design_object, value):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        if restriction_obj.get('displayName') in ['Date', 'Time']:
            return value.replace("-", "").replace(":", "")
        return value

    @staticmethod
    def __update_segment_for_repetitions(segment, reps):
        if len(reps):
            for i, rep in enumerate(reps):
                segment += f"_{reps[i]['rep_number']}"
        return segment

    @staticmethod
    def __get_all_parents(source_location):
        src = source_location.split('/')
        return sorted(['/'.join(src[:k - 1]) for k, i in enumerate(src) if src[:k - 1] and len(src[:k - 1]) > 1])

    @staticmethod
    def __create_full_obj(parents, segment, element, source_location, reps):

        def update_for_edi(rep):
            loops = parents[-1].split('/')[1:]
            rep['rep_name'] = loops[reps.index(rep)]
            return rep

        edi_reps = list(map(update_for_edi, reps))
        updated_location = source_location.split('/')
        for e in edi_reps:
            index_ = updated_location.index(e['rep_name']) + 1
            updated_location.insert(index_, f"[{e['rep_number']}]")
        return {
            'segment': segment,
            'elements': sorted([element]),
            'location': '/'.join(source_location.split('/')[:-1]),
            'updated_location': '/'.join(updated_location)
        }

    def __collect_data(self, segment, element, full_obj):
        if self.temp_res.get(segment) is None:
            self.temp_res[segment] = [element]
            self.temp_res_list.append(full_obj)
        else:
            self.temp_res[segment].append(element)
            current = next((item for item in self.temp_res_list if item.get('segment', '') == segment), {})
            current['elements'].append(element)

    def __populate_dict(self, item, existing_dict, full_obj, reps, full_path=None):
        if len(item) == 1:
            existing_dict[item[0]] = full_obj
        else:
            head, tail = item[0], item[1:]
            original_head = head

            if len(reps) and 'Transaction' not in head:
                head += f"-{reps[-2] if len(reps) > 1 else reps[-1]['rep_number']}"

            existing_dict.setdefault(head, {})
            full_path = "/".join([x for x in (full_path, original_head) if x is not None])

            self.__populate_dict(tail, existing_dict[head], full_obj, reps, full_path=full_path)

    def sort_stuff(self, original_list):
        intermediate_list = [path.split('/') for path in original_list]
        longest_path_length = len(max(intermediate_list, key=len)) - 1
        for path_chunk_index in range(longest_path_length):
            if paths_with_reps := self.get_paths_with_reps(intermediate_list, path_chunk_index):
                self.sort_intermediate_list(intermediate_list, paths_with_reps)
        resulting_list = ['/'.join(path) for path in intermediate_list]
        return resulting_list

    @staticmethod
    def sort_intermediate_list(intermediate_list, paths_with_reps):
        for item, value in paths_with_reps.items():
            start = value['start_position']
            end = value['end_position'] + 1
            key_element_position = item.count('/') + 1
            intermediate_list[start: end] = sorted(intermediate_list[start: end], key=itemgetter(key_element_position))

    @staticmethod
    def get_paths_with_reps(intermediate_list, path_chunk_index):
        paths_with_reps = {}
        for path_index, path in enumerate(intermediate_list):
            if len(path) > path_chunk_index:
                path_chunk = path[path_chunk_index]
                if path_chunk.startswith("[") and path_chunk.endswith("]"):
                    key = '/'.join(path[:path_chunk_index])
                    if paths_with_reps.get(key):
                        paths_with_reps[key]['end_position'] = path_index
                    else:
                        paths_with_reps[key] = {'start_position': path_index, 'end_position': path_index}
        return paths_with_reps
