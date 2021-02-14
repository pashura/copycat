
class JSONParser:

    def parse(self, json_obj):
        return self._flatten(json_obj)

    def _flatten(self, current: dict, result=None):
        if result is None:
            result = []
        if isinstance(current, dict):
            result.append(current)
            for key in current:
                self._flatten(current[key], result)
        elif isinstance(current, list):
            for key in current:
                self._flatten(key, result)
        return result
