from typing import List

from copy_cat.core.transformer.sorter import FedsSorter
from copy_cat.models.design import DesignObject
from copy_cat.models.feds import FedsDocument, FedsSegment, FedsElement
from copy_cat.models.test_data import DataObject
from copy_cat.utils import get_reps_and_location


class Transformer:
    def __init__(self):
        self.document = None
        self.locations = []

    def transform(
        self,
        design: DesignObject,
        reversed_design: DesignObject,
        test_data: List[DataObject],
    ) -> List:
        self.document = FedsDocument(
            document=f"D{design.name.removeprefix('Transaction-')}",
            partnership=self._add_header(),
        )
        self._process_test_data(test_data, reversed_design)
        self._collect_locations(design)
        FedsSorter().sort(self.document, self.locations)
        return self.document.feds_representation

    @staticmethod
    def _add_header():
        # Get hub id from Company Aggregator
        hub_id = "hub"
        return f"P{hub_id}ALLAPPDEV"

    def _process_test_data(
        self, test_data: List[DataObject], reversed_design: DesignObject
    ):
        for test_data_obj in test_data:
            location, reps = get_reps_and_location(test_data_obj.location_without_root)
            if not (design_object := reversed_design.get_child_by_location(location)):
                continue
            if (source := design_object.sourcing) and design_object.visible:
                segment = self.__segment(source, reps)
                element = (
                    self.__composite(
                        source, test_data_obj.value, design_object.restriction
                    )
                    if source.is_composite
                    else self.__element(
                        source, test_data_obj.value, design_object.restriction
                    )
                )

                self.__combine_data(segment, element)

    @staticmethod
    def __segment(source_location, reps):
        segment = FedsSegment(
            name=source_location.record_name.split("-")[-1],
            location=source_location.location,
            reps=reps,
        )
        for i, rep in enumerate(reps):
            segment.repetitions.append(reps[i]["rep_number"])
        return segment

    @staticmethod
    def __element(source_location, value, restriction):
        return FedsElement(
            value=value,
            element_id=f"0{source_location.location[-2:]}",
            dataType=restriction.display_name,
        )

    @staticmethod
    def __composite(source_location, value, restriction):
        return FedsElement(
            value=value,
            element_id=f"0{source_location.parent_name[-2:]}",
            composite_id=f"0{source_location.location.split('-')[-1]}",
            dataType=restriction.display_name,
        )

    def __combine_data(self, segment, element):
        if current := next(
            (
                item
                for item in self.document.segments
                if item.unique_id == segment.unique_id
            ),
            None,
        ):
            current.elements.append(element)
        else:
            segment.elements.append(element)
            self.document.segments.append(segment)

    def _collect_locations(self, schema_object):
        for child in schema_object.children:
            self.locations.append(child.location)
            self._collect_locations(child)
