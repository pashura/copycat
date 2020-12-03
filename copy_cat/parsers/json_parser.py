
class JSONParser:
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def parse(self):
        return self._flatten(self.json_obj)

    def _flatten(self, current: dict, result=None):
        if result is None:
            result = []
        if isinstance(current, dict) and current.get('text') is None:
            for key in current:
                self._flatten(current[key], result)
        elif isinstance(current, list):
            for key in current:
                self._flatten(key, result)
        elif isinstance(current, dict) and current.get('text') is not None:
            result.append(current)
        return result
