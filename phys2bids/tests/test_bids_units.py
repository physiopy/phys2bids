from phys2bids.bids_units import bidsify_units


def test_bidsify_units():
    # test normal unit
    assert bidsify_units('V') == 'V'
    # test unit with standard prefix
    assert bidsify_units('centik') == 'cK'
    # test unit with not standard prefix
    assert bidsify_units('matV') == 'matV'
    # test unit that's not bids standard
    assert bidsify_units('mmlie') == 'mmlie'
