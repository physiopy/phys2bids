from phys2bids.bids_units import bidsify_units
from phys2bids.bids_units import unit_aliases


def test_bidsify_units():
    # test unit with standard prefix
    assert bidsify_units('centik') == 'cK'
    # test unit with not standard prefix
    assert bidsify_units('matV') == 'matV'
    # test unit that's not bids standard
    assert bidsify_units('mmlie') == 'mmlie'
    # test there is not problem with every unit in the dict
    for unit_key in unit_aliases.keys():
        assert bidsify_units(unit_key) == unit_aliases[unit_key]
