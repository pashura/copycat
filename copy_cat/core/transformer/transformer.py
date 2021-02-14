from copy_cat.parsers.design_parser import DesignParser


class Transformer:
    def __init__(self):
        pass

    def transform(self, design, reversed_design, test_data):
        design_parser = DesignParser()

        design_parser.parse(design, test_data)

        self.sort_result()
        self.transform_to_feds()

    @staticmethod
    def get_source_location(design_object):
        return design_object.get('sourcing', {}).get('location')

    @staticmethod
    def conditional_sort(ls, f):
        return [w if not f(w) else next(iter(sorted(w for w in ls if f(w)))) for w in ls]

    def sort_result(self):
        pass

    def transform_to_feds(self):
        pass
