from operator import itemgetter


class FedsSorter:
    def sort(self, document, locations):
        for segment in document.segments:
            segment.elements.sort(key=lambda x: (x.element_id, x.composite_id))

        document.segments.sort(key=lambda x: locations.index(x.location))
        sorted_paths = self._sort_stuff(
            [segment.xpath for segment in document.segments]
        )
        document.segments.sort(key=lambda x: sorted_paths.index(x.xpath))

    def _sort_stuff(self, original_list):
        intermediate_list = [path.split("/") for path in original_list]
        longest_path_length = len(max(intermediate_list, key=len)) - 1
        for path_chunk_index in range(longest_path_length):
            if paths_with_reps := self._get_paths_with_reps(
                intermediate_list, path_chunk_index
            ):
                self._sort_intermediate_list(intermediate_list, paths_with_reps)
        resulting_list = ["/".join(path) for path in intermediate_list]
        return resulting_list

    @staticmethod
    def _sort_intermediate_list(intermediate_list, paths_with_reps):
        for item, value in paths_with_reps.items():
            start = value["start_position"]
            end = value["end_position"] + 1
            key_element_position = item.count("/") + 1
            intermediate_list[start:end] = sorted(
                intermediate_list[start:end], key=itemgetter(key_element_position)
            )

    @staticmethod
    def _get_paths_with_reps(intermediate_list, path_chunk_index):
        paths_with_reps = {}
        for path_index, path in enumerate(intermediate_list):
            if len(path) > path_chunk_index:
                path_chunk = path[path_chunk_index]
                if path_chunk.startswith("[") and path_chunk.endswith("]"):
                    key = "/".join(path[:path_chunk_index])
                    if paths_with_reps.get(key):
                        paths_with_reps[key]["end_position"] = path_index
                    else:
                        paths_with_reps[key] = {
                            "start_position": path_index,
                            "end_position": path_index,
                        }
        return paths_with_reps
