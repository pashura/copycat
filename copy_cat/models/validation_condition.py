from typing import List

from copy_cat.models.base import BaseValidationCondition


class Condition(BaseValidationCondition):
    condition: str
    element: str
    value: str


class Conditions(BaseValidationCondition):
    conjunction: str
    conditions: List[Condition]


class ValidationCondition(BaseValidationCondition):
    type: str
    conditions: List[Conditions]
    results: List[Conditions]
    rules: List[Conditions]
