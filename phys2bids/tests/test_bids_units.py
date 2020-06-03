from phys2bids.bids_units import bidsify_units
from phys2bids.bids_units import UNIT_ALIASES


def test_bidsify_units():
    # Add a dictionary of test possibilities
    unit_tests = {
                  # test unit with standard prefix
                  'centik': 'cK', 'CENTIk': 'cK',
                  # test unit with not standard prefix
                  'matV': 'matV', 'BigV': 'BigV',
                  # test unit that are not bids standard
                  'mmHg': 'mmHg', 'mmlie': 'mmlie', 'MMLIE': 'MMLIE',
                 }
    # Actually test
    for unit_key in unit_tests.keys():
        assert bidsify_units(unit_key) == unit_tests[unit_key]
    # test there is not problem with every unit in the dict
    for unit_key in UNIT_ALIASES.keys():
        assert bidsify_units(unit_key) == UNIT_ALIASES[unit_key]
