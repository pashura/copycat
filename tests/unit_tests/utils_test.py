from copy_cat.utils import find_dictionary


def test_find_dictionary_returns_dict_requested_when_updated_conditional_element_is_none():
    json_array = [
        {"name": "REF01", "id": 1},
        {"name": "REF02", "id": 2},
        {"name": "REF03", "id": 3},
    ]
    result = find_dictionary(json_array, "name", "REF03")
    assert result == json_array[2]


def test_find_dictionary_returns_none_if_it_does_not_exist_when_updated_conditional_element_is_none():
    json_array = [
        {"name": "REF01", "id": 1},
        {"name": "REF02", "id": 2},
        {"name": "REF03", "id": 3},
    ]
    result = find_dictionary(json_array, "name", "REF04")
    assert result is None
