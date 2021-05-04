import pytest

import client


my_var_foo = {"MY_VAR": {"key": "MY_VAR", "value": "foo", "is_secret": False}}
my_var_bar = {"MY_VAR": {"key": "MY_VAR", "value": "bar", "is_secret": False}}
another_var = {"ANOTHER_VAR": {"key": "ANOTHER_VAR", "value": "foo", "is_secret": False}}
two_vars = {
    "MY_VAR": {"key": "MY_VAR", "value": "foo", "is_secret": False},
    "ANOTHER_VAR": {"key": "ANOTHER_VAR", "value": "foo", "is_secret": False},
}
no_var = None
empty_dict = {}

compare_test_data = [
    (my_var_foo, my_var_foo, empty_dict, empty_dict), # nothing changes
    (my_var_foo, my_var_bar, my_var_foo, my_var_bar), # env var value changes
    (my_var_foo, two_vars, empty_dict, another_var), # 2 env vars exist, one to be removed from config
    (two_vars, my_var_foo, another_var, empty_dict), # one env var exists, one to be added from config
    (my_var_foo, no_var, my_var_foo, empty_dict), # no env vars exist, one to be added from config
    (no_var, my_var_foo, empty_dict, my_var_foo), # one env var exists, none listed in config
]


@pytest.mark.parametrize("desired_values,actual_values,values_to_add,values_to_delete", compare_test_data)
def test_compare(desired_values, actual_values, values_to_add, values_to_delete):
    results_to_add, results_to_delete = client.compare(actual_values, desired_values)
    assert results_to_add == values_to_add
    assert results_to_delete == values_to_delete
