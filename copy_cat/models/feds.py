from typing import List, Optional

from pydantic import Field

from copy_cat.models.base import BaseFeds


class FedsElement(BaseFeds):
    value: str
    element_id: str
    composite_id: str = Field(default='000')
    identifier: str = Field(default='E')


class FedsSegment(BaseFeds):
    name: str
    elements: Optional[List[FedsElement]] = []
    location: str
    identifier: str = Field(default='S')
    repetitions: Optional[List[int]] = []

    reps: List  # temporary list -> remove

    @property
    def unique_id(self):
        return self.name + '-'.join(self.repetitions or [])

    @property
    def xpath(self):
        def parents():
            src = self.location.split('/')
            return sorted(['/'.join(src[:k - 1]) for k, i in enumerate(src) if src[:k - 1] and len(src[:k - 1]) > 1])

        def update_rep_for_edi(rep):
            rep['rep_name'] = parents()[-1].split('/')[1:][self.reps.index(rep)]
            return rep

        updated_location = self.location.split('/')
        for edi_rep in list(map(update_rep_for_edi, self.reps)):
            index_ = updated_location.index(edi_rep['rep_name']) + 1
            updated_location.insert(index_, f"[{edi_rep['rep_number']}]")
        return '/'.join(updated_location)


class FedsDocument(BaseFeds):
    header: str
    partnership: str
    identifier: str = Field(default='D')
    segments: List[FedsSegment] = []

    @property
    def feds_representation(self):
        feds = [self.header, self.partnership]
        for segment in self.segments:
            feds.append(f'{segment.identifier}{segment.name}')
            for element in segment.elements:
                feds.append(f'{element.identifier}{element.element_id}{element.composite_id}{element.value}')
        return feds

# FedsDocument.update_forward_refs()
