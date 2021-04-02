class UnsupportedValidationConditionTypeError(Exception):
    def __init__(self):
        super().__init__("Unsupported Validation Condition")
