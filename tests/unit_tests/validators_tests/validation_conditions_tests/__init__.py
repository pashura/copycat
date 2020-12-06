CONDITIONS = {
    'conjunction': '',
    'conditions': [
        {'condition': 'present', 'element': 'element1', 'value': ''},
        {'condition': 'equals', 'element': 'element2', 'value': 'ZZ'}
    ]
}

RESULTS = {
    'conjunction': 'and',
    'conditions': [
        {'condition': 'required', 'element': 'element3', 'value': ''},
        {'condition': 'equals', 'element': 'element4', 'value': '1'},
        {'condition': 'minLength', 'element': 'element5', 'value': '6'},
        {'condition': 'maxLength', 'element': 'element5', 'value': '8'}
    ]
}

VALIDATION_CONDITION_WITH_RULES = {
    'type': 'Condition With Rules',
    'conditions': [],
    'results': [],
    'rules': [CONDITIONS]
}

VALIDATION_CONDITION_IF_THEN_WITH_OR_CONJUNCTION = {
    'type': 'ifThen',
    'rules': [],
    'conditions': [dict(CONDITIONS, conjunction='or')],
    'results': [dict(RESULTS, conjunction='or')]
}

VALIDATION_CONDITION_IF_THEN_WITH_AND_CONJUNCTION = {
    'type': 'ifThen',
    'rules': [],
    'conditions': [dict(CONDITIONS, conjunction='and')],
    'results': [dict(RESULTS, conjunction='and')]
}


class DummyValidator:
    def validate(self, *args, **kwargs):
        pass
