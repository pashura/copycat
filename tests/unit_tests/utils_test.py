from unittest.mock import patch

from copy_cat.utils import (
    find_child_schema_object,
    find_dictionary,
    get_schema_object_name,
    traverse_path_in_schema_object
)


def test_traverse_path_in_schema_object_should_find_element_by_name_and_suffix():
    path = "Segment-REF-Suffix/REF02"
    schema_object = {"name": "random", "children": [{"name": "Segment-REF", "suffix": "Suffix", "children": [
        {"name": "REF02", "children": []}]}]}
    expected = {"name": "REF02", "children": []}
    actual = traverse_path_in_schema_object(schema_object, path)
    assert expected == actual


def test_traverse_path_in_schema_object_should_return_none_if_path_does_not_match_children():
    path = "Segment-REFXX/REF02"
    schema_object = {"name": "random", "children": [{"name": "Segment-REF", "children": [
        {"name": "REF02", "children": []}]}]}
    expected = None
    actual = traverse_path_in_schema_object(schema_object, path)
    assert expected == actual


def test_traverse_path_in_schema_object_should_return_none_when_path_to_traverse_is_empty():
    schema_object = {"name": "random", "children": [{"name": "Segment-REF", "children": [
        {"name": "REF02", "children": []}]}]}
    expected = None
    actual = traverse_path_in_schema_object(schema_object, '')
    assert expected == actual


def test_find_child_schema_object_should_return_none_if_children_is_not_present():
    result = find_child_schema_object({}, "Segment-REF")
    assert result is None


@patch('copy_cat.utils.get_schema_object_name')
def test_find_child_schema_object_should_call_get_schema_object_name(mock_get_schema_object_name):
    parent = {"name": "Transaction-810", "children": [{"name": "Segment-REF", "suffix": "test"}]}
    find_child_schema_object(parent, "Segment-REF")
    mock_get_schema_object_name.assert_called_with({"name": "Segment-REF", "suffix": "test"})


def test_find_child_schema_object_should_return_the_correct_object():
    parent = {"name": "Transaction-810", "children": [{"name": "Segment-REF", "suffix": "test"},
                                                      {"name": "Segment-REF"}]}
    result = find_child_schema_object(parent, "Segment-REF")
    assert result == {"name": "Segment-REF"}


def test_find_child_schema_object_should_return_none_if_child_does_not_exist():
    parent = {"name": "Transaction-810", "children": [{"name": "Segment-REF", "suffix": "test"},
                                                      {"name": "Segment-REF"}]}
    result = find_child_schema_object(parent, "Segment-BIG")
    assert result is None


def test_get_schema_object_name_should_return_none_if_name_is_unavailable():
    result = get_schema_object_name({})
    assert result is None


def test_get_schema_object_name_should_return_name_if_available():
    result = get_schema_object_name({"name": "Loop-HL"})
    assert result == "Loop-HL"


def test_get_schema_object_name_should_return_none_if_only_suffix():
    result = get_schema_object_name({"suffix": "Shipment"})
    assert result is None


def test_get_schema_object_name_should_return_name_hyphen_suffix_if_both_are_present():
    result = get_schema_object_name({"name": "Loop-HL", "suffix": "Shipment"})
    assert result == "Loop-HL-Shipment"


def test_find_dictionary_returns_dict_requested_when_updated_conditional_element_is_none():
    json_array = [{"name": "REF01", "id": 1}, {"name": "REF02", "id": 2}, {"name": "REF03", "id": 3}]
    result = find_dictionary(json_array, "name", "REF03")
    assert result == json_array[2]


def test_find_dictionary_returns_none_if_it_does_not_exist_when_updated_conditional_element_is_none():
    json_array = [{"name": "REF01", "id": 1}, {"name": "REF02", "id": 2}, {"name": "REF03", "id": 3}]
    result = find_dictionary(json_array, "name", "REF04")
    assert result is None
